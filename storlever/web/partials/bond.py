import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('bond', '/partials/bond')

@get_view(route_name='bond', renderer='storlever:templates/partials/bond.pt')
def interface_get(request):
    return {}