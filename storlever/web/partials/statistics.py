import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('statistics', '/partials/statistics')

@get_view(route_name='statistics', renderer='storlever:templates/partials/statistics.pt')
def statistics_get(request):
    return {}