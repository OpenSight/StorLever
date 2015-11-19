import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('smart', '/partials/smart')

@get_view(route_name='smart', renderer='storlever:templates/partials/smart.pt')
def interface_get(request):
    return {}