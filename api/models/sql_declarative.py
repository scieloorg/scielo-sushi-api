from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, DATE, DATETIME, DECIMAL, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class LogFile(Base):
    __tablename__ = 'control_log_file'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    full_path = Column(VARCHAR(255), nullable=False, unique=True)
    name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False)
    size = Column(BIGINT, nullable=False)
    server = Column(VARCHAR(255), nullable=False)
    date = Column(DATE, nullable=False, index=True)
    status = Column(INTEGER, default=0)
    collection = Column(VARCHAR(3), nullable=False)


class LogFileSummary(Base):
    __tablename__ = 'control_log_file_summary'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    idlogfile = Column(INTEGER(unsigned=True), ForeignKey('control_log_file.id', name='idlogfile'))

    total_lines = Column(INTEGER, nullable=False)
    lines_parsed = Column(INTEGER)

    total_imported_lines = Column(INTEGER)
    total_ignored_lines = Column(INTEGER)
    sum_imported_ignored_lines = Column(INTEGER)

    ignored_lines_filtered = Column(INTEGER)
    ignored_lines_http_errors = Column(INTEGER)
    ignored_lines_http_redirects = Column(INTEGER)
    ignored_lines_invalid = Column(INTEGER)
    ignored_lines_bots = Column(INTEGER)
    ignored_lines_static_resources = Column(INTEGER)

    total_time = Column(INTEGER)
    status = Column(INTEGER)


