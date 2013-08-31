from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view,
                                   RestError)


def includeme(config):
    # network resource
    # GET:    network interface list
    # POST:   add or delete bound interface
    config.add_route('block', '/block')


@get_view(route_name='block')
def block_get(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}
