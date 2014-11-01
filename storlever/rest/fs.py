from storlever.rest.common import (get_view, post_view, 
                                   put_view, delete_view)
from storlever.rest.common import get_params_from_request
from pyramid.response import Response

from storlever.lib.exception import StorLeverError
from storlever.mngr.fs import fsmgr
from storlever.mngr.fs import ext4
from storlever.mngr.fs import xfs
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal

    

def includeme(config):
    config.add_route('type_list', '/fs/type_list')
    config.add_route('mkfs', '/fs/mkfs')
    config.add_route('fs_list', '/fs/list')
    config.add_route('fs', '/fs/list/{fsname}')
    config.add_route('fs_meta', '/fs/list/{fsname}/meta')
     
    config.add_route('ls', '/fs/list/{fsname}/ls')
    
    
    
    
    
    config.add_route('share_list', '/fs/fs_list/{fs}/share_list')



#http://192.168.1.2:6543/storlever/api/v1/fs/type_list
@get_view(route_name='type_list')
def get_fs_type_list(request):
    fs_mrg = fsmgr.fs_mgr()
    type_list = fs_mrg.fs_type_list()
    return type_list

mk_fs_schema = Schema({
    "type": StrRe(r"^([a-zA-Z].+)$"),
    "dev": StrRe(r"^(/dev/.+)$"),
    Optional("options"): Default(StrRe(),default=""),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
#curl -v -X POST -d type=ext4 -d dev=/dev/mapper/vg1-lv   http://192.168.1.2:6543/storlever/api/v1/fs/mkfs
@post_view(route_name='mkfs')
def mk_fs(request):
    fs_mrg = fsmgr.fs_mgr()
    params = get_params_from_request(request, mk_fs_schema)
    fs_mrg.mkfs_on_dev(params["type"],params["dev"],params["options"])
    return Response(status=200)

#http://192.168.1.2:6543/storlever/api/v1/fs_list
@get_view(route_name='fs_list')
def get_fs_list(request):
    fs_mrg = fsmgr.fs_mgr()
    files = fs_mrg.get_fs_list()
    fs_dict = []
    for fs in files:
        fs_info = {
                   'name':fs.name,
                   'conf':fs.fs_conf,
                   'available':fs.is_available(),
                   }
        fs_dict.append(fs_info)
    return fs_dict

add_fs_schema = Schema({
    "fsname": StrRe(r"^([a-zA-Z].+)$"),
    "type": StrRe(r"^([a-zA-Z].+)$"),
    "dev": StrRe(r"^(/dev/.+)$"),
    
    Optional("mountoption"): Default(StrRe(),default=""),
    Optional("checkonboot"): Default(BoolVal(), default=False),
    Optional("comment"): Default(StrRe(),default=""),
    Optional("user"): Default(StrRe(),default="unknown"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})              
#curl -v -X POST -d fsname=test -d dev=/dev/mapper/vg1-lv -d type=ext4  http://192.168.1.2:6543/storlever/api/v1//fs/list
@post_view(route_name='fs_list')
def add_fs(request):
    fs_mrg = fsmgr.fs_mgr()
    params = get_params_from_request(request, add_fs_schema)
    fs_mrg.add_fs(params["fsname"],params["type"],params["dev"],\
                              params["mountoption"],params["checkonboot"],params["user"])
    return Response(status=200)

#curl -v -X get http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}
@get_view(route_name='fs')
def get_fs(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    fs_info = {
                   'name':fs.name,
                   'conf':fs.fs_conf,
                   'available':fs.is_available(),
                   'usage': fs.usage_info()
                   }
    return fs_info

change_fs_schema = Schema({
    "op": StrRe(r"^(grow)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X put -d op=grow http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}
@put_view(route_name='fs')
def change_fs(request):
    params = get_params_from_request(request, change_fs_schema)
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    
    if(params['op']) == 'grow' :
        fs.grow_size()
        return Response(status=200) 
    else :
        return Response(status=403)


#curl -v -X get http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}/meta
@get_view(route_name='fs_meta')
def get_fs_meda(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    meta_info = fs.fs_meta_dump()
    return meta_info

#curl -v -X delete http://192.168.1.2:6543/storlever/api/v1/fs_list/{fsname}
@delete_view(route_name='fs')
def del_fs(request):
    user=request.client_addr
    fs_name = request.matchdict['fsname']
    
    fs_mrg = fsmgr.fs_mgr()
    fs_mrg.del_fs(fs_name,user)
    return Response(status=200)


get_fs_ls_schema = Schema({
    Optional("path"): Default(StrRe(),default=""),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X get  -H "Content-Type: application/json; charset=UTF-8" -d '{"path":"aa"}' http://192.168.1.2:6543/storlever/api/v1/fs/list/test/ls
@get_view(route_name='ls')
def get_fs_ls(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, get_fs_ls_schema)
    path = params["path"]
    print path
    usage_info = fs.ls_dir(path)
    return usage_info
