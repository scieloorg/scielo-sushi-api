from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import get_counter_tables


def main(global_config, **settings):
    config = Configurator(settings=settings)

    engine = engine_from_config(settings, 'sqlalchemy.')
    counter_tables = get_counter_tables(engine)

    settings = config.registry.settings
    settings['counter_tables'] = counter_tables

    config.add_route('home', '/')
    config.add_route('status', '/status')
    config.add_route('members', '/members')
    config.add_route('reports', '/reports')
    config.add_route('reports_report_id', '/reports/{report_id}')
    config.scan('.views')

    return config.make_wsgi_app()
