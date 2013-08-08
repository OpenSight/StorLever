from storlever.api.common import get_view, post_view, put_view, delete_view


def includeme(config):
    config.add_route('system', '/system')
    

@get_view(route_name='system',
          api_ver=lambda ver: ver==3)
def system_get(request):
    return {'cpu': 'Intel'}


@put_view(route_name='system',
          api_ver=lambda ver: ver==2)
def system_put(request):
    return 'put successfully'
