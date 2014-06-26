from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from storlever.mngr.block import blockmgr

def includeme(config):
    # block device list resource
    # GET:    block device list
    config.add_route('block_list', '/block_list')
    #
    config.add_route('block', '/block_list/{block}')
    # adapter list resource (HBA, raid controller etc)
    # GET:    adapter list
    config.add_route('adapter_list', '/adapter_list')
    config.add_route('adapter', '/adapter_list/{adapter}')
    config.add_route('adapter_disk_list', '/adapter_list/{adapter}/disk_list')
    config.add_route('adapter_vdisk_list', '/adapter_list/{adapter}/vdisk_list')


# http://192.168.1.10:6543/storlever/api/v1/block_list
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

# http://192.168.1.10:6543/storlever/api/v1/block_list/sdb
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
    


@get_view(route_name='adapter_list')
def adapters_get(request):
    pass


@get_view(route_name='adapter')
def adapters_get(request):
    pass


@get_view(route_name='adapter_disk_list')
def adapters_get(request):
    pass


@get_view(route_name='adapter_vdisk_list')
def adapters_get(request):
    pass
