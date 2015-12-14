from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from storlever.mngr.block import blockmgr
from storlever.mngr.block import scsimgr
from storlever.mngr.block.md import md
from pyramid.response import Response
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
from storlever.rest.common import get_params_from_request

def includeme(config):
    # block device list resource
    # GET:    block device list
    config.add_route('block_list', '/block/block_list')
    config.add_route('block', '/block/block_list/{block}')
    config.add_route('block_opt', '/block/block_list/{block}/opt')
    config.add_route('dev_list', '/block/scsi/dev_list')
    config.add_route('dev_host_list', '/block/scsi/host_list')
    config.add_route('scan_bus', '/block/scsi/scan_bus')
    config.add_route('scsi_dev', '/block/scsi/dev_list/{scsi_id}')
    config.add_route('scsi_dev_smart', '/block/scsi/dev_list/{scsi_id}/smart')
    


# http://192.168.1.10:6543/storlever/api/v1/block/block_list
@get_view(route_name='block_list')
def blocks_get(request):
    block_mgr =  blockmgr.block_mgr()
    block_list = block_mgr.get_block_dev_list()
    block_info_dict = []
    
    for block_info in block_list:
        block = {
                 'name':block_info.name,
                 'major':block_info.major,
                 'minor':block_info.minor,
                 'size':block_info.size,
                 'type':block_info.type,
                 'readonly':block_info.readonly,
                 'fs_type':block_info.fs_type,
                 'mount_point':block_info.mount_point
                 }
        
        block_info_dict.append(block)
        
    return block_info_dict

# http://192.168.1.10:6543/storlever/api/v1/block/block_list/sdb
@get_view(route_name='block')
def block_get(request):
    block_name = request.matchdict['block']
    block_mgr =  blockmgr.block_mgr()
    block_info = block_mgr.get_block_dev_by_name(block_name)
    block = {
             'name':block_info.name,
             'major':block_info.major,
             'minor':block_info.minor,
             'size':block_info.size,
             'type':block_info.type,
             'readonly':block_info.readonly,
             'fs_type':block_info.fs_type,
             'mount_point':block_info.mount_point
             }
        
    return block

block_clean_meta_schema = Schema({
    Optional("opt"): StrRe(r"^(clean_meta|flush_buf)$"),
    DoNotCare(Use(str)): object   # for all those key we don't care
})

# curl -v -X put -d opt=clean_meta  'http://192.168.1.123:6543/storlever/api/v1/block/block_list/sdb'
@put_view(route_name='block')
def block_clean_meta(request):
    block_name = request.matchdict['block']
    params = get_params_from_request(request, block_clean_meta_schema)
    if params['opt'] == "clean_meta":  
        block_mgr =  blockmgr.block_mgr()
        block_dev = block_mgr.get_block_dev_by_name(block_name)
        block_dev.clean_meta()
    elif params['opt'] == "flush_buf":  
        block_mgr =  blockmgr.block_mgr()
        block_dev = block_mgr.get_block_dev_by_name(block_name)
        block_dev.flush_block_buf()   
    return Response(status=200)

# curl -v -X PUT  -d opt="flush_buf/clean_meta"http://192.168.1.10:6543/storlever/api/v1/block/block_list/sdb/opt
@put_view(route_name='block_opt')
def set_block_opt(request):
    scsi_id = request.matchdict['scsi_id']
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_dev_info = scsi_mgr.get_scsi_dev_by_id(scsi_id)
    params = get_params_from_request(request, scsi_dev_smart_schema)
    smart_set = params.get("smart", None),
    offline_set = params.get("offline_auto", None),
    scsi_dev_info.set_smart_config(smart_set,offline_set)
    return Response(status=200)


    
# http://192.168.1.10:6543/storlever/api/v1/block/scsi/dev_list
@get_view(route_name='dev_list')
def scsi_list_get(request):
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_list = scsi_mgr.get_scsi_dev_list()
    scsi_list_dict = []
    
    for scsi_dev_info in scsi_list:
        model = scsi_dev_info.model
        scsi_dev = {
                 'scsi_id':scsi_dev_info.scsi_id,
                 'scsi_type':scsi_dev_info.scsi_type,
                 'dev_file':scsi_dev_info.dev_file,
                 'sg_file':scsi_dev_info.sg_file,
                 'vendor':scsi_dev_info.vendor,
                 'model':model,
                 'rev':scsi_dev_info.rev,
                 'state':scsi_dev_info.state
                 }
        
        scsi_list_dict.append(scsi_dev)
    return scsi_list_dict


