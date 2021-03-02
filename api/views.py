import os

from pyramid.view import view_config

from .adapter import (
    mount_json_for_reports,
    mount_json_for_status_alert,
    mount_json_for_members,
    wrapper_mount_json_for_report
)

from .db_calls import PROCEDURE_DETECTOR_DICT
from .errors import *
from .models import db_session
from .utils import get_counter_table, handle_str_date, is_valid_date_range, is_valid_issn, is_valid_date_format

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
        Status = get_counter_table(self.request, 'counter_status')
        Alert = get_counter_table(self.request, 'counter_alert')

        status = db_session.query(Status).filter_by(status_id=1).one()
        result_query_alert = db_session.query(Alert).filter(Alert.is_active == 1)
        json_status = mount_json_for_status_alert(status, result_query_alert)
        return json_status

    @view_config(route_name='members', renderer='json')
    def members(self):
        Member = get_counter_table(self.request, 'counter_member')

        result_query_members = db_session.query(Member).all()
        json_members = mount_json_for_members(result_query_members)
        return json_members

    @view_config(route_name='reports', renderer='json')
    def reports(self):
        Report = get_counter_table(self.request, 'counter_report')

        result_query_reports = db_session.query(Report).all()
        json_counter_reports = mount_json_for_reports(result_query_reports)
        return json_counter_reports

    @view_config(route_name='reports_report_id', renderer='json')
    def reports_report_id(self):
        Report = get_counter_table(self.request, 'counter_report')

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
            report_data = db_session.query(Report).filter_by(report_id=report_id).one()
        except:
            db_session.rollback()
            report_data = {}

        attrs['report_data'] = report_data

        json_metrics = _wrapper_call_report(report_id, attrs)

        # Caso não existam dados de acesso para o período selecionado
        if len(json_metrics.get('Report_Items', [])) == 0:
            return error_no_usage_available()

        # Verifica se há parâmetros inválidos na request
        invalid_filters = _check_filters(self.request.params)
        if len(invalid_filters) > 0:
            json_metrics['Exceptions'] = error_invalid_report_filter_value(invalid_filters, severity='warning')

        return json_metrics


def _wrapper_call_report(report_id, attrs):
    granularity, mode = _get_granularity_and_mode(attrs)
    procedure_name, params_names = PROCEDURE_DETECTOR_DICT.get(granularity, {}).get(mode, {}).get(report_id, ('', []))

    if procedure_name and params_names:
        params = []

        for p in params_names:
            p_value = attrs.get(p)
            if p_value:
                params.append(p_value)

        result_query_metrics = db_session.execute(procedure_name % tuple(params))
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
