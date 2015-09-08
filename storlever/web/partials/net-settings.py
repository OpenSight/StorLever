import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('net-settings', '/partials/net-settings')

@get_view(route_name='net-settings', renderer='storlever:templates/partials/net-settings.pt')
def interface_get(request):
    return {}