from storlever.api.common import get_view, post_view, put_view, delete_view


def includeme(config):
    config.add_route('network', '/network')
    

@get_view(route_name='network',
          api_ver=lambda ver: ver==1)
def network_get(request):
    return {'eth0': {'ip':'192.168.1.22', 'gateway': '192.168.1.1'}}

@get_view(route_name='network',
          api_ver=lambda ver: ver==2)
def network_get_v2(request):
    return {'eth0': {}}

@post_view(route_name='network',
          api_ver=lambda ver: ver==1)
def network_post(request):
    return "post successfully"
