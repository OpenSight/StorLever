from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from pyramid.response import FileResponse


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
    config.add_route('network_interface', '/network/{interface}')
    # test purpose
    config.add_route('download_conf', '/download')


@get_view(route_name='network')
def network_get(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}


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

