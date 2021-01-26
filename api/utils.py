import calendar
import re

from datetime import datetime


REGEX_DATE_FORMAT = r'\d{4}\-\d{2}($|\-\d{2}$)'
REGEX_ISSN = r'[0-9]{4}-[0-9]{3}[0-9xX]'


def get_counter_table(request, name):
    return request.registry.settings.get('counter_tables').get(name)


def handle_str_date(str_date, is_end_date=False):
    handled_date = None

    if len(str_date) == len('YYYY-MM'):
        date = datetime.strptime(str_date, '%Y-%m')

        if not is_end_date:
            handled_date = date
        else:
            month_last_day = calendar.monthrange(date.year, date.month)[-1]
            handled_date = date.replace(day=month_last_day)

    elif len(str_date) == len('YYYY-MM-DD'):
        handled_date = datetime.strptime(str_date, '%Y-%m-%d')

    return handled_date.strftime('%Y-%m-%d')


def is_valid_date_range(begin_date, end_date):
    if end_date >= begin_date:
        return True
    return False


def is_valid_issn(issn):
    if re.match(pattern=REGEX_ISSN, string=issn):
        return True
    return False


def is_valid_date_format(date):
    if re.match(pattern=REGEX_DATE_FORMAT, string=date):
        return True
    return False
