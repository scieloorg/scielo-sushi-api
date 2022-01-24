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

