from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view,
                                   RestError)


def includeme(config):
    # vg (volume group) list resource
    # GET:    vg list
    # POST:   add/delete vg
    config.add_route('vg_list', '/vg_list')
    # vg resource
    # GET:    vg information
    # POST:   add/remove PV from vg
    # DELETE: remove vg
    config.add_route('vg', '/vg_list/{vg}')
    # lv (logical volume) list resource
    # GET:    lv list
    # POST:   add/delete lv
    config.add_route('lv_list', '/lv_list')
    # lv resource
    # GET:    lv information
    # POST:   enlarge/shrink lv
    # DELETE: delete lv
    config.add_route('lv', '/lv_list/{lv}')


@get_view(route_name='vg_list')
def network_get(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}


@post_view(route_name='vg')
def network_post(request):
    raise RestError('it failing')
    return "post successfully"
