from pyramid.config import Configurator

from .models import DBSession, Base


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_route('home', '/')
    config.add_route('status', '/status')
    config.add_route('members', '/members')
    config.add_route('reports', '/reports')
    config.add_route('reports_report_id', '/reports/{report_id}')
    config.scan('.views')
    return config.make_wsgi_app()