# http://192.168.1.10:6543/storlever/api/v1/block/scsi/host_list
@get_view(route_name='dev_host_list')
def host_list_get(request):
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_list = scsi_mgr.get_scsi_host_list()
    return scsi_list



scan_bus_schema = Schema({                
    Optional("opt"): StrRe(r"^(re_scan)$"),
    Optional("host"): Default(ListVal(IntVal(0, 16)), default=[]),
    Optional("channels"): Default(ListVal(IntVal(0, 1)), default=[]),
    Optional("targets"): Default(ListVal(IntVal(0, 16)), default=[]),
    Optional("luns"): Default(ListVal(IntVal(0, 7)), default=[]),
    Optional("remove"): BoolVal(),
    Optional("force_rescan"): BoolVal(),
    Optional("force_remove"): BoolVal(),
    DoNotCare(Use(str)): object   # for all those key we don't care
})
# curl -v -X put -d opt=re_scan  http://192.168.1.10:6543/storlever/api/v1/block/scsi/scan_bus
@put_view(route_name='scan_bus')
def scan_bus(request):
    scsi_mgr =  scsimgr.scsi_mgr()
    params = get_params_from_request(request, scan_bus_schema)
    remove = params.get("remove", False),
    force_rescan = params.get("force_rescan", False),
    force_remove = params.get("force_remove", False),
    if params['opt'] == "re_scan":  
        scsi_mgr.rescan_bus(params['host'], params['channels'], params['targets'],\
                             params['luns'],remove,force_rescan, force_remove)
    return Response(status=200)


# http://192.168.1.10:6543/storlever/api/v1/block/dev_list/{scsi_id}
@get_view(route_name='scsi_dev')
def get_scsi_dev(request):
    scsi_id = request.matchdict['scsi_id']
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_dev_info = scsi_mgr.get_scsi_dev_by_id(scsi_id)
    
    model = scsi_dev_info.model
    scsi_dev = {
             'scsi_id':scsi_dev_info.scsi_id,
             'scsi_type':scsi_dev_info.scsi_type,
             'dev_file':scsi_dev_info.dev_file,
             'sg_file':scsi_dev_info.sg_file,
             'vendor':scsi_dev_info.vendor,
             'model':model,
             'rev':scsi_dev_info.rev,
             'state':scsi_dev_info.state
             } 
    return scsi_dev


# http://192.168.1.10:6543/storlever/api/v1/block/scsi_list/{scsi_id}/smart
@get_view(route_name='scsi_dev_smart')
def get_scsi_dev_smartinfo(request):
    scsi_id = request.matchdict['scsi_id']
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_dev_info = scsi_mgr.get_scsi_dev_by_id(scsi_id)
    samrt_info = scsi_dev_info.get_smart_info()
    return samrt_info

scsi_dev_smart_schema = Schema({
    Optional("smart"): BoolVal(),
    Optional("offline_auto"): BoolVal(),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
# curl -v -X PUT  -d smart="true/false" -d offline_auto="true/false" http://192.168.1.10:6543/storlever/api/v1/block/scsi_list/2:0:0:0/smart
@put_view(route_name='scsi_dev_smart')
def set_scsi_dev_smart(request):
    scsi_id = request.matchdict['scsi_id']
    scsi_mgr =  scsimgr.scsi_mgr()
    scsi_dev_info = scsi_mgr.get_scsi_dev_by_id(scsi_id)
    params = get_params_from_request(request, scsi_dev_smart_schema)
    smart_set = params.get("smart", None),
    offline_set = params.get("offline_auto", None),
    scsi_dev_info.set_smart_config(smart_set,offline_set)
    return Response(status=200)



#@get_view(route_name='adapter_list')
#def adapters_get(request):
    #pass


#@get_view(route_name='adapter')
#def adapters_get(request):
    #pass


#@get_view(route_name='adapter_disk_list')
#def adapters_get(request):
    #pass


#@get_view(route_name='adapter_vdisk_list')
#def adapters_get(request):
    #pass