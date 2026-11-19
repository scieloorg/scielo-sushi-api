from os import environ
from threading import BoundedSemaphore

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from api.models.sql_automap import DBSession, Base


def main(global_config, **settings):
    sqlalchemy_url_value = environ.get('STR_CONNECTION', 'mysql://root:pass@172.17.0.3:3306/matomo')
    settings.update({'sqlalchemy.url': sqlalchemy_url_value})

    application_url_value = environ.get('APPLICATION_URL', 'http://127.0.0.1:6543')
    settings.update({'application.url': application_url_value})

    ir_a1_limit = environ.get('SUSHI_IR_A1_MAX_CONCURRENT')
    if ir_a1_limit is not None:
        try:
            ir_a1_limit = int(ir_a1_limit)
            if ir_a1_limit < 0:
                raise ValueError
        except ValueError:
            raise ValueError('SUSHI_IR_A1_MAX_CONCURRENT must be a non-negative integer')
        settings['sushi.ir_a1_max_concurrent'] = ir_a1_limit
        if ir_a1_limit > 0:
            settings['sushi.ir_a1_slots'] = BoundedSemaphore(ir_a1_limit)

    config = Configurator(settings=settings)

    engine = engine_from_config(settings, 'sqlalchemy.', pool_recycle=1800)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config.add_renderer('tsv', 'api.renderers.TSVRenderer')

    config.add_route('home', '/')
    config.add_route('status', '/status')
    config.add_route('members', '/members')
    config.add_route('reports', '/reports')
    config.add_route('reports_report_id', '/reports/{report_id}')
    config.scan('.views')

    return config.make_wsgi_app()
