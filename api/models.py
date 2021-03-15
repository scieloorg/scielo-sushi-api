from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register


DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = automap_base()
