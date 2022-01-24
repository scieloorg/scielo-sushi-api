from api import values
from api.models.sql_declarative import Alert, DateStatus, Member, Report, Status
from api.models.sql_automap import DBSession
from sqlalchemy import and_


def call_procedure(query):
    if query:
        return DBSession.execute(query)
def get_dates_not_ready(begin_date, end_date, collection, report_id):
    status_column = values.REPORT_ID_TO_COLUMN_STATUS.get(report_id, '')
    if status_column:
        not_read_dates = DBSession.query(DateStatus).filter(and_(DateStatus.collection == collection,
                                                                 getattr(DateStatus, status_column) == 0,
                                                                 DateStatus.date.between(begin_date, end_date))).all()
    else:
        return []

    return sorted([d.date.strftime('%Y-%m-%d') for d in not_read_dates])