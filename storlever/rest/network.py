from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.rest.common import get_params_from_request
from storlever.lib.exception import StorLeverError
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
from pyramid.response import FileResponse
from storlever.mngr.network import ifmgr
from storlever.mngr.network import netif
from pyramid.response import Response
from storlever.mngr.network import bond
from storlever.mngr.network import dnsmgr

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

def get_port_info(port_name):
    eth_face = ifmgr.if_mgr()
    netif_info = eth_face.get_interface_by_name(port_name)
    ip_info = netif_info.get_ip_config()
    property_info = netif_info.property_info
    link_state = netif_info.link_state
    statistic_info = netif_info.statistic_info
    port_info = {'name': port_name,
                 'ip': ip_info[0],
                 'netmask': ip_info[1],
                 'gateway': ip_info[2],
                 'mac': property_info["mac"],
                 'speed': link_state['speed'],
                 'linkup': link_state['link_up'],
                 'tx': statistic_info['tx_bytes'],
                 'rx': statistic_info['rx_bytes']
                 }
    return port_info


#/network/port_list
@get_view(route_name='port_list')
def network_get(request):
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    eth_list_dict = []
    for port_name in eth_list:
        port_info = get_port_info(port_name)
        eth_list_dict.append(port_info)
    return eth_list_dict

#/network/single_list
@get_view(route_name='single_list')
def get_single_list(request):
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    print eth_list
    eth_list_dict = []
    for port_name in eth_list:
        if 'bond' in port_name:
            continue
        port_info = get_port_info(port_name)
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
        port_info = get_port_info(port)
        eth_list_dict.append(port_info)
        return eth_list_dict
    else:
        #raise StorLeverError(" does not exist")
        return Response(status=500)
        
@put_view(route_name='single_port')
def modify_single_port(request):
    port_info = get_params_from_request(request)
    port = str(request.matchdict['port_name'])
    eth_face = ifmgr.if_mgr()
    eth_list = eth_face.interface_name_list()
    if port in eth_list:
        port_info_old = get_port_info(port)
        ip = port_info.get("ip",port_info_old["ip"])
        netmask = port_info.get("netmask",port_info_old["netmask"])
        gateway = port_info.get("gateway",port_info_old["gateway"])
        netif_set = netif.EthInterface(port)
        port_info = netif_set.set_ip_config(ip, netmask, gateway, request.client_addr)
        return  Response(status=200)
    else:
        #raise StorLeverError(" does not exist")
        return Response(status=500)


#/network/bond_list
@get_view(route_name='bond_list')
def get_bond_list(request):
    bond_manager = bond.bond_mgr()
    bond_list = bond_manager.group_name_list()
    bond_list_dict = []
    
    for bond_name in bond_list:
        port_info = get_port_info(bond_name)
        bond_info = bond.BondGroup(bond_name)       
        port_info['mode'] = bond_info.mode
        port_info['miimon'] = bond_info.miimon
        port_info['slaves'] = bond_info.slaves
        bond_list_dict.append(port_info)
    return bond_list_dict

#curl -v -X POST -d ip=192.168.1.123 -d miimon=100 -d netmask=255.255.255.0 -d gateway=192.168.1.1 -d mode=1 -d slaves=eth0,eth1 'http://192.168.1.123:6543/storlever/api/v1/network/bond_list'
@post_view(route_name='bond_list')
def add_bond_group(request):
    params = get_params_from_request(request)
    bond_manager = bond.bond_mgr()
    blist = str(params['slaves']).split(",")
    bond_manager.add_group(int(params['miimon']), int(params['mode']),blist,
                  params['ip'], params['netmask'], params['gateway'],
                  request.client_addr)
    return Response(status=201)

@get_view(route_name='bond_port')
def get_bond_port_info(request):
    bond_name = request.matchdict['port_name']
    port_info = get_port_info(bond_name)
    bond_info = bond.BondGroup(bond_name)       
    port_info['mode'] = bond_info.mode
    port_info['miimon'] = bond_info.miimon
    port_info['slaves'] = bond_info.slaves
    return port_info


#curl -v -X put -d ip=192.168.1.122  -d miimon=100 -d netmask=255.255.255.0 -d gateway=192.168.1.11 -d mode=1  'http://192.168.1.123:6543/storlever/api/v1/network/bond_list/bond0'
@put_view(route_name='bond_port')
def modify_bond_group(request):
    port_name = request.matchdict['port_name']
    bond_manager = bond.bond_mgr()
    bond_list = bond_manager.group_name_list()
    if port_name in bond_list:
        params = get_params_from_request(request)
        port_info = get_port_info(port_name)
        bond_info = bond.BondGroup(port_name)       
        
        if  params.has_key('miimon'):
            miimon = int(params['miimon'])
        else:
            miimon = bond_info.miimon

        if params.has_key('mode'):
            mode = int(params['mode'])
        else:
            mode = bond_info.mode
            
        if params.has_key('ip'):
            ip = params['ip']
        else:
            ip = port_info['ip']
            
        if params.has_key('netmask'):
            ip = params['netmask']
        else:
            ip = port_info['netmask']
            
        if params.has_key('gateway'):
            ip = params['gateway']
        else:
            ip = port_info['gateway']
            
        bond_group = bond.BondGroup(str(port_name))
        bond_group.set_bond_config(miimon,mode,ip,params['netmask'],params['gateway'])
        return Response(status=200)
    else:
        #raise StorLeverError(" does not exist")
        return Response(status=500)


@get_view(route_name='dns')
def get_dns(request):
    dns_manager = dnsmgr.dns_mgr()
    servers = dns_manager.get_name_servers()
    return servers

# curl -v -X put -d ip=192.168.1.123 -d servers=8.8.8.8,202.101.172.47  'http://192.168.1.123:6543/storlever/api/v1/network/dns'
@put_view(route_name='dns')
def modify_dns(request):
    params = get_params_from_request(request)
    servers = str(params['servers']).split(",")
    print servers
    dns_manager = dnsmgr.dns_mgr()
    dns_manager.set_name_servers(servers, request.client_addr)
    return Response(status=200)