class Journal(Base):
    __tablename__ = 'counter_journal'

    __table_args__ = (UniqueConstraint('print_issn', 'online_issn', 'pid_issn', name='uni_issn'),)
    __table_args__ += (Index('idx_print_issn', 'print_issn'),)
    __table_args__ += (Index('idx_online_issn', 'online_issn'),)
    __table_args__ += (Index('idx_pid_issn', 'pid_issn'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    print_issn = Column(VARCHAR(9), nullable=False)
    online_issn = Column(VARCHAR(9), nullable=False)
    pid_issn = Column(VARCHAR(9), nullable=False)


class JournalCollection(Base):
    __tablename__ = 'counter_journal_collection'
    __table_args__ = (UniqueConstraint('collection', 'idjournal_jc', name='uni_col_jou'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection = Column(VARCHAR(3), nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    uri = Column(VARCHAR(255))
    publisher_name = Column(VARCHAR(255))
    idjournal_jc = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_jc'))


class ArticleLanguage(Base):
    __tablename__ = 'counter_article_language'
    __table_args__ = (UniqueConstraint('language', name='uni_lang'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    language = Column(VARCHAR(10), nullable=False)


class ArticleFormat(Base):
    __tablename__ = 'counter_article_format'
    __table_args__ = (UniqueConstraint('format', name='uni_fmt'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    format = Column(VARCHAR(10), nullable=False)


class Article(Base):
    __tablename__ = 'counter_article'
    __table_args__ = (UniqueConstraint('collection', 'pid', name='uni_col_pid'),)
    __table_args__ += (Index('idx_col_pid_jou_yop', 'collection', 'pid', 'idjournal_a', 'yop'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection = Column(VARCHAR(3), nullable=False)
    pid = Column(VARCHAR(128), nullable=False)
    yop = Column(INTEGER(4))

    idjournal_a = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_a'))
    journal = relationship(Journal)


class ArticleMetric(Base):
    __tablename__ = 'counter_article_metric'
    __table_args__ = (UniqueConstraint('year_month_day', 'idarticle', 'idformat', 'idlanguage', 'idlocalization', name='uni_date_art_all'),)
    __table_args__ += (Index('idx_date_art_all', 'year_month_day', 'idarticle', 'idformat', 'idlanguage', 'idlocalization'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    idarticle = Column(INTEGER(unsigned=True), ForeignKey('counter_article.id', name='idarticle'))
    article = relationship(Article)

    idformat = Column(INTEGER(unsigned=True), ForeignKey('counter_article_format.id', name='idformat'))
    idlanguage = Column(INTEGER(unsigned=True), ForeignKey('counter_article_language.id', name='idlanguage'))
    idlocalization = Column(INTEGER(unsigned=True), ForeignKey('counter_localization.id', name='idlocalization'))

    year_month_day = Column(DATE, nullable=False)
    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class Localization(Base):
    __tablename__ = 'counter_localization'
    __table_args__ = (UniqueConstraint('latitude', 'longitude', name='uni_loc'),)
    __table_args__ += (Index('idx_loc', 'latitude', 'longitude'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))


class JournalMetric(Base):
    __tablename__ = 'counter_journal_metric'
    __table_args__ = (UniqueConstraint('year_month_day', 'collection', 'idformat_cjm', 'idlanguage_cjm', 'idjournal_cjm', 'yop', name='uni_col_date_all_cjm'),)
    __table_args__ += (Index('idx_col_date_all_cjm', 'collection', 'year_month_day', 'idformat_cjm', 'idlanguage_cjm', 'yop', 'idjournal_cjm'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False)

    idformat_cjm = Column(INTEGER(unsigned=True), ForeignKey('counter_article_format.id', name='idformat_cjm'))
    idlanguage_cjm = Column(INTEGER(unsigned=True), ForeignKey('counter_article_language.id', name='idlanguage_cjm'))
    idjournal_cjm = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_cjm'))

    yop = Column(INTEGER(4))
    year_month_day = Column(DATE, nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class SushiJournalYOPMetric(Base):
    __tablename__ = 'sushi_journal_yop_metric'
    __table_args__ = (UniqueConstraint('year_month_day', 'collection', 'yop', 'idjournal_sjym', name='uni_col_date_yop_jou_sjym'),)
    __table_args__ += (Index('idx_col_date_yop_sjym', 'collection', 'year_month_day', 'yop', 'idjournal_sjym'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False)

    idjournal_sjym = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_sjym'))
    yop = Column(INTEGER(4))
    year_month_day = Column(DATE, nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class SushiJournalMetric(Base):
    __tablename__ = 'sushi_journal_metric'
    __table_args__ = (UniqueConstraint('year_month_day', 'collection', 'idjournal_sjm', name='uni_col_date_jou_sjm'),)
    __table_args__ += (Index('idx_col_date_sjm', 'collection', 'year_month_day', 'idjournal_sjm'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False)

    idjournal_sjm = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_sjm'))
    year_month_day = Column(DATE, nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class SushiArticleMetric(Base):
    __tablename__ = 'sushi_article_metric'
    __table_args__ = (UniqueConstraint('year_month_day', 'idarticle_sam', name='uni_date_art_sam'),)
    __table_args__ += (Index('idx_date_sam', 'year_month_day', 'idarticle_sam'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    idarticle_sam = Column(INTEGER(unsigned=True), ForeignKey('counter_article.id', name='idarticle_sam'))
    year_month_day = Column(DATE, nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


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


class DateStatus(Base):
    __tablename__ = 'control_date_status'
    __table_args__ = (UniqueConstraint('collection', 'date', name='uni_collection_date'), )

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    date = Column(DATE, nullable=False, index=True)
    collection = Column(VARCHAR(3), nullable=False)
    status = Column(INTEGER, default=0)

    status_counter_article_metric = Column(BOOLEAN, default=False)
    status_counter_journal_metric = Column(BOOLEAN, default=False)
    status_sushi_article_metric = Column(BOOLEAN, default=False)
    status_sushi_journal_metric = Column(BOOLEAN, default=False)
    status_sushi_journal_yop_metric = Column(BOOLEAN, default=False)


class AggrStatus(Base):
    __tablename__ = 'aggr_status'
    __table_args__ = (UniqueConstraint('collection', 'date', name='uni_collection_date'), )

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    date = Column(DATE, nullable=False, primary_key=True)

    status_aggr_article_journal_year_month_metric = Column(BOOLEAN, default=False)
    status_aggr_article_language_year_month_metric = Column(BOOLEAN, default=False)
    status_aggr_journal_language_year_month_metric = Column(BOOLEAN, default=False)
    status_aggr_journal_geolocation_year_month_metric = Column(BOOLEAN, default=False)
    status_aggr_journal_language_yop_year_month_metric = Column(BOOLEAN, default=False)
    status_aggr_journal_geolocation_yop_year_month_metric = Column(BOOLEAN, default=False)


class AggrArticleJournalYearMonthMetric(Base):
    __tablename__ = 'aggr_article_journal_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'article_id', 'journal_id', name='uni_col_art_jou_ymm_aajymm'),)
    __table_args__ += (Index('idx_ymaj_id', 'year_month', 'article_id', 'journal_id'),)
    __table_args__ += (Index('idx_yj_id', 'year_month', 'journal_id'),)
    __table_args__ += (Index('idx_j_id', 'journal_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    article_id = Column(INTEGER(unsigned=True), ForeignKey('counter_article.id', name='idarticle_aajymm'))
    journal_id = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_aajymm'))
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class AggrArticleLanguageYearMonthMetric(Base):
    __tablename__ = 'aggr_article_language_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'article_id', 'language_id', name='uni_col_art_lan_ymm_aalymm'),)
    __table_args__ += (Index('idx_ym_id', 'year_month', 'article_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    article_id = Column(INTEGER(unsigned=True), ForeignKey('counter_article.id', name='idarticle_aalymm'))
    language_id = Column(INTEGER(unsigned=True), ForeignKey('counter_article_language.id', name='idlanguage_aalymm'))
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class AggrJournalLanguageYearMonthMetric(Base):
    __tablename__ = 'aggr_journal_language_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'journal_id', 'language_id', name='uni_col_jou_lan_ymm_ajlymm'),)
    __table_args__ += (Index('idx_ym_id', 'year_month', 'journal_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    journal_id = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_ajlymm'))
    language_id = Column(INTEGER(unsigned=True), ForeignKey('counter_article_language.id', name='idlanguage_ajlymm'))
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class AggrJournalGeolocationYearMonthMetric(Base):
    __tablename__ = 'aggr_journal_geolocation_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'journal_id', 'country_code', name='uni_col_jou_geo_ymm_ajgymm'),)
    __table_args__ += (Index('idx_ym_id', 'year_month', 'journal_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    journal_id = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_ajgymm'))
    country_code = Column(VARCHAR(4), nullable=False)
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class AggrJournalLanguageYOPYearMonthMetric(Base):
    __tablename__ = 'aggr_journal_language_yop_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'journal_id', 'language_id', 'yop', name='uni_col_jou_lan_yop_ymm_ajlyymm'),)
    __table_args__ += (Index('idx_ym_id', 'year_month', 'journal_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    journal_id = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_ajlyymm'))
    language_id = Column(INTEGER(unsigned=True), ForeignKey('counter_article_language.id', name='idlanguage_ajlyymm'))
    yop = Column(INTEGER(4))
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class AggrJournalGeolocationYOPYearMonthMetric(Base):
    __tablename__ = 'aggr_journal_geolocation_yop_year_month_metric'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'journal_id', 'country_code', 'yop', name='uni_col_jou_geo_yop_ymm_ajgyymm'),)
    __table_args__ += (Index('idx_ym_id', 'year_month', 'journal_id'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    journal_id = Column(INTEGER(unsigned=True), ForeignKey('counter_journal.id', name='idjournal_ajgyymm'))
    country_code = Column(VARCHAR(4), nullable=False)
    yop = Column(INTEGER(4))
    year_month = Column(VARCHAR(7), nullable=False)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


class ArticleCode(Base):
    __tablename__ = 'counter_article_code'
    __table_args__ = (UniqueConstraint('collection', 'pid_v2', 'pid_v3', 'doi', name='uni_col_pid2_pid3_doi_cac'),)
    __table_args__ += (Index('idx_p2_p3', 'pid_v2', 'pid_v3'),)
    __table_args__ += (Index('idx_p2_doi', 'pid_v2', 'doi'),)
    __table_args__ += (Index('idx_p3_doi', 'pid_v3', 'doi'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(VARCHAR(3), nullable=False, primary_key=True)
    pid_v2 = Column(VARCHAR(23), nullable=False, primary_key=True)
    pid_v3 = Column(VARCHAR(23), nullable=False, primary_key=True)
    doi = Column(VARCHAR(255), nullable=False, primary_key=True)
