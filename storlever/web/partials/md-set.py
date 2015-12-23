import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('md-set', '/partials/md-set')

@get_view(route_name='md-set', renderer='storlever:templates/partials/md-set.pt')
def interface_get(request):
    return {}