"""
storlever.rest.san
~~~~~~~~~~~~~~~~

This module implements the rest API for SAN servers.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.rest.common import get_view, post_view, put_view, delete_view
from pyramid.response import Response

from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal
from storlever.lib.exception import StorLeverError
from storlever.mngr.san.tgt import tgtmgr


from storlever.rest.common import get_params_from_request

def includeme(config):

    config.add_route('tgt_conf', '/san/tgt/conf')
    config.add_route('tgt_target_iqn_list', '/san/tgt/target_list')
    config.add_route('tgt_target_info', '/san/tgt/target_list/{target_iqn}')

    config.add_route('tgt_target_incominguser_list',
                     '/san/tgt/target_list/{target_iqn}/incominguser_list')
    config.add_route('tgt_target_incominguser_info',
                     '/san/tgt/target_list/{target_iqn}/incominguser_list/{user_name}')
    config.add_route('tgt_target_outgoinguser_list',
                     '/san/tgt/target_list/{target_iqn}/outgoinguser_list')
    config.add_route('tgt_target_outgoinguser_info',
                     '/san/tgt/target_list/{target_iqn}/outgoinguser_list/{user_name}')

    config.add_route('tgt_target_lun_list',
                     '/san/tgt/target_list/{target_iqn}/lun_list')
    config.add_route('tgt_target_lun_info',
                     '/san/tgt/target_list/{target_iqn}/lun_list/{lun_number}')



@get_view(route_name='tgt_conf')
def get_tgt_conf(request):
    tgt_mgr = tgtmgr.TgtManager
    return tgt_mgr.get_tgt_conf()

tgt_conf_schema = Schema({

    # Define iscsi incoming discovery authentication setting. If it is
    # empty, no authentication is performed. The format is username:passwd
    Optional("incomingdiscoveryuser"): StrRe(r"^(|\w+:\w+)$"),

    # Define iscsi outgoing discovery authentication setting. If it is
    # empty, no authentication is performe  The format is username:passwd
    Optional("outgoingdiscoveryuser"): StrRe(r"^(|\w+:\w+)$"),

    DoNotCare(Use(str)): object  # for all other key we don't care
})





@put_view(route_name='tgt_conf')
def put_tgt_conf(request):
    tgt_mgr = tgtmgr.TgtManager
    tgt_conf = get_params_from_request(request, tgt_conf_schema)
    tgt_mgr.set_tgt_conf(tgt_conf, operator=request.client_addr)
    return Response(status=200)




@get_view(route_name='tgt_target_iqn_list')
def get_tgt_target_iqn_list(request):
    tgt_mgr = tgtmgr.TgtManager
    return tgt_mgr.get_target_iqn_list()


target_conf_schema = Schema({
    "iqn": StrRe(r"^\S+$"),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@post_view(route_name='tgt_target_iqn_list')
def post_tgt_target_iqn_list(request):
    tgt_mgr = tgtmgr.TgtManager
    new_target_conf = get_params_from_request(request, target_conf_schema)
    tgt_mgr.create_target(new_target_conf["iqn"], operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('tgt_target_info',
                                      target_iqn=new_target_conf["iqn"])
    return resp


@get_view(route_name='tgt_target_info')
def get_tgt_target_info(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    target_conf = {
        "iqn": iqn,
        "state": target.get_state(),
        "initiator_addr_list": target.get_initiator_addr_list(),
        "initiator_name_list": target.get_initiator_name_list(),
        "incominguser_list": target.get_incominguser_list(),
        "outgoinguser_list": target.get_outgoinguser_list(),
        "session_list": target.get_session_list(),
        "lun_num":len(target.get_lun_list())
    }

    return target_conf




target_mod_schema = Schema({
    # target state, can only set to offline or ready, if present
    Optional("state"): StrRe(r"^(offline|ready)$"),

    # Allows connections only from the specified IP address. It means to ALL if
    # no any initiator-address is specified.
    Optional("initiator_addr_list"): [StrRe(r"^\S+$")],

    # Allows connections only from the specified initiator name. It means to ALL if
    # no any initiator-name is specified.
    Optional("initiator_name_list"): [StrRe(r"^\S+$")],


    DoNotCare(Use(str)): object  # for all other key we don't care
})



@put_view(route_name='tgt_target_info')
def put_tgt_target_info(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target_conf = get_params_from_request(request, target_mod_schema)
    target = tgt_mgr.get_target_by_iqn(iqn)

    if "initiator_addr_list" in target_conf:
        target.set_initiator_addr_list(target_conf["initiator_addr_list"],
                                       operator=request.client_addr)

    if "initiator_name_list" in target_conf:
        target.set_initiator_name_list(target_conf["initiator_name_list"],
                                       operator=request.client_addr)

    if "state" in target_conf:
        target.set_state(target_conf["state"], operator=request.client_addr)

    return Response(status=200)



@delete_view(route_name='tgt_target_info')
def delete_tgt_target_info(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    tgt_mgr.remove_target_by_iqn(iqn, operator=request.client_addr)
    return Response(status=200)




@get_view(route_name='tgt_target_incominguser_list')
def get_tgt_target_incominguser_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    return target.get_incominguser_list()

user_conf_schema = Schema({
    "username": StrRe(r"^\w+$"),
    "password": StrRe(r"^\w+$"),

    DoNotCare(Use(str)): object  # for all other key we don't care
})

@post_view(route_name='tgt_target_incominguser_list')
def post_tgt_target_incominguser_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    new_user_conf = get_params_from_request(request, user_conf_schema)
    target.set_incominguser(new_user_conf["username"], new_user_conf["password"], operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('tgt_target_incominguser_info',
                                      target_iqn=iqn,
                                      user_name=new_user_conf["username"])
    return resp



@put_view(route_name='tgt_target_incominguser_info')
def put_tgt_target_incominguser_info(request):
    iqn = request.matchdict['target_iqn']
    username = request.matchdict['user_name']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    mod_user_conf = get_params_from_request(request)
    mod_user_conf["username"] = username
    mod_user_conf = user_conf_schema.validate(mod_user_conf)

    target.set_incominguser(mod_user_conf["username"], mod_user_conf["password"], operator=request.client_addr)

    return Response(status=200)

@delete_view(route_name='tgt_target_incominguser_info')
def delete_tgt_target_incominguser_info(request):
    iqn = request.matchdict['target_iqn']
    username = request.matchdict['user_name']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    target.del_incominguser(username, operator=request.client_addr)
    return Response(status=200)




@get_view(route_name='tgt_target_outgoinguser_list')
def get_tgt_target_outgoinguser_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    return target.get_outgoinguser_list()


@post_view(route_name='tgt_target_outgoinguser_list')
def post_tgt_target_outgoinguser_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    new_user_conf = get_params_from_request(request, user_conf_schema)
    target.set_outgoinguser(new_user_conf["username"], new_user_conf["password"], operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('tgt_target_outgoinguser_info',
                                      target_iqn=iqn,
                                      user_name=new_user_conf["username"])
    return resp


@put_view(route_name='tgt_target_outgoinguser_info')
def put_tgt_target_outgoinguser_info(request):
    iqn = request.matchdict['target_iqn']
    username = request.matchdict['user_name']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    mod_user_conf = get_params_from_request(request)
    mod_user_conf["username"] = username
    mod_user_conf = user_conf_schema.validate(mod_user_conf)

    target.set_outgoinguser(mod_user_conf["username"], mod_user_conf["password"], operator=request.client_addr)

    return Response(status=200)

@delete_view(route_name='tgt_target_outgoinguser_info')
def delete_tgt_target_outgoinguser_info(request):
    iqn = request.matchdict['target_iqn']
    username = request.matchdict['user_name']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    target.del_outgoinguser(username, operator=request.client_addr)
    return Response(status=200)





@get_view(route_name='tgt_target_lun_list')
def get_tgt_target_lun_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    return target.get_lun_list()


lun_conf_schema = Schema({

    # lun number
    "lun": IntVal(1, 255),

    # path to a regular file, or block device, or a sg char device
    Optional("path"): StrRe(r"^\S+$"),

    # the type of device . Possible device-types are:
    # disk    : emulate a disk device
    # tape    : emulate a tape reader
    # ssc     : same as tape
    # cd      : emulate a DVD drive
    # changer : emulate a media changer device
    # pt      : passthrough type to export a /dev/sg device
    Optional("device_type"): StrRe(r"^(disk|tape|ssc|cd|changer|pt)$"),

    # the type of backend storage. Possible backend types are:
    # rdwr    : Use normal file I/O. This is the default for disk devices
    # aio     : Use Asynchronous I/O
    # sg      : Special backend type for passthrough devices
    #  ssc     : Special backend type for tape emulation
    Optional("bs_type"): StrRe(r"^(rdwr|aio|sg|ssc)$"),

    # if true, a direct mapped logical unit (LUN) with the same properties as the
    # physical device (such as VENDOR_ID, SERIAL_NUM, etc.)
    Optional("direct_map"): BoolVal(),

    # enable write cache or not
    Optional("write_cache"): BoolVal(),

    # readonly or read-write
    Optional("readonly"): BoolVal(),

    # online or offline
    Optional("online"): BoolVal(),

    # scsi id, if empty, it would automatically be set to a default value
    Optional("scsi_id"): StrRe(r"^\S*$"),

    # scsi sn, if empty, it would automatically be set to a default value
    Optional("scsi_sn"): StrRe(r"^\S*$"),

    DoNotCare(Use(str)): object  # for all other key we don't care
})


@post_view(route_name='tgt_target_lun_list')
def post_tgt_target_lun_list(request):
    iqn = request.matchdict['target_iqn']
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    new_lun_conf = get_params_from_request(request, lun_conf_schema)
    if "path" not in new_lun_conf:
        raise StorLeverError("New LUN's path must be configured", 400)

    target.add_lun(new_lun_conf["lun"],
                   new_lun_conf["path"],
                   new_lun_conf.get("device_type", "disk"),
                   new_lun_conf.get("bs_type", "rdwr"),
                   new_lun_conf.get("direct_map", False),
                   new_lun_conf.get("write_cache", True),
                   new_lun_conf.get("readonly", False),
                   new_lun_conf.get("online", True),
                   new_lun_conf.get("scsi_id", ""),
                   new_lun_conf.get("scsi_sn", ""),
                   operator=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('tgt_target_lun_info',
                                      target_iqn=iqn,
                                      lun_number=new_lun_conf["lun"])
    return resp



@get_view(route_name='tgt_target_lun_info')
def get_tgt_target_lun_info(request):
    iqn = request.matchdict['target_iqn']
    lun = int(request.matchdict['lun_number'])
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    lun_conf = target.get_lun_by_num(lun)
    return lun_conf


@put_view(route_name='tgt_target_lun_info')
def put_tgt_target_lun_info(request):
    iqn = request.matchdict['target_iqn']
    lun = int(request.matchdict['lun_number'])
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    mod_lun_conf = get_params_from_request(request)
    mod_lun_conf["lun"] = lun
    mod_lun_conf = lun_conf_schema.validate(mod_lun_conf)
    target.set_lun(mod_lun_conf["lun"],
                   mod_lun_conf.get("path"),
                   mod_lun_conf.get("device_type"),
                   mod_lun_conf.get("bs_type"),
                   mod_lun_conf.get("direct_map"),
                   mod_lun_conf.get("write_cache"),
                   mod_lun_conf.get("readonly"),
                   mod_lun_conf.get("online"),
                   mod_lun_conf.get("scsi_id"),
                   mod_lun_conf.get("scsi_sn"),
                   operator=request.client_addr)

    return Response(status=200)



@delete_view(route_name='tgt_target_lun_info')
def delete_tgt_target_lun_info(request):
    iqn = request.matchdict['target_iqn']
    lun = int(request.matchdict['lun_number'])
    tgt_mgr = tgtmgr.TgtManager
    target = tgt_mgr.get_target_by_iqn(iqn)
    target.del_lun(lun, operator=request.client_addr)
    return Response(status=200)
