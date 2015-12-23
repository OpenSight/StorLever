import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('block-set', '/partials/block-set')

@get_view(route_name='block-set', renderer='storlever:templates/partials/block-set.pt')
def interface_get(request):
    return {}