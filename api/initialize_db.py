import json
import os
import sys
import transaction

from datetime import datetime
from os import environ
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from .sql_declarative import Base, Report, Status, Alert


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s config.ini")' % (cmd, cmd))


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    sqlalchemy_url_value = environ.get('MARIADB_STRING_CONNECTION', 'mysql://root:pass@localhost:port/database')
    settings.update({'sqlalchemy.url': sqlalchemy_url_value})

    application_url_value = environ.get('APPLICATION_URL', 'http://127.0.0.1:6543')
    settings.update({'application.url': application_url_value})

    DBSession = scoped_session(sessionmaker())
    register(DBSession)

    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)

    file_counter_report = os.path.join(os.getcwd(), '/app/static/counter_report.json')
    with transaction.manager:
        with open(file_counter_report) as f:
            application_url = settings.get('application.url')
            array = json.load(f)

            for dic in array:
                for v in dic.values():

                    report = Report(report_id=v['Report_ID'],
                                    name=v['Report_Name'],
                                    release=v['Release'],
                                    description=v['Report_Description'],
                                    path=application_url + v['Path'])

                    DBSession.add(report)

        status = Status()
        status.description = "COUNTER Usage Reports for SciELO platform."
        status.note = ""
        status.registry_url = application_url + '/registration'
        status.service_active = True
        DBSession.add(status)

        alert = Alert()
        alert.description = "Reports DR, DR_D1, DR_D2, PR, PR_1, TR_J2 and TR_J3 are currently unavailable."
        alert.created = datetime.now().isoformat()
        alert.is_active = True
        DBSession.add(alert)
