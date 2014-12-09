from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError
from storlever.mngr.block.md import md
from pyramid.response import Response
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError, BoolVal, StrRe, ListVal, Or
from storlever.rest.common import get_params_from_request

def includeme(config):
####md rest
    config.add_route('md_list', '/block/md_list') #post get 
    config.add_route('md', '/block/md_list/{md_name}')#get put delete



#http://192.168.1.10:6543/storlever/api/v1/block/md_list
@get_view(route_name='md_list')
def get_md_list(request):
    md_mgr =  md.md_mgr()
    mds = md_mgr.get_all_md()  
    md_info = mds._list_raid()
    return md_info


add_md_schema = Schema({
    "name": StrRe(r"^(.+)$"),
    #"level":  Or(1,0,5,10,6),
    "dev": Default(ListVal(StrRe(r"^(/dev/sd[a-z]|/dev/vd.+)$")), default=[]),
    DoNotCare(Use(str)): object  # for all those key we don't care
})
#curl -v -X POST -d name=test -d dev=/dev/sdb,/dev/sdc -d level=1  http://192.168.1.2:6543/storlever/api/v1/block/md_list
@post_view(route_name='md_list')
def add_md(request):
    md_mgr =  md.md_mgr()
    mds = md_mgr.get_all_md()
    params = get_params_from_request(request, add_md_schema)
    mds.create(params['name'],1,params['dev'])
    return Response(status=200)