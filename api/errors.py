def error_invalid_date_arguments():
    return {
        'Code': 3020,
        'Severity': 'error',
        'Message': 'Invalid Date Arguments',
    }


def error_no_usage_available():
    return {
        'Code': 3030,
        'Severity': 'error',
        'Message': 'No Usage Available for Requested Dates',
    }


def error_usage_not_ready():
    # TODO: os dados existentes devem ser retornados, porém, no json deve ser incluída uma exceção
    return {
        'Code': 3031,
        'Severity': ['error', 'warning'],
        'Message': 'Usage Not Ready for Requested Dates',
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
        'Code': 3050,
        'Severity': 'warning',
        'Message': 'Partial Data Returned',
    }


def error_invalid_report_filter_value(data):
    return {
        'Code': 3060,
        'Severity': ['warning', 'error'],
        'Message': 'Request contained one or more filter values that are not supported by the server',
        'Data': data
    }
