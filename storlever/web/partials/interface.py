import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('interface', '/partials/interface')

@get_view(route_name='interface', renderer='storlever:templates/partials/interface.pt')
def interface_get(request):
    return {}