import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('mail', '/partials/mail')

@get_view(route_name='mail', renderer='storlever:templates/partials/mail.pt')
def interface_get(request):
    return {}