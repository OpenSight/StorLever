from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.rest.common import get_params_from_request
from pyramid.response import Response

from storlever.lib.exception import StorLeverError
from storlever.mngr.block.lvm import lvm
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
    
    
def includeme(config):
    # vg (volume group) list resource
    # GET:    vg list
    # POST:   add/delete vg
    config.add_route('vg_list', '/block/lvm/vg_list')
    # vg resource
    # GET:    vg information
    # POST:   add/remove PV from vg
    # DELETE: remove vg
    config.add_route('vg', '/block/lvm/vg_list/{vg}')
    config.add_route('vg_op', '/block/lvm/vg_list/{vg}/op')
    
    # lv (logical volume) list resource
    # GET:    lv list
    # POST:   add/delete lv
    config.add_route('lv_list', '/block/lvm/vg_list/{vg}/lv_list')
    # lv resource
    # GET:    lv information
    # POST:   enlarge/shrink lv
    # DELETE: delete lv
    config.add_route('lv', '/block/lvm/vg_list/{vg}/lv_list/{lv}')
    config.add_route('lv_op', '/block/lvm/vg_list/{vg}/lv_list/{lv}/op')
    config.add_route('lv_snapshot', '/block/lvm/vg_list/{vg}/lv_list/{lv}/snapshot')
    config.add_route('pvmove', '/block/lvm/pvmove')

#curl -v -X GET http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list
@get_view(route_name='vg_list')
def get_vg_list(request):
    lvm_mng = lvm.lvm_mgr()
    vgs = lvm_mng.get_all_vg()
    vg_dict = []
    for vg in vgs:
        vg_info = {
                   'name':vgs[vg].name,
                   'uuid':vgs[vg].uuid,
                   'size':vgs[vg].size,
                   'free_size':vgs[vg].free_size,
                   }
        vg_dict.append(vg_info)
    return vg_dict

