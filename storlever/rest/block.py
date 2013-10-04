from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError


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



@get_view(route_name='block_list')
def blocks_get(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}


@get_view(route_name='block')
def adapters_get(request):
    pass


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
