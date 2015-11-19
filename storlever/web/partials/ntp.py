import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('ntp', '/partials/ntp')

@get_view(route_name='ntp', renderer='storlever:templates/partials/ntp.pt')
def interface_get(request):
    return {}