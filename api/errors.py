def error_invalid_date_arguments():
    return {
        'Code': 3020,
        'Severity': 'error',
        'Message': 'Invalid Date Arguments',
    }


def error_required_filter_missing(data):
    return {
        'Code': 3070,
        'Severity': 'error',
        'Message': 'A required filter was not included in the request',
        'Data': data
    }

def error_report_not_supported():
    return {
        'Code': 3000,
        'Severity': 'error',
        'Message': 'Report Not Supported',
    }


def error_no_usage_available():
    return {
        'Code': 3030,
        'Severity': 'error',
        'Message': 'No Usage Available for Requested Dates',
    }


def error_usage_not_ready(severity, not_ready_dates):
    return {
        'Code': 3031,
        'Severity': severity,
        'Message': 'Usage Not Ready for Requested Dates',
        'Data': not_ready_dates
    }


def error_usage_no_longer_available():
    # TODO: os dados existentes devem ser retornados, porém, no json deve ser incluída uma exceção
    return {
        'Code': 3032,
        'Severity': 'warning',
        'Message': 'Usage Not Ready for Requested Dates',
    }


def error_partial_data():
    return {
        'Code': 3040,
        'Severity': 'warning',
        'Message': 'Partial Data Returned',
    }


def error_invalid_report_filter_value(data, severity):
    return {
        'Code': 3060,
        'Severity': severity,
        'Message': 'Request contained one or more filter values that are not supported by the server',
        'Data': data
    }


def error_invalid_report_attribute_value(data, severity):
    return {
        'Code': 3062,
        'Severity': severity,
        'Message': 'Request contained one or more attribute values that are not supported by the server',
        'Data': data
    }


def error_parameter_not_recognized_in_this_context(data):
    return {
        'Code': 3050,
        'Severity': 'warning',
        'Message': 'Parameter Not Recognized in this Context',
        'Data': data,
    }
