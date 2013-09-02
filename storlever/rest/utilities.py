from storlever.rest.common import get_view, post_view, put_view, delete_view


def includeme(config):
    # GET:  get NTP configuration
    # POST: set NTP configuration
    config.add_route('ntp', '/ntp')
    

@get_view(route_name='ntp')
def system_get(request):
    return {'cpu': 'Intel'}
