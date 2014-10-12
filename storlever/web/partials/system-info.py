import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('system-info', '/partials/system-info')

@get_view(route_name='system-info', renderer='storlever:templates/partials/system-info.pt')
def statistics_get(request):
    return {}