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


def clean_granularity(granularity):
    if granularity not in ('monthly', 'totals'):
        return 'monthly'
    return granularity


def clean_parameters(required_params, optional_params):
    cleaned_collection_acronym = clean_collection_acronym(optional_params.get('collection'))

    cleaned_params = {
        'customer': clean_field(required_params.get('customer', '')),
        'issn': clean_field(optional_params.get('issn', '')),
        'pid': clean_field(optional_params.get('pid', '')),
        'granularity': clean_granularity('granularity'),
        'institution': clean_field(optional_params.get('institution', '')),
        'institution_id': clean_field(optional_params.get('institution_id', '')),
        'begin_date': required_params.get('begin_date'),
        'end_date': required_params.get('end_date'),
        'platform': 'Scientific Electronic Library Online - ' + clean_collection_name(cleaned_collection_acronym),
        'report_data': '',
        'collection':  cleaned_collection_acronym,
        'api': clean_api(optional_params.get('api', '')),
    }

    return cleaned_params

