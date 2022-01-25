from api import values
from api.models.sql_declarative import Alert, DateStatus, Member, Report, Status
from api.models.sql_automap import DBSession
from sqlalchemy import and_


def call_procedure(query):
    if query:
        return DBSession.execute(query)


def get_status():
    return DBSession.query(Status).order_by(Status.status_id.desc()).first()


def get_alert(is_active):
    return DBSession.query(Alert).filter(Alert.is_active == is_active).all()


def get_reports():
    return DBSession.query(Report).all()


def get_members():
    return DBSession.query(Member).all()


def get_report_by_id(report_id):
    return DBSession.query(Report).filter_by(report_id=report_id).one()


def get_dates_not_ready(begin_date, end_date, collection, report_id):
    status_column = values.REPORT_ID_TO_COLUMN_STATUS.get(report_id, '')
    if status_column:
        not_read_dates = DBSession.query(DateStatus).filter(and_(DateStatus.collection == collection,
                                                                 getattr(DateStatus, status_column) == 0,
                                                                 DateStatus.date.between(begin_date, end_date))).all()
    else:
        return []

    return sorted([d.date.strftime('%Y-%m-%d') for d in not_read_dates])