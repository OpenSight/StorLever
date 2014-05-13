"""
storlever_megaraid.rest.megaraid
~~~~~~~~~~~~~~~~

This module implement the REST API of megaraid module

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.rest.common import (get_view, post_view,
                                   put_view, delete_view)
from storlever.lib.exception import StorLeverError

from storlever_megaraid.mngr.block.megaraid import megaraidmgr

def includeme(config):
    config.add_route('megaraid_physical_list', '/block/megaraid/physical_list')


@get_view(route_name='megaraid_physical_list')
def get_megaraid_physical_list(request):
    return {'eth0': {'ip': '192.168.1.22', 'gateway': '192.168.1.1'}}


