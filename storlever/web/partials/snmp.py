import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('snmp', '/partials/snmp')

@get_view(route_name='snmp', renderer='storlever:templates/partials/snmp.pt')
def interface_get(request):
    return {}