import calendar

from api import values
from datetime import datetime


def clean_field(field):
    els = []
    for c in field:
        if c not in ('\"', '\'', '\n', '\t', ' '):
            els.append(c)
    return ''.join(els)


def clean_api(api):
    if api not in ('v2',):
        return 'v1'
    return api
