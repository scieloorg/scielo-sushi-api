from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from os import environ
from .models import DBSession, Base


def main(global_config, **settings):
    sqlalchemy_url_value = environ.get('STR_CONNECTION', 'mysql://root:pass@172.17.0.3:3306/matomo')
    settings.update({'sqlalchemy.url': sqlalchemy_url_value})

    application_url_value = environ.get('APPLICATION_URL', 'http://127.0.0.1:6543')
    settings.update({'application.url': application_url_value})

    config = Configurator(settings=settings)

    engine = engine_from_config(settings, 'sqlalchemy.', pool_recycle=1800)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config.add_route('home', '/')
    config.add_route('status', '/status')
    config.add_route('members', '/members')
    config.add_route('reports', '/reports')
    config.add_route('reports_report_id', '/reports/{report_id}')
    config.scan('.views')

    return config.make_wsgi_app()
