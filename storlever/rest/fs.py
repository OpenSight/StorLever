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
    #config.add_route('fs_usage', '/fs/list/{fsname}/usage')
    config.add_route('fs_meta', '/fs/list/{fsname}/meta')
    config.add_route('ls', '/fs/list/{fsname}/ls')
    config.add_route('opt', '/fs/list/{fsname}/opt')
    config.add_route('quota_group_list', '/fs/list/{fsname}/quota_group')
    config.add_route('quota_group', '/fs/list/{fsname}/quota_group/{group_name}')#put dete
    config.add_route('quota_user_list', '/fs/list/{fsname}/quota_user')#get post
    config.add_route('quota_user', '/fs/list/{fsname}/quota_user/{user_name}')#put dete
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
    "fsname": StrRe(r"^(.+)$"),
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
    "opt": StrRe(r"^(grow)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

#curl -v -X put -d op=grow http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}
@put_view(route_name='fs')
def change_fs(request):
    params = get_params_from_request(request, change_fs_schema)
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    
    if(params['opt']) == 'grow' :
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
    ls_info = fs.ls_dir(path)
    return ls_info

file_opt_schema = Schema({
    "opt": StrRe(r"^(mod_owner|mod_mode|quota_check)|$"),
    Optional("path"): StrRe(r"^(.+)$"),
    Optional("user"): Default(StrRe(r"^(.+)$"),default=None),
    Optional("group"): Default(StrRe(r"^(.+)$"),default=None),
    Optional("mode"): Default(StrRe(r"^(.+)$"),default=None),
    DoNotCare(Use(str)): object  # for all those key we don't care
}) 
#curl -v -X put  -H "Content-Type: application/json; charset=UTF-8" -d '{"opt":"mod_owner","path":"aa"}' http://192.168.1.2:6543/storlever/api/v1/fs/list/test/opt
@get_view(route_name='opt')
def file_opt_owner(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, get_fs_ls_schema)
    path = params["path"]
    if(params['opt']) == 'mod_owner' :
        user = params["user"]
        group = params["group"]
        fs.mod_dir_owner(path,user,group,request.client_addr)
        return Response(status=200)
    elif params['opt'] == 'mod_mode' :
        mode = params["mode"]
        fs.mod_dir_mode(path,mode,request.client_addr)
        return Response(status=200)
    elif params['opt'] == 'quota_check' :
        mode = params["mode"]
        fs.quota_check()
        return Response(status=200)
    else :
        return Response(status=403)


'''
file_opt_schema = Schema({
    Optional("path"): StrRe(r"^(.+)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
}) 
#curl -v -X get http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}/usage
@get_view(route_name='fs_usage')
def get_fs_usage(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, file_opt_schema)
    path = params["path"]
    usage_info = fs.dir_usage_stat(path)
    return usage_info
'''
   
#http://192.168.1.2:6543/storlever/api/v1/fs/list/{fsname}/quota_group_list
@get_view(route_name='quota_group_list')
def get_quota_group_list(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    group_info = fs.quota_group_report()
    return group_info

add_quoat_group_schema = Schema({
    "group": StrRe(r"^(.+)$"),
    Optional("block_softlimit"): Default(int(),default=0),
    Optional("block_hardlimit"): Default(int(),default=0),
    Optional("inode_softlimit"): Default(int(),default=0),
    Optional("inode_hardlimit"): Default(int(),default=0),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
@post_view(route_name='group_quota_list')
def add_quota_group(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, add_quoat_group_schema)
    group = params["group"]
    block_softlimit = params["block_softlimit"]
    block_hardlimit = params["block_hardlimit"]
    inode_softlimit = params["inode_softlimit"]
    inode_hardlimit = params["inode_hardlimit"]
    fs.quota_group_set(group,block_softlimit,block_hardlimit,inode_softlimit,inode_hardlimit)
    return Response(status=200)

put_quoat_group_schema = Schema({
    "group": StrRe(r"^(.+)$"),
    Optional("block_softlimit"): Default(int(),default=0),
    Optional("block_hardlimit"): Default(int(),default=0),
    Optional("inode_softlimit"): Default(int(),default=0),
    Optional("inode_hardlimit"): Default(int(),default=0),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
#config.add_route('quota_group', '/fs/list/{fsname}/quota_group/{group_name}')#put dete
@put_view(route_name='quota_group')
def put_quota_group(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, put_quoat_group_schema)
    group = params["group"]
    block_softlimit = params["block_softlimit"]
    block_hardlimit = params["block_hardlimit"]
    inode_softlimit = params["inode_softlimit"]
    inode_hardlimit = params["inode_hardlimit"]
    fs.quota_group_set(group,block_softlimit,block_hardlimit,inode_softlimit,inode_hardlimit)
    return Response(status=200)

del_quoat_group_schema = Schema({
    "group": StrRe(r"^(.+)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
#config.add_route('quota_group', '/fs/list/{fsname}/quota_group/{group_name}')#put dete
@delete_view(route_name='quota_group')
def del_quota_group(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, del_quoat_group_schema)
    group = params["group"]
    fs.quota_group_set(group,0,0,0,0)
    return Response(status=200)


# config.add_route('quota_user_list', '/fs/list/{fsname}/quota_user')#get post
#   config.add_route('quota_user', '/fs/list/{fsname}/quota_user/{user_name}')#put dete

@get_view(route_name='quota_user_list')
def get_quota_user_list(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    quota_user_info = fs.quota_user_report()
    return quota_user_info

add_quoat_user_schema = Schema({
    "user": StrRe(r"^(.+)$"),
    Optional("block_softlimit"): Default(int(),default=0),
    Optional("block_hardlimit"): Default(int(),default=0),
    Optional("inode_softlimit"): Default(int(),default=0),
    Optional("inode_hardlimit"): Default(int(),default=0),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
@post_view(route_name='quota_user_list')
def add_quota_user(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, add_quoat_user_schema)
    user = params["user"]
    block_softlimit = params["block_softlimit"]
    block_hardlimit = params["block_hardlimit"]
    inode_softlimit = params["inode_softlimit"]
    inode_hardlimit = params["inode_hardlimit"]
    fs.quota_user_set(user,block_softlimit,block_hardlimit,inode_softlimit,inode_hardlimit)
    return Response(status=200)

put_quoat_user_schema = Schema({
    "user": StrRe(r"^(.+)$"),
    Optional("block_softlimit"): Default(int(),default=0),
    Optional("block_hardlimit"): Default(int(),default=0),
    Optional("inode_softlimit"): Default(int(),default=0),
    Optional("inode_hardlimit"): Default(int(),default=0),
    DoNotCare(Use(str)): object  # for all those key we don't care
})

@put_view(route_name='quota_user')
def put_quota_user(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, put_quoat_group_schema)
    user = params["user"]
    block_softlimit = params["block_softlimit"]
    block_hardlimit = params["block_hardlimit"]
    inode_softlimit = params["inode_softlimit"]
    inode_hardlimit = params["inode_hardlimit"]
    fs.quota_user_set(user,block_softlimit,block_hardlimit,inode_softlimit,inode_hardlimit)
    return Response(status=200)

del_quoat_user_schema = Schema({
    "user": StrRe(r"^(.+)$"),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
@delete_view(route_name='quota_user')
def del_quota_user(request):
    fs_name = request.matchdict['fsname']
    fs_mrg = fsmgr.fs_mgr()
    fs = fs_mrg.get_fs_by_name(fs_name)
    params = get_params_from_request(request, del_quoat_group_schema)
    user = params["user"]
    fs.quota_group_set(user,0,0,0,0)
    return Response(status=200)
