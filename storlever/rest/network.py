from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.rest.common import get_params_from_request
from storlever.lib.exception import StorLeverError
from pyramid.response import FileResponse
from storlever.mngr.network import ifmgr
from storlever.mngr.network import netif
from pyramid.response import Response
from storlever.mngr.network.bond import BondManager

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
    config.add_route('single_list', '/network/single_list')
    config.add_route('single_port', '/network/single_list/{port_name}')
    config.add_route('bond_list', '/network/bond_list')
    config.add_route('bond_port', '/network/bond_list/{port_name}')
    config.add_route('dns', '/network/dns')

#/network/port_list
@get_view(route_name='port_list')
def network_get(request):
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    eth_list_dict = []
    for port_name in eth_list:
        port_info = netif.get_port_info(port_name)
        eth_list_dict.append(port_info)
    return eth_list_dict

#/network/single_list
@get_view(route_name='single_list')
def get_single_list(request):
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    eth_list_dict = []
    for port_name in eth_list:
        port_info = netif.get_port_info(port_name)
        eth_list_dict.append(port_info)
    return eth_list_dict

#/network/single_list/{port_name}
@get_view(route_name='single_port')
def get_single_port(request):
    port = str(request.matchdict['port_name'])
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    if port in eth_list:    
        eth_list_dict = []
        port_info = netif.get_port_info(port)
        eth_list_dict.append(port_info)
        return eth_list_dict
    else:
        #raise StorLeverError(" does not exist")
        return Response(status=500)
        
@put_view(route_name='single_port')
def post_single_port(request):
    port_info = get_params_from_request(request)
    port = str(request.matchdict['port_name'])
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    if port in eth_list:
        port_info_old = netif.get_port_info(port)
        ip = port_info.get("ip",port_info_old["ip"])
        netmask = port_info.get("netmask",port_info_old["netmask"])
        gateway = port_info.get("gateway",port_info_old["gateway"])
        netif_set = netif.EthInterface(port)
        port_info = netif_set.set_ip_config(ip, netmask, gateway, user="unknown")
        return  Response(status=200)
    else:
        #raise StorLeverError(" does not exist")
        return Response(status=500)

def network_post(request):
    raise StorLeverError('it failing')
    return "post successfully"

#/network/bond_list
@get_view(route_name='bond_list')
def get_bond_list(request):
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    eth_list_dict = []
    for port_name in eth_list:
        port_info = netif.get_port_info(port_name)
        eth_list_dict.append(port_info)
    return eth_list_dict

@post_view(route_name='bond_list')
def add_bond_group(request):
    BondManager.add_group(self, miimon, mode, ifs=[],
                  ip="", netmask="", gateway="",
                  user="unknown")
    return eth_list_dict