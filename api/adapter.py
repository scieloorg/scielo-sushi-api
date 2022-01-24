from api import utils, values
from datetime import datetime



def generate_output(request, fmt, report_id, data, params, exceptions):
    if fmt == 'tsv':
        return tsv_report_wrapper(request, report_id, data, params, exceptions)

    return json_report_wrapper(report_id, data, params, exceptions)


def json_report_wrapper(report_id, result_query, params, exceptions):
    if report_id == 'ir_a1':
        return _json_ir_a1(result_query, params, exceptions)

    if report_id == 'cr_j1':
        return _json_cr_j1(result_query, params, exceptions)

    if report_id == 'tr_j1':
        return _json_tr_j1(result_query, params, exceptions)

    if report_id == 'tr_j4':
        return _json_tr_j4(result_query, params, exceptions)


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


def tsv_report_wrapper(request, report_id, result_query, params, exceptions):
    filename = '_'.join(['report', report_id]) + '.tsv'
    request.response.content_disposition = 'attachment;filename=' + filename

    if report_id == 'ir_a1':
        return _tsv_report_ir_a1(result_query, params, exceptions)

    if report_id == 'cr_j1':
        return _tsv_report_cr_j1(result_query, params, exceptions)

    if report_id == 'tr_j1':
        return _tsv_report_tr_j1(result_query, params, exceptions)

    if report_id == 'tr_j4':
        return _tsv_report_tr_j4(result_query, params, exceptions)


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
        ri_key = ri.yearMonth

        if ri_key not in collection2values:
            collection2values[ri_key] = (0, 0)

        if ri.yearMonth not in yms:
            yms.append(ri.yearMonth)

        tir = getattr(ri, 'totalItemRequests')
        uir = getattr(ri, 'uniqueItemRequests')

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
        if year_month not in yms:
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
