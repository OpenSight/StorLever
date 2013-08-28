''' StorLever main file to make a wsgi application
'''

from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_renderer(None, JSON())
    config.include('storlever.rest.network', route_prefix='storlever/api/v1')
    config.include('storlever.rest.system', route_prefix='storlever/api/v1')
    config.scan()
    
    return config.make_wsgi_app()

