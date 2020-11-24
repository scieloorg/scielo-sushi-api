from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from zope.sqlalchemy import register


Base = automap_base()
engine = create_engine('mysql://bn_matomo@172.18.0.3:3306/bitnami_matomo')
Base.prepare(engine, reflect=True)

Article = Base.classes.counter_article
ArticleFormat = Base.classes.counter_article_format
ArticleLanguage = Base.classes.counter_article_language
ArticleMetric = Base.classes.counter_article_metric
Journal = Base.classes.counter_journal
JournalCollection = Base.classes.counter_journal_collection
Localization = Base.classes.counter_localization

try:
    Report = Base.classes.counter_report
    Member = Base.classes.counter_member
    Institution = Base.classes.counter_institution
    Status = Base.classes.counter_status
    Alert = Base.classes.counter_alert
except AttributeError as e:
    pass

DBSession = Session(engine)
register(DBSession)
