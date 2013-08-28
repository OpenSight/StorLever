from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view,
                                   RestError)


def includeme(config):
    config.add_route('network', '/network')
    

@get_view(route_name='network')
def network_get(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}


@post_view(route_name='network')
def network_post(request):
    raise RestError('it failing')
    return "post successfully"
