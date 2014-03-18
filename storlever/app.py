"""
storlever.common
~~~~~~~~~~~~~~~~

StorLever's main file to make a WSGI application.

:copyright: (c) 2013 by Yiting Huang.
:license: GPLv3, see LICENSE for more details.

"""

from pyramid.config import Configurator
from pyramid.renderers import JSON
from storlever.lib.lock import set_lock_factory_from_name


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # get user-specific config from setting
    json_indent = settings.get("json.indent")
    if json_indent is not None:
        json_indent = int(json_indent)

    # get lock factory
    if (settings.get("lock.module") is not None) and \
            (settings.get("lock.factory") is not None):
        set_lock_factory_from_name(settings.get("lock.module"),
                                   settings.get("lock.factory"))

    # make JSON as the default renderer
    config.add_renderer(None, JSON(indent=json_indent))

    # route and view configuration of REST API version 1 can be found in module storlever.rest
    # check storlever.rest.__init__.py for more detail
    config.include('storlever.rest', route_prefix='storlever/api/v1')

    # route and view configuration of Web UI can be found in module storlever.web
    # check storlever.web.__init__.py for more detail
    config.include('storlever.web')

    return config.make_wsgi_app()

