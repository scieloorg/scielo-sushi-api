from api import utils, values
from api.libs import cleaner
from datetime import datetime


def generate_output(request, fmt, report_id, data, params, exceptions):
    if fmt == 'tsv':
        return tsv_report_wrapper(request, report_id, data, params, exceptions)

    return json_report_wrapper(report_id, data, params, exceptions)


def json_report_wrapper(report_id, result_query, params, exceptions):
    if report_id == 'lr_a1':
        return _json_lr_a1(result_query, params, exceptions)

    if report_id == 'ir_a1':
        return _json_ir_a1(result_query, params, exceptions)

    if report_id == 'cr_j1':
        return _json_cr_j1(result_query, params, exceptions)

    if report_id == 'tr_j1':
        return _json_tr_j1(result_query, params, exceptions)

    if report_id == 'tr_j4':
        return _json_tr_j4(result_query, params, exceptions)

    if report_id == 'lr_j1':
        return _json_lr_j1(result_query, params, exceptions)

    if report_id == 'lr_j4':
        return _json_lr_j4(result_query, params, exceptions)

    if report_id == 'gr_j1':
        return _json_gr_j1(result_query, params, exceptions)

    if report_id == 'gr_j4':
        return _json_gr_j4(result_query, params, exceptions)


def mount_json_for_reports(result_query):
    json_results = []

    for rq in result_query:
        j = {
            "Report_Name": rq.name,
            "Report_ID": rq.report_id,
            "Release": rq.release,
            "Report_Description": rq.description,
            "Path": rq.path
        }

        json_results.append(j)

    return json_results


def mount_json_for_status_alert(status, result_query_alert):
    status_alert_result = {
        "Description": status.description,
        "Service_Active": True if status.service_active else False,
        "Registry_URL": status.registry_url,
        "Note": status.note,
        "Alerts": []
    }

    for rqa in result_query_alert:
        if rqa.is_active:
            j = {
                "Date_Time": str(rqa.created),
                "Alert": rqa.description
            }
            status_alert_result["Alerts"].append(j)

    return [status_alert_result]


def mount_json_for_members(result_query_members):
    json_results = []

    for rqm in result_query_members:
        j = {
            "Customer_ID": rqm.member_id,
            "Requestor_ID": rqm.requestor_id,
            "Name": rqm.name,
            "Notes": rqm.notes,
            "Institution_ID": []
        }

        json_results.append(j)

    return json_results


