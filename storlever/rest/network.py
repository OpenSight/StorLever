from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from pyramid.response import FileResponse
from storlever.mngr.network import ifmgr


def includeme(config):
    # network resource
    # GET:    network interface list
    # POST:   add or delete bound interface
    config.add_route('network', '/network')
    # network interface resource
    # GET:    interface information
    # POST:   start/stop interface
    # PUT:    modify interface parameter
    # DELETE: delete bound interface
    config.add_route('port_list', '/network/port_list')
	#config.add_route('single_list', '/network/single_list')
	#config.add_route('single_port', '/network/single_list/{port_name}')
	#config.add_route('bond_list', '/network/bond_list')
	#config.add_route('bond_port', '/network/bond_list/{port_name}')
	
	
    #config.add_route('network_interface', '/network/{interface}')
    # test purpose
    config.add_route('download_conf', '/download')


@get_view(route_name='port_list')
def network_get(request):
	eth_face = ifmgr.if_mgr()
	eth_list = eth_face.interface_name_list()
	eth_list_dict = []
	for port in eth_list:
		eth_list_dict.append(port)
	return eth_list_dict

@post_view(route_name='network')
def network_post(request):
    raise StorLeverError('it failing')
    return "post successfully"

# example for file download
@get_view(route_name='download_conf')
def download_conf(request):
    response = FileResponse('/root/install.log', request=request, content_type='application/force-download')
    response.headers['Content-Disposition'] = 'attachment; filename=install.log'
    return response

