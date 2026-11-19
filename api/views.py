from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from api import adapter, errors, utils, values
from api.libs import cleaner, db, validator


class CounterViews(object):
    def __init__(self, request):
        self.request = request

    def _override_render(self):
        fmt = self.request.GET.get('fmt', 'json')
        if fmt == 'tsv':
            self.request.override_renderer = 'tsv'
        else:
            self.request.override_renderer = 'json'

    @view_config(route_name='home', renderer='json')
    def home(self):
        return self.status()

    @view_config(route_name='status', renderer='json')
    def status(self):
        res_status = db.get_status()
        res_alert = db.get_alert(is_active = 1)

        return adapter.mount_json_for_status_alert(res_status, res_alert)

    @view_config(route_name='members', renderer='json')
    def members(self):
        res_members = db.get_members()

        return adapter.mount_json_for_members(res_members)

    @view_config(route_name='reports', renderer='json')
    def reports(self):
        res_reports = db.get_reports()

        return adapter.mount_json_for_reports(res_reports)

    def _ir_a1_admission_response(self):
        settings = self.request.registry.settings
        limit = settings.get('sushi.ir_a1_max_concurrent')
        if limit is None:
            return None

        if limit == 0:
            detail = 'The ir_a1 report is temporarily disabled.'
        else:
            slots = settings['sushi.ir_a1_slots']
            if slots.acquire(blocking=False):
                # Keep the slot through response rendering and transaction cleanup.
                self.request.add_finished_callback(lambda request: slots.release())
                return None
            detail = 'The ir_a1 report is busy. Retry later.'

        response = Response(
            status=503,
            content_type='application/json',
            json_body=errors.error_service_not_available(detail),
        )
        response.cache_control.no_store = True
        if limit:
            response.retry_after = 5
        return response

    @view_config(route_name='reports_report_id', renderer='json')
    def reports_report_id(self):
        report_id = self.request.matchdict.get('report_id', '')
        if report_id == 'ir_a1':
            rejection = self._ir_a1_admission_response()
            if rejection is not None:
                return rejection

        required_params = utils.extract_parameters(self.request, values.URI_REQUIRED_PARAMETERS)
        optional_params = utils.extract_parameters(self.request, values.URI_OPTIONAL_PARAMETERS)

        rp_validation_results = validator.validate_parameters(required_params, values.URI_REQUIRED_PARAMETERS)
        if len(rp_validation_results['errors']) > 0:
            return rp_validation_results['errors']

        op_validation_results = validator.validate_parameters(optional_params)
        if len(op_validation_results['errors']) > 0:
            return op_validation_results['errors']

        special_validation_results = validator.validate_parameters_according_to_report(report_id, {**optional_params, **required_params})
        if len(special_validation_results['errors']) > 0:
            return special_validation_results['errors']

        cleaned_params = cleaner.clean_parameters(rp_validation_results, op_validation_results)
        utils.set_collection_extra(report_id, cleaned_params)

        # Validate that the collection exists in the database
        collection = cleaned_params.get('collection')
        if collection and not db.collection_exists(collection):
            return [errors.error_invalid_collection(collection)]

        try:
            report_db_params = db.get_report_by_id(report_id=report_id)
        except (NoResultFound, MultipleResultsFound):
            return errors.error_report_not_supported()
        cleaned_params['report_db_params'] = report_db_params

        report_exceptions = utils.check_exceptions(report_id, self.request.GET.keys(), cleaned_params)
        report_query = utils.wrapper_call_report(report_id, cleaned_params)

        if report_query is None:
            return errors.error_report_not_supported()

        result_proxy = db.call_procedure(report_query)

        data = utils.extract_report_data(result_proxy)

        if data is None:
            return errors.error_report_not_supported()

        if utils.is_empty_report(data):
            return errors.error_no_usage_available()

        self._override_render()

        return adapter.generate_output(
            request=self.request,
            fmt=self.request.GET.get('fmt'),
            report_id=report_id,
            data=data,
            params=cleaned_params,
            exceptions=report_exceptions,
        )
