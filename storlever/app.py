''' StorLever main file to make a wsgi application
'''

from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.include('storlever.api.network', route_prefix='storlever/api/v{api_version}')

    config.scan()
    
    return config.make_wsgi_app()


