from sqlalchemy import Column, ForeignKey, BOOLEAN
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Institution(Base):
    __tablename__ = 'counter_institution'

    institution_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    type = Column(VARCHAR(20))
    value = Column(VARCHAR(255))


class Member(Base):
    __tablename__ = 'counter_member'

    member_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    requestor_id = Column(INTEGER(unsigned=True))
    name = Column(VARCHAR(255), nullable=False)
    notes = Column(VARCHAR(1024), nullable=True)

    fk_institution_id = Column(INTEGER(unsigned=True), ForeignKey('counter_institution.institution_id',
                                                                  name='fk_institution_id'))


class Report(Base):
    __tablename__ = 'counter_report'

    report_id = Column(VARCHAR(5), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    release = Column(INTEGER(unsigned=True), nullable=False)
    description = Column(VARCHAR(1024), nullable=False)
    path = Column(VARCHAR(255), nullable=False)


class Status(Base):
    __tablename__ = 'counter_status'

    status_id = Column(INTEGER(unsigned=True), primary_key=True)
    description = Column(VARCHAR(1024))
    service_active = Column(BOOLEAN, nullable=False)
    registry_url = Column(VARCHAR(255))
    note = Column(VARCHAR(1024))


class Alert(Base):
    __tablename__ = 'counter_alert'

    alert_id = Column(INTEGER(unsigned=True), primary_key=True)
    created = Column(DATETIME, nullable=False)
    description = Column(VARCHAR(1024))
    is_active = Column(BOOLEAN, nullable=False)
