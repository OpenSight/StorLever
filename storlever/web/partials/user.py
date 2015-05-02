import platform

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.lib.exception import StorLeverError

def includeme(config):
    config.add_route('user', '/partials/user')

@get_view(route_name='user', renderer='storlever:templates/partials/user.pt')
def user_get(request):
    return {}