from pyramid.view import view_config, view_defaults
import common

def includeme(config):
    config.add_route('network.all', '/network')
    
@view_defaults(route_name='network.all',
               #custom_predicates = (common.version2float, ),
               renderer='json')
class network(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET',
                 match_param="api_version=1")
    def get(self):
        return {'eth0': {'ip':'192.168.1.22', 'gateway': '192.168.1.1'}}
    
    @view_config(request_method='POST')
    def post(self):
        return 'post successfully'