def _json_tr_j1(result_query_reports_tr_j1, params, exceptions):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": params.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": params.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_tr_j1:
        if r.journalID not in report_items:
            report_items[r.journalID] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[r.journalID]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[r.journalID]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(r.beginDate),
                    'End_Date': str(r.endDate)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[r.journalID]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_lr_j1(result_query_reports_lr_j1, params, exceptions):
    begin_date, ed_discard = cleaner.get_start_and_last_days(params.get('begin_date', ''))
    bd_discard, end_date = cleaner.get_start_and_last_days(params.get('end_date', ''))

    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": str(begin_date),
        }, {
            "Name": "End_Date",
            "Value": str(end_date),
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_lr_j1:
        key = (r.journalID, r.articlesLanguage)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Article_Language': r.articlesLanguage,
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        if params['granularity'] == 'monthly':
            begin_date, end_date  = cleaner.get_start_and_last_days(r.yearMonth)

        elif params['granularity'] == 'totals':
            begin_date, ed_discard  = cleaner.get_start_and_last_days(r.beginDate)
            bd_discard, end_date  = cleaner.get_start_and_last_days(r.endDate)

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(begin_date),
                    'End_Date': str(end_date)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_lr_a1(result_query_reports_lr_a1, params, exceptions):
    begin_date, ed_discard = cleaner.get_start_and_last_days(params.get('begin_date', ''))
    bd_discard, end_date = cleaner.get_start_and_last_days(params.get('end_date', ''))

    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": str(begin_date)
        }, {
            "Name": "End_Date",
            "Value": str(end_date)
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    article_scielo_ids = _get_scielo_pids(result_query_reports_lr_a1, 'articlePID')
    
    for r in result_query_reports_lr_a1:
        article_key, article_doi = _get_article_key_and_doi(r, 'articleDOI', 'articlePID')

        key = '-'.join([article_key, r.articleLanguage])

        if key not in report_items:
            report_items[key] = {
                'Item': article_key,
                'Publisher': r.journalPublisher,
                'Publisher_ID': [],
                'Platform': params.get('platform', ''),
                'Authors': '',
                'Publication_Date': '',
                'Article_Language': r.articleLanguage,
                'Article_Version': '',
                'DOI': article_doi,
                'Proprietary_ID': '',
                'Print_ISSN': '',
                'Online_ISSN': '',
                'URI': '',
                'Parent_Title': r.journalTitle,
                'Parent_DOI': '',
                'Parent_Proprietary_ID': '',
                'Parent_Print_ISSN': r.printISSN,
                'Parent_Online_ISSN': r.onlineISSN,
                'Parent_URI': r.journalURI,
                'Parent_Data_Type': 'Journal',
                'Item_ID': article_scielo_ids,
                'Data_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

        if params['granularity'] == 'monthly':
            begin_date, end_date  = cleaner.get_start_and_last_days(r.yearMonth)

        elif params['granularity'] == 'totals':
            begin_date, ed_discard  = cleaner.get_start_and_last_days(r.beginDate)
            bd_discard, end_date  = cleaner.get_start_and_last_days(r.endDate)

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(begin_date),
                    'End_Date': str(end_date)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Parent_Title']]
        
    return json_results


def _json_lr_j4(result_query_reports_lr_j4, params, exceptions):
    begin_date, ed_discard = cleaner.get_start_and_last_days(params.get('begin_date', ''))
    bd_discard, end_date = cleaner.get_start_and_last_days(params.get('end_date', ''))

    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": str(begin_date),
        }, {
            "Name": "End_Date",
            "Value": str(end_date),
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_lr_j4:
        key = (r.journalID, r.articlesLanguage, r.yop)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Article_Language': r.articlesLanguage,
                'Article_YOP': r.yop,
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        if params['granularity'] == 'monthly':
            begin_date, end_date  = cleaner.get_start_and_last_days(r.yearMonth)

        elif params['granularity'] == 'totals':
            begin_date, ed_discard  = cleaner.get_start_and_last_days(r.beginDate)
            bd_discard, end_date  = cleaner.get_start_and_last_days(r.endDate)

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(begin_date),
                    'End_Date': str(end_date)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_tr_j4(result_query_reports_tr_j4, params, exceptions):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": params.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": params.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_tr_j4:
        key = (r.journalID, r.yop)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'YOP': r.yop,
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(r.beginDate),
                    'End_Date': str(r.endDate)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_ir_a1(result_query_reports_ir_a1, params, exceptions):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": params.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": params.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_ir_a1:
        key = '-'.join([r.collection, r.pid])

        if key not in report_items:
            report_items[key] = {
                'Item': r.pid,
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Platform': params.get('platform', ''),
                'Authors': '',
                'Publication_Date': '',
                'Article_Version': '',
                'DOI': '',
                'Proprietary_ID': '',
                'Print_ISSN': '',
                'Online_ISSN': '',
                'URI': '',
                'Parent_Title': r.title,
                'Parent_DOI': '',
                'Parent_Proprietary_ID': '',
                'Parent_Print_ISSN': r.printISSN,
                'Parent_Online_ISSN': r.onlineISSN,
                'Parent_URI': '',
                'Parent_Data_Type': 'Journal',
                'Item_ID': [],
                'Data_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(r.beginDate),
                    'End_Date': str(r.endDate)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Item']]
    return json_results


def _json_cr_j1(result_query_reports_cr_j1, params, exceptions):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": params.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": params.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_cr_j1:
        r_collection_acronym = params.get('collection')
        if r_collection_acronym not in report_items:
            report_items[r_collection_acronym] = {
                'Title': r_collection_acronym,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Data_Type': 'Collection',
                'Section_Type': 'Journal',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(r.beginDate),
                    'End_Date': str(r.endDate)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[r_collection_acronym]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_gr_j1(result_query_reports_gr_j1, params, exceptions):
    begin_date, ed_discard = cleaner.get_start_and_last_days(params.get('begin_date', ''))
    bd_discard, end_date = cleaner.get_start_and_last_days(params.get('end_date', ''))

    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": str(begin_date),
        }, {
            "Name": "End_Date",
            "Value": str(end_date),
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_gr_j1:
        key = (r.journalID, r.countryCode)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Access_Country_Code_': r.countryCode,
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        if params['granularity'] == 'monthly':
            begin_date, end_date  = cleaner.get_start_and_last_days(r.yearMonth)

        elif params['granularity'] == 'totals':
            begin_date, ed_discard  = cleaner.get_start_and_last_days(r.beginDate)
            bd_discard, end_date  = cleaner.get_start_and_last_days(r.endDate)

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(begin_date),
                    'End_Date': str(end_date)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results


def _json_gr_j4(result_query_reports_gr_j4, params, exceptions):
    begin_date, ed_discard = cleaner.get_start_and_last_days(params.get('begin_date', ''))
    bd_discard, end_date = cleaner.get_start_and_last_days(params.get('end_date', ''))

    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": params.get('customer', ''),
            "Report_ID": params.get('report_db_params', {}).report_id,
            "Release": params.get('report_db_params', {}).release,
            "Report_Name": params.get('report_db_params', {}).name,
            "Institution_Name": params.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": params.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": str(begin_date),
        }, {
            "Name": "End_Date",
            "Value": str(end_date),
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": exceptions,
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_gr_j4:
        key = (r.journalID, r.countryCode, r.yop)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': params.get('platform', ''),
                'Publisher': r.publisherName,
                'Publisher_ID': [],
                'Access_Country_Code_': r.countryCode,
                'Article_YOP': r.yop,
                'Data_Type': 'Journal',
                'Section_Type': 'Article',
                'Access_Type': 'Open Access',
                'Access_Method': 'Regular',
                'Performance': []}

            if r.printISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Print_ISSN',
                    "Value": r.printISSN
                })

            if r.onlineISSN:
                report_items[key]['Item_ID'].append({
                    "Type": 'Online_ISSN',
                    "Value": r.onlineISSN
                })

        if params['granularity'] == 'monthly':
            begin_date, end_date  = cleaner.get_start_and_last_days(r.yearMonth)

        elif params['granularity'] == 'totals':
            begin_date, ed_discard  = cleaner.get_start_and_last_days(r.beginDate)
            bd_discard, end_date  = cleaner.get_start_and_last_days(r.endDate)

        for m in ['Total_Item_Requests', 'Unique_Item_Requests']:
            metric_name = m[0].lower() + m[1:].replace('_', '')

            performance_m = {
                'Period': {
                    'Begin_Date': str(begin_date),
                    'End_Date': str(end_date)
                },
                'Instance': {
                    'Metric_Type': m,
                    'Count': str(getattr(r, metric_name))
                }
            }
            report_items[key]['Performance'].append(performance_m)

        json_results['Report_Items'] = [ri for ri in report_items.values() if ri['Title']]
    return json_results



def tsv_report_wrapper(request, report_id, result_query, params, exceptions):
    filename = '_'.join(['report', report_id]) + '.tsv'
    request.response.content_disposition = 'attachment;filename=' + filename

    if report_id == 'lr_a1':
        return _tsv_report_lr_a1(result_query, params, exceptions)

    if report_id == 'ir_a1':
        return _tsv_report_ir_a1(result_query, params, exceptions)

    if report_id == 'cr_j1':
        return _tsv_report_cr_j1(result_query, params, exceptions)

    if report_id == 'tr_j1':
        return _tsv_report_tr_j1(result_query, params, exceptions)

    if report_id == 'tr_j4':
        return _tsv_report_tr_j4(result_query, params, exceptions)

    if report_id == 'lr_j1':
        return _tsv_report_lr_j1(result_query, params, exceptions)

    if report_id == 'lr_j4':
        return _tsv_report_lr_j4(result_query, params, exceptions)

    if report_id == 'gr_j1':
        return _tsv_report_gr_j1(result_query, params, exceptions)

    if report_id == 'gr_j4':
        return _tsv_report_gr_j4(result_query, params, exceptions)


def _tsv_header(params, exceptions, data_type='Journal'):
    headers = {}
    for h in values.TSV_REPORT_DEFAULT_HEADERS:
        headers[h] = ''

    headers['Report_Name'] = params.get('report_db_params', {}).name
    headers['Report_ID'] = params.get('report_db_params', {}).report_id
    headers['Release'] = str(params.get('report_db_params', {}).release)
    headers['Metric_Types'] = 'Total Item Requests; Unique Item Requests'
    headers['Report_Filters'] = f'Data_Type={data_type}; Access_Type=Controlled; Access_Method=Regular'
    headers['Exceptions'] = utils.format_error_messages(exceptions)
    headers['Created'] = datetime.now().isoformat()
    headers['Created_By'] = 'Scientific Electronic Library Online SUSHI API'

    bd = params.get('begin_date', '')
    ed = params.get('end_date', '')
    headers['Reporting_Period'] = f'Begin_Date={bd}; End_Date={ed}'

    return headers


def _tsv_report_cr_j1(result_query, params, exceptions):
    result = {'headers': _tsv_header(params, exceptions, data_type='Collection')}

    collection2values = {'Reporting_Period_Total': (0, 0)}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if params['granularity'] == 'monthly':
            ri_key = ri.yearMonth

            if ri_key not in collection2values:
                collection2values[ri_key] = (0, 0)

            if ri.yearMonth not in yms:
                yms.append(ri.yearMonth)

            collection2values[ri_key] = (tir, uir)

        collection2values['Reporting_Period_Total'] = tuple(map(sum, zip(collection2values['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_DEFAULT_ROWS + yms)

    for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
        line = [
            params.get('platform'),
            '',
            '',
            'SciELO SUSHI API',
            '',
            '',
            '',
            '',
            '',
            metric_name
        ]

        for ym in yms:
            ym_v = str(collection2values.get(ym, (0, 0))[j])
            line.append(ym_v)

        output['rows'].append(line)

    return output


def _tsv_report_lr_a1(result_query, params, exceptions):
    begin_date, bd_discard  = cleaner.get_start_and_last_days(params['begin_date'])
    ed_discard, end_date  = cleaner.get_start_and_last_days(params['end_date'])

    params['begin_date'] = begin_date
    params['end_date'] = end_date

    result = {'headers': _tsv_header(params, exceptions)}

    article2values = {}
    article2description = {}
    article_scielo_pids = _get_scielo_pids(result_query, 'articlePID')    
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        if params.get('api', 'v1') == 'v2':
            article_key = (ri.articleDOI, ri.articleLanguage)
            article_description = (ri.printISSN, ri.onlineISSN, ri.journalTitle, ri.journalURI, ri.journalPublisher, ri.articleCollection, article_scielo_pids, ri.articleLanguage, ri.articleDOI)
        else:
            article_key = (ri.articlePID, ri.articleLanguage)
            article_description = (ri.printISSN, ri.onlineISSN, ri.journalTitle, ri.journalURI, ri.journalPublisher, ri.articleCollection, ri.articlePID, ri.articleLanguage, '')

        article2description[article_key] = article_description

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if article_key not in article2values:
            article2values[article_key] = {'Reporting_Period_Total': (0, 0)}

        if params['granularity'] == 'monthly':
            year_month = cleaner.handle_str_date(ri.yearMonth, str_format=False).strftime('%b-%Y')
            if year_month not in yms:
                yms.append(year_month)

            if year_month not in article2values[article_key]:
                article2values[article_key][year_month] = 0

            article2values[article_key][year_month] = (tir, uir)

        article2values[article_key]['Reporting_Period_Total'] = tuple(map(sum, zip(article2values[article_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_LR_A1_ROWS + yms)

    for i in article2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[0],
                article2description[i][4],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[1],
                '',
                article2description[i][8],
                '',
                '',
                '',
                '',
                article2description[i][2],
                '',
                '',
                '',
                '',
                article2description[i][0],
                article2description[i][1],
                article2description[i][3],
                '',
                metric_name
            ]

            for ym in yms:
                ym_v = str(article2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_ir_a1(result_query, params, exceptions):
    result = {'headers': _tsv_header(params, exceptions, data_type='Article')}

    article2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_id = ri.onlineISSN or ri.printISSN or ri.journalID
        article_key = (journal_id, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.pid, ri.yop)

        if article_key not in article2values:
            article2values[article_key] = {'Reporting_Period_Total': (0, 0)}

        year_month = ri.beginDate.strftime('%b-%Y')
        if year_month not in yms and params['granularity'] == 'monthly':
            yms.append(year_month)
        if year_month not in article2values[article_key]:
            article2values[article_key][year_month] = 0

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        article2values[article_key][year_month] = (tir, uir)
        article2values[article_key]['Reporting_Period_Total'] = tuple(map(sum, zip(article2values[article_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_IR_ROWS + yms)

    for i in article2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[6],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                i[7],
                '',
                '',
                '',
                i[3],
                i[4],
                '',
                i[1],
                '',
                '',
                '',
                '',
                '',
                '',
                i[5],
                '',
                metric_name
            ]

            for ym in yms:
                ym_v = str(article2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_tr_j1(result_query, params, exceptions):
    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri)

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        year_month = ri.beginDate.strftime('%b-%Y')
        if year_month not in yms and params['granularity'] == 'monthly':
            yms.append(year_month)
        if year_month not in journal2values[journal_key]:
            journal2values[journal_key][year_month] = 0

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        journal2values[journal_key][year_month] = (tir, uir)
        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_DEFAULT_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_tr_j4(result_query, params, exceptions):
    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.yop)

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        year_month = ri.beginDate.strftime('%b-%Y')
        if year_month not in yms and params['granularity'] == 'monthly':
            yms.append(year_month)
        if year_month not in journal2values[journal_key]:
            journal2values[journal_key][year_month] = 0

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        journal2values[journal_key][year_month] = (tir, uir)
        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_TR_J4_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                i[6],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_lr_j1(result_query, params, exceptions):
    begin_date, bd_discard  = cleaner.get_start_and_last_days(params['begin_date'])
    ed_discard, end_date  = cleaner.get_start_and_last_days(params['end_date'])

    params['begin_date'] = begin_date
    params['end_date'] = end_date

    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.articlesLanguage)

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        if params['granularity'] == 'monthly':
            year_month = cleaner.handle_str_date(ri.yearMonth, str_format=False).strftime('%b-%Y')
            if year_month not in yms:
                yms.append(year_month)

            if year_month not in journal2values[journal_key]:
                journal2values[journal_key][year_month] = 0

            journal2values[journal_key][year_month] = (tir, uir)

        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_LR_J1_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                i[6],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_lr_j4(result_query, params, exceptions):
    begin_date, bd_discard  = cleaner.get_start_and_last_days(params['begin_date'])
    ed_discard, end_date  = cleaner.get_start_and_last_days(params['end_date'])

    params['begin_date'] = begin_date
    params['end_date'] = end_date

    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.articlesLanguage, ri.yop)

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        if params['granularity'] == 'monthly':
            year_month = cleaner.handle_str_date(ri.yearMonth, str_format=False).strftime('%b-%Y')
            if year_month not in yms:
                yms.append(year_month)

            if year_month not in journal2values[journal_key]:
                journal2values[journal_key][year_month] = 0

            journal2values[journal_key][year_month] = (tir, uir)

        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_LR_J4_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                i[6],
                i[7],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_gr_j1(result_query, params, exceptions):
    begin_date, bd_discard  = cleaner.get_start_and_last_days(params['begin_date'])
    ed_discard, end_date  = cleaner.get_start_and_last_days(params['end_date'])

    params['begin_date'] = begin_date
    params['end_date'] = end_date

    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.countryCode)

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        if params['granularity'] == 'monthly':
            year_month = cleaner.handle_str_date(ri.yearMonth, str_format=False).strftime('%b-%Y')
            if year_month not in yms:
                yms.append(year_month)

            if year_month not in journal2values[journal_key]:
                journal2values[journal_key][year_month] = 0

            journal2values[journal_key][year_month] = (tir, uir)

        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_GR_J1_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                i[6],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _tsv_report_gr_j4(result_query, params, exceptions):
    begin_date, bd_discard  = cleaner.get_start_and_last_days(params['begin_date'])
    ed_discard, end_date  = cleaner.get_start_and_last_days(params['end_date'])

    params['begin_date'] = begin_date
    params['end_date'] = end_date

    result = {'headers': _tsv_header(params, exceptions)}

    journal2values = {}
    yms = ['Reporting_Period_Total']

    for ri in result_query:
        journal_key = (ri.journalID, ri.title, ri.publisherName, ri.printISSN, ri.onlineISSN, ri.uri, ri.countryCode, ri.yop)

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

        if journal_key not in journal2values:
            journal2values[journal_key] = {'Reporting_Period_Total': (0, 0)}

        if params['granularity'] == 'monthly':
            year_month = cleaner.handle_str_date(ri.yearMonth, str_format=False).strftime('%b-%Y')
            if year_month not in yms:
                yms.append(year_month)

            if year_month not in journal2values[journal_key]:
                journal2values[journal_key][year_month] = 0

            journal2values[journal_key][year_month] = (tir, uir)

        journal2values[journal_key]['Reporting_Period_Total'] = tuple(map(sum, zip(journal2values[journal_key]['Reporting_Period_Total'], (tir, uir))))

    output = {'rows': []}
    for k in values.TSV_REPORT_DEFAULT_HEADERS:
        output['rows'].append([k, result['headers'][k]])

    output['rows'].append(values.TSV_REPORT_GR_J4_ROWS + yms)

    for i in journal2values:
        for j, metric_name in enumerate(['Total_Item_Requests', 'Unique_Item_Requests']):
            line = [
                i[1],
                i[2],
                '',
                'SciELO SUSHI API',
                '',
                '',
                i[3],
                i[4],
                i[5],
                i[6],
                i[7],
                metric_name
            ]

            for ym in yms:
                ym_v = str(journal2values[i].get(ym, (0, 0))[j])
                line.append(ym_v)

            output['rows'].append(line)

    return output


def _get_scielo_pids(result_query, field_pid_name):
    article_scielo_ids = set()

    for r in result_query:
        str_pids = getattr(r, field_pid_name) or ''
        els_pids = str_pids.split(',')
        
        article_scielo_ids = article_scielo_ids.union(set(els_pids))
    return sorted(article_scielo_ids)


def _get_article_key_and_doi(item, field_doi_name, field_pid_name):
    article_doi = getattr(item, field_doi_name, '')
    article_key = getattr(item, field_pid_name)

    return article_key, article_doi
