from datetime import datetime


def wrapper_mount_json_for_report(report_id, result_query, attrs):
    if report_id == 'ir_a1':
        return mount_json_for_reports_ir_a1(result_query, attrs)
    if report_id == 'tr_j1':
        return mount_json_for_reports_tr_j1(result_query, attrs)
    if report_id == 'tr_j4':
        return mount_json_for_reports_tr_j4(result_query, attrs)


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


def mount_json_for_reports_tr_j1(result_query_reports_tr_j1, attrs):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": attrs.get('customer', ''),
            "Report_ID": attrs.get('report_data', {}).report_id,
            "Release": attrs.get('report_data', {}).release,
            "Report_Name": attrs.get('report_data', {}).name,
            "Institution_Name": attrs.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": attrs.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": attrs.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": attrs.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": [],
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_tr_j1:
        if r.journalID not in report_items:
            report_items[r.journalID] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': attrs.get('platform', ''),
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

        json_results['Report_Items'] = [ri for ri in report_items.values()]
    return json_results


def mount_json_for_reports_tr_j4(result_query_reports_tr_j4, attrs):
    json_results = {
        "Report_Header": {
            "Created": datetime.now().isoformat(),
            "Created_By": "Scientific Electronic Library Online SUSHI API",
            "Customer_ID": attrs.get('customer', ''),
            "Report_ID": attrs.get('report_data', {}).report_id,
            "Release": attrs.get('report_data', {}).release,
            "Report_Name": attrs.get('report_data', {}).name,
            "Institution_Name": attrs.get('institution_name', ''),
            "Institution_ID": [{
                "Type": "ISNI",
                "Value": attrs.get('institution_id', '')
            }],
        },
        "Report_Filters": [{
            "Name": "Begin_Date",
            "Value": attrs.get('begin_date', '')
        }, {
            "Name": "End_Date",
            "Value": attrs.get('end_date', '')
        }],
        "Report_Attributes": [{
            "Name": "Attributes_To_Show",
            "Value": "Data_Type|Access_Method"
        }],
        "Exceptions": [],
        "Report_Items": []
    }

    report_items = {}

    for r in result_query_reports_tr_j4:
        key = (r.journalID, r.yop)
        if key not in report_items:
            report_items[key] = {
                'Title': r.title,
                'Item_ID': [],
                'Platform': attrs.get('platform', ''),
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

        json_results['Report_Items'] = [ri for ri in report_items.values()]
    return json_results
