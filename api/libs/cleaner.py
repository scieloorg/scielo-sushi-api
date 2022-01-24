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


def clean_collection_acronym(collection):
    if not collection or collection not in values.COLLECTION_ACRONYM_TO_COLLECTION_NAME.keys():
        return 'scl'
    return collection


def clean_collection_name(collection):
    collection_name = values.COLLECTION_ACRONYM_TO_COLLECTION_NAME.get(collection)
    if not collection_name:
        collection_name = values.COLLECTION_ACRONYM_TO_COLLECTION_NAME['scl']
    return collection_name

