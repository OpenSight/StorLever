''' StorLever main file to make a wsgi application
'''

from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    json_indent = settings.get("json.indent")

    # make JSON as the default renderer
    config.add_renderer(None, JSON(indent=json_indent))

    # route and view configuration of REST API version 1 can be found in module storlever.rest
    # check storlever.rest.__init__.py for more detail
    config.include('storlever.rest', route_prefix='storlever/api/v1')

    # scan to register view callables
    config.scan()
    
    return config.make_wsgi_app()

