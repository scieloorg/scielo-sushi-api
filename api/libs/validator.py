import re

from api import errors, values
from api.libs import cleaner


def is_valid_date_range(begin_date, end_date):
    if end_date >= begin_date:
        return True
    return False


def is_valid_issn(issn):
    if re.match(pattern=values.REGEX_ISSN, string=issn):
        return True
    return False


def is_valid_date_format(date):
    if re.match(pattern=values.REGEX_DATE_FORMAT, string=date):
        return True
    return False


def is_valid_pid(pid):
    if pid.startswith('S'):
        if len(pid) == 23:
            return True
        else:
            return False
    return True


def validate_date_format(param_date, name):
    if not param_date:
        return errors.error_required_filter_missing(name)

    if not is_valid_date_format(param_date):
        return errors.error_invalid_date_arguments()

    try:
        if name == 'end_date':
            return cleaner.handle_str_date(param_date, is_end_date=True)
        else:
            return cleaner.handle_str_date(param_date)

    except ValueError or TypeError or AttributeError as e:
        if 'unconverted data' or 'argument of type' or 'parameter date' in e:
            return errors.error_invalid_date_arguments()

