from api import errors, values
from api.libs import db


def check_exceptions(report_id, params_names, cleaned_params):
    exceptions = []

    pns = [p for p in params_names]

    invalid_filters = check_parameters(pns)
    if len(invalid_filters) > 0:
        exceptions.append(errors.error_invalid_report_filter_value(invalid_filters, severity='warning'))

    invalid_params_for_report = check_report_and_parameters_compatibility(report_id, pns)
    if len(invalid_params_for_report) > 0:
        exceptions.append(errors.error_parameter_not_recognized_in_this_context(invalid_params_for_report))

        for i in invalid_params_for_report:
            del cleaned_params[i]

    not_ready_dates = db.get_dates_not_ready(cleaned_params['begin_date'], cleaned_params['end_date'], cleaned_params['collection'], report_id)
    if len(not_ready_dates) > 0:
        exceptions.append(errors.error_usage_not_ready('warning', not_ready_dates))

    return exceptions


def check_report_and_parameters_compatibility(report_id, params):
    invalid_params = []

    if report_id == 'cr_j1':
        for i in params:
            if i in ['issn', 'pid']:
                invalid_params.append(i)

    if report_id in ['tr_j1', 'tr_j4']:
        for i in params:
            if i in ['pid']:
                invalid_params.append(i)

    return invalid_params


def check_parameters(params):
    invalid_parameters = []

    for p in params:
        if p not in values.URI_SUPPORTED_PARAMETERS:
            invalid_parameters.append(p)

    return invalid_parameters


def extract_parameters(request, params_list):
    params = {}

    for p in params_list:
        if p in request.params:
            params[p] = request.params.get(p)

    return params


def extract_report_data(result_proxy):
    if result_proxy:
        return [i for i in result_proxy]


def get_granularity_and_mode(params):
    granularity = params.get('granularity', 'totals')

    if params.get('issn', '') != '':
        mode = 'issn'
    elif params.get('pid', '') != '':
        mode = 'pid'
    else:
        mode = 'global'

    return granularity, mode


def is_empty_report(report_items):
    if len(report_items) == 0:
        return True

    for item in report_items:
        if item.totalItemRequests > 0:
            return False

        if item.uniqueItemRequests > 0:
            return False

    return True


def format_error_messages(exceptions: list):
    output = []

    for e in exceptions:
        e_msg = e.get('Message')
        e_val = e.get('Data')

        if isinstance(e_val, list):
            e_val = ','.join(e_val)
        output.append('='.join([e_msg, e_val]))

    return ';'.join(output)


def set_collection_extra(report_id, attrs):
    if report_id in ('cr_j1', 'lr_j1'):
        if attrs['collection'] == 'scl':
            attrs.update({'collection_extra': 'nbr'})

        if attrs['collection'] == 'nbr':
            attrs.update({'collection_extra': 'scl'})

    else:
        attrs.update({'collection_extra': ''})


def wrapper_call_report(report_id, params):
    granularity, mode = get_granularity_and_mode(params)

    if params['api'] == 'v2':
        procedure_name, params_names = values.V2_GRANULARITY_MODE_REPORT_TO_PROCEDURE_AND_PARAMETERS.get(granularity, {}).get(mode, {}).get(report_id, ('', []))
    else:
        procedure_name, params_names = values.GRANULARITY_MODE_REPORT_TO_PROCEDURE_AND_PARAMETERS.get(granularity, {}).get(mode, {}).get(report_id, ('', []))

    if report_id in ('lr_j1',):
        params['begin_date'] = cleaner.handle_str_date(params['begin_date'], year_month_only=True)
        params['end_date'] = cleaner.handle_str_date(params['end_date'], year_month_only=True)

    if procedure_name and params_names:
        procedure_params = []

        for p in params_names:
            p_value = params.get(p)

            if p_value:
                procedure_params.append(p_value)

            if not p_value and p == 'collection_extra':
                procedure_params.append('')

        return procedure_name % tuple(procedure_params)
