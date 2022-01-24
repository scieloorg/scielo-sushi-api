import re

from api import errors, values
from api.libs import cleaner


def is_valid_date_range(begin_date, end_date):
    if end_date >= begin_date:
        return True
    return False
