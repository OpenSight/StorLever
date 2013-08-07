from pyramid.view import view_config, view_defaults

from storlever.api.common import version_cmp, eq, lt, gt, le, ge


def includeme(config):
    config.add_route('network', '/network')


@view_config(route_name='network',
             request_method='GET',
             custom_predicates=(version_cmp(eq, 1),))
def network_get(request):
    return {'eth0': {'ip':'192.168.1.22', 'gateway': '192.168.1.1'}}


@view_config(route_name='network',
             request_method='GET',
             custom_predicates=(version_cmp(eq, 2),))
def network_get_v2(request):
    return {'eth0': {}}



    
