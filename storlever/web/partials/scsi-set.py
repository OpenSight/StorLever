import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('scsi-set', '/partials/scsi-set')

@get_view(route_name='scsi-set', renderer='storlever:templates/partials/scsi-set.pt')
def interface_get(request):
    return {}