import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('zabbix', '/partials/zabbix')

@get_view(route_name='zabbix', renderer='storlever:templates/partials/zabbix.pt')
def interface_get(request):
    return {}