def error_invalid_date_arguments(date):
    return {
        'Code': 3020,
        'Severity': 'error',
        'Message': 'Invalid Date Arguments',
    }


def error_no_usage_avalailable(date):
    return {
        'Code': 3030,
        'Severity': ['error', 'warning'],
        'Message': 'No Usage Available for Requested Dates',
    }


def error_usage_not_ready(date):
    # TODO: os dados existentes devem ser retornados, porém, no json deve ser incluída uma exceção
    return {
        'Code': 3031,
        'Severity': ['error', 'warning'],
        'Message': 'Usage Not Ready for Requested Dates',
    }


def error_usage_no_longer_available(date):
    # TODO: os dados existentes devem ser retornados, porém, no json deve ser incluída uma exceção
    return {
        'Code': 3032,
        'Severity': 'warning',
        'Message': 'Usage Not Ready for Requested Dates',
    }


def error_partial_data(date):
    return {
        'Code': 3050,
        'Severity': 'warning',
        'Message': 'Partial Data Returned',
    }