new_vg_schema = Schema({
    "vgname": StrRe(r"^([a-zA-Z].+)$"),
    "dev": Default(ListVal(StrRe(r"^(/dev/sd[a-z]|/dev/md.+)$")), default=[]),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X POST -d vgname=vg1 -d dev=/dev/sdb,/dev/sdc  http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list
#enable eth* or disable eth*
@post_view(route_name='vg_list')
def create_vg(request):
    lvm_mng = lvm.lvm_mgr()
    params = get_params_from_request(request, new_vg_schema)
    vg = lvm_mng.new_vg(params['vgname'], params['dev'])
    
    if vg is None:
        return Response(status=500)
    else:
        vg_info = {
                   'name':vg.name,
                   'uuid':vg.uuid,
                   'size':vg.size,
                   'free_size':vg.free_size,
                   }
        return vg_info

#curl -v -X GET http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}
@get_view(route_name='vg')
def get_vg_info(request):
    vg_name = request.matchdict['vg']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    vg_info = {
               'name':vg.name,
               'uuid':vg.uuid,
               'size':vg.size,
               'free_size':vg.free_size,
               }
    return vg_info

vg_op_schema = Schema({
    Optional("opt"): StrRe(r"^(grow|shrink)$"),
    Optional("dev"): Default(ListVal(StrRe(r"^(/dev/sd[a-z]|/dev/md.+)$")), default=[]),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X post -d opt=grow -d dev=/dev/sdb http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}/op
@post_view(route_name='vg_op')
def post_vg_op(request):
    params = get_params_from_request(request, vg_op_schema)
    vg_name = request.matchdict['vg']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    if(params['opt']) == 'grow':
        for dev in params['dev']:
            vg.grow(dev)
    elif(params['opt']) == 'shrink':
        for dev in params['dev']:
            vg.shrink(dev)
    return Response(status=200)


#curl -v -X delete http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}
@delete_view(route_name='vg')
def delete_vg_rest(request):
    vg_name = request.matchdict['vg']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    vg.delete()
    return Response(status=200)


add_lv_schema = Schema({
    "lvname": StrRe(r"^([a-zA-Z].+)$"),
    "size": IntVal(1024), #min 1024
    DoNotCare(Use(str)): object  # for all those key we don't care
})
#curl -v -X post -d lvname=vgx size=204800000 http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}
@post_view(route_name='vg')
def add_lv(request):
    vg_name = request.matchdict['vg']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    params = get_params_from_request(request, add_lv_schema)
    lv = vg.create_lv(params['lvname'],params['size'])
    if vg is None:
        return Response(status=500)
    else:
        lv_info = {
                   'name':lv.name,
                   'uuid':lv.uuid,
                   'size':lv.size,
                   'state':lv.is_activate,
                   'origin':lv.origin,
                   'attr':lv.attr,
                   'snap_percent':lv.snap_percent
                   }
        return lv_info


#curl -v -X GET http://192.168.1.123:6543/storlever/api/v1/block/lvm/{vg}/lv_list
@get_view(route_name='lv_list')
def get_lv_list(request):
    vg_name = request.matchdict['vg']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    lv_dict = []
    lvs = vg.lvs
    for lv in lvs:
        lv_info = {
               'name':lvs[lv].name,
               'uuid':lvs[lv].uuid,
               'size':lvs[lv].size,
               'state':lvs[lv].is_activate,
               'origin':lvs[lv].origin,
               'attr':lvs[lv].attr,
               'snap_percent':lvs[lv].snap_percent
               }
        lv_dict.append(lv_info)
    return lv_dict

#curl -v -X GET http://192.168.1.123:6543/storlever/api/v1/block/lvm/lv_list/lvname
@get_view(route_name='lv')
def get_lv(request):
    vg_name = request.matchdict['vg']
    lv_name = request.matchdict['lv']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    lv = vg.get_lv(lv_name)
    lv_info = {
           'name':lv.name,
           'uuid':lv.uuid,
           'size':lv.size,
           'state':lv.is_activate,
           'origin':lv.origin,
           'attr':lv.attr,
           'snap_percent':lv.snap_percent
           }
    return lv_info


@delete_view(route_name='lv')
def get_lv(request):
    vg_name = request.matchdict['vg']
    lv_name = request.matchdict['lv']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    lv = vg.get_lv(lv_name)
    lv.delete()
    return Response(status=200)


lv_op_schema = Schema({
    "opt": StrRe(r"^(activate|disable)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X post -d opt=activate http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}/lv_list/{lv}/opt
@post_view(route_name='lv_op')
def post_lv_op(request):
    params = get_params_from_request(request, lv_op_schema)
    vg_name = request.matchdict['vg']
    lv_name = request.matchdict['lv']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    lv = vg.get_lv(lv_name)
    if(params['opt']) == 'activate' :
        lv.activate()
    elif(params['opt']) == 'disable' :
        lv.deactivate()
               
    return Response(status=200)


lv_snapshot_schema = Schema({
    "name": StrRe(r"^([a-zA-Z].+)$"),
    "size": IntVal(1024),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X post -d opt=activate http://192.168.1.123:6543/storlever/api/v1/block/lvm/vg_list/{vg}/lv_list/{lv}/snapshot
@post_view(route_name='lv_snapshot')
def post_lv_snapshot(request):
    params = get_params_from_request(request, lv_snapshot_schema)
    vg_name = request.matchdict['vg']
    lv_name = request.matchdict['lv']
    lvm_mng = lvm.lvm_mgr()
    vg = lvm_mng.get_vg(vg_name)
    lv = vg.get_lv(lv_name)
    lv.snapshot(params['name'], params['size'])
    return Response(status=200)

pv_move_schema = Schema({
    "src":StrRe(r"^(/dev/sd[a-z]|/dev/md.+)$"),
    Optional("dst"): StrRe(r"^(/dev/sd[a-z]|/dev/md.+)$"),
    Optional("lvname"): StrRe(r"^([a-zA-Z].+)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X post -d src  http://192.168.1.123:6543/storlever/api/v1/block/lvm/pvmove
@post_view(route_name='pvmove')
def post_pv_move(request):
    params = get_params_from_request(request, pv_move_schema)
    pv_name = params["src"]
    pv_mgr = lvm.PV(name=pv_name)
    pv_mgr.move(params["dst"], params["lvname"])
    return Response(status=200)
