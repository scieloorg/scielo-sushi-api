from api.db_calls import REPORT_ID_STATUS_COLUMN_DICT
from api.models import DBSession
from api.sql_declarative import DateStatus
from sqlalchemy import and_


def get_dates_unavailable(begin_date, end_date, collection, report_id):
    status_column = REPORT_ID_STATUS_COLUMN_DICT.get(report_id, '')
    if status_column:
        unavailable_dates = DBSession.query(DateStatus).filter(and_(DateStatus.collection == collection,
                                                                    getattr(DateStatus, status_column) == 0,
                                                                    DateStatus.date.between(begin_date, end_date))).all()
    else:
        return []

    return sorted([d.date.strftime('%Y-%m-%d') for d in unavailable_dates])
