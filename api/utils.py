import calendar
from datetime import datetime


def get_counter_table(request, name):
    return request.registry.settings.get('counter_tables').get(name)


def handle_str_date(str_date, is_end_date=False):
    handled_date = None

    try:
        if len(str_date) == len('YYYY-MM'):
            date = datetime.strptime(str_date, '%Y-%m')

            if not is_end_date:
                handled_date = date
            else:
                month_last_day = calendar.monthrange(date.year, date.month)[-1]
                handled_date = date.replace(day=month_last_day)

        elif len(str_date) == len('YYYY-MM-DD'):
            handled_date = datetime.strptime(str_date, '%Y-%m-%d')

        handled_date_str = handled_date.strftime('%Y-%m-%d')
        return handled_date_str

    except:
        raise ValueError('Invalid date', str_date)
