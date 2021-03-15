import os

from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .adapter import (
    mount_json_for_reports,
    mount_json_for_status_alert,
    mount_json_for_members,
    wrapper_mount_json_for_report
)

from .db_calls import PROCEDURE_DETECTOR_DICT
from .errors import *
from .lib.database import get_dates_unavailable
from .models import DBSession
from .sql_declarative import Status, Alert, Member, Report
from .utils import handle_str_date, is_valid_date_range, is_valid_issn, is_valid_date_format


COLLECTION = os.environ.get('collection', 'scl')
VALID_FILTERS = {'granularity',
                 'customer_id',
                 'issn',
                 'pid',
                 'begin_date',
                 'end_date'}


class CounterViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='json')
    def home(self):
        return self.status()

    @view_config(route_name='status', renderer='json')
    def status(self):
        status = DBSession.query(Status).order_by(Status.status_id.desc()).first()
        result_query_alert = DBSession.query(Alert).filter(Alert.is_active == 1)
        json_status = mount_json_for_status_alert(status, result_query_alert)
        return json_status

    @view_config(route_name='members', renderer='json')
    def members(self):
        result_query_members = DBSession.query(Member).all()
        json_members = mount_json_for_members(result_query_members)
        return json_members

    @view_config(route_name='reports', renderer='json')
    def reports(self):
        result_query_reports = DBSession.query(Report).all()
        json_counter_reports = mount_json_for_reports(result_query_reports)
        return json_counter_reports

    @view_config(route_name='reports_report_id', renderer='json')
    def reports_report_id(self):
        report_id = self.request.matchdict.get('report_id', '')

        ####################
        # required filters #
        ####################
        customer = self.request.params.get('customer', '')
        params_begin_date = self.request.params.get('begin_date', '')
        params_end_date = self.request.params.get('end_date', '')

        begin_date = _check_date(params_begin_date, 'begin_date')
        if not isinstance(begin_date, str):
            return begin_date

        end_date = _check_date(params_end_date, 'end_date')
        if not isinstance(end_date, str):
            return end_date

        # Check if date range is valid
        if not is_valid_date_range(begin_date, end_date):
            return error_invalid_date_arguments()

        # TODO: é preciso popular as tabelas counter_customer e counter_institution

        ####################
        # optional filters #
        ####################
        issn = self.request.params.get('issn', '')
        pid = self.request.params.get('pid', '')

        if 'issn' in self.request.params:
            if not is_valid_issn(issn):
                return error_invalid_report_filter_value(issn, severity='error')

        granularity = self.request.params.get('granularity', 'monthly')

        # all attributes/parameters
        attrs = {
            'customer': customer,
            'issn': issn,
            'pid': pid,
            'granularity': granularity,
            'institution': '',
            'institution_id': '',
            'begin_date': begin_date,
            'end_date': end_date,
            'platform': 'Scientific Electronic Library Online',
            'report_data': '',
            'collection': COLLECTION
        }

        try:
            report_data = DBSession.query(Report).filter_by(report_id=report_id).one()
        except NoResultFound or MultipleResultsFound:
            report_data = {}

        attrs['report_data'] = report_data

        json_metrics = _wrapper_call_report(report_id, attrs)

        # Caso não existam dados de acesso para o período selecionado
        if len(json_metrics.get('Report_Items', [])) == 0:
            return error_no_usage_available()

        # Obtém exceções
        exceptions = check_exceptions(self.request.params, begin_date, end_date, report_id)
        if exceptions:
            json_metrics['Exceptions'] = exceptions

        return json_metrics


def check_exceptions(params, begin_date, end_date, report_id):
    exceptions = []

    # Verifica se há parâmetros inválidos na request
    invalid_filters = _check_filters(params)
    if len(invalid_filters) > 0:
        exceptions.append(error_invalid_report_filter_value(invalid_filters, severity='warning'))

    # Verifica se há datas com dados ausentes nas tabelas sushi
    unavailable_dates = get_dates_unavailable(begin_date, end_date, COLLECTION, report_id)
    if len(unavailable_dates) > 0:
        exceptions.append(error_partial_data(unavailable_dates))

    return exceptions


def _wrapper_call_report(report_id, attrs):
    granularity, mode = _get_granularity_and_mode(attrs)
    procedure_name, params_names = PROCEDURE_DETECTOR_DICT.get(granularity, {}).get(mode, {}).get(report_id, ('', []))

    if procedure_name and params_names:
        params = []

        for p in params_names:
            p_value = attrs.get(p)
            if p_value:
                params.append(p_value)

        result_query_metrics = DBSession.execute(procedure_name % tuple(params))
        return wrapper_mount_json_for_report(report_id, result_query_metrics, attrs)

    return {}


def _get_granularity_and_mode(attrs):
    granularity = attrs.get('granularity', 'totals')

    if attrs['issn'] != '':
        mode = 'issn'
    elif attrs['pid'] != '':
        mode = 'pid'
    else:
        mode = 'global'

    return granularity, mode


def _check_filters(params):
    invalid_filters = []

    for p in params:
        if p not in VALID_FILTERS:
            invalid_filters.append(p)

    return invalid_filters


def _check_date(param_date, name):
    # Check if begin_date was informed
    if not param_date:
        return error_required_filter_missing(name)

    # Check if begin_date format is valid
    if not is_valid_date_format(param_date):
        return error_invalid_date_arguments()

    # Check if begin_date is a valid date
    try:
        if name == 'end_date':
            return handle_str_date(param_date, is_end_date=True)
        else:
            return handle_str_date(param_date)
    except ValueError or TypeError or AttributeError as e:
        if 'unconverted data' or 'argument of type' or 'parameter date' in e:
            return error_invalid_date_arguments()
