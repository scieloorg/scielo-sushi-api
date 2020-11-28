from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
global db_session


def get_counter_tables(engine):
    Base.prepare(engine, reflect=True)

    counter_tables_names = ['counter_article',
                            'counter_article_format',
                            'counter_article_metric',
                            'counter_journal',
                            'counter_journal_collection',
                            'counter_localization',
                            'counter_report',
                            'counter_member',
                            'counter_institution',
                            'counter_status',
                            'counter_alert']

    counter_tables = {}

    for ctn in counter_tables_names:
        table = getattr(Base.classes, ctn)
        table_formatted_name = table.__table__.name
        counter_tables[table_formatted_name] = table

    global db_session
    db_session = Session(bind=engine)

    return counter_tables
