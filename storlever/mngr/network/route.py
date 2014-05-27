"""
storlever.mngr.network.route
~~~~~~~~~~~~~~~~

This module implements some functions of DNS for linux network.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""


from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import cfg_mgr
from storlever.lib import logger
import logging
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.modulemgr import ModuleManager
from storlever.lib.command import check_output


MODULE_INFO = {
    "module_name": "route_tab",
    "rpms": [
        "net-tools",
    ],
    "comment": "Provides the functions to handle IP route table in the network system"
}


ROUTE_CMD = "/sbin/route"

class RouteManager(object):
    """contains all methods to manage dns configure"""

    def __init__(self):
        # need a mutex to protect name servers config
        pass

    def get_ipv4_route_list(self):
        route_list = []
        route_lines = check_output([ROUTE_CMD, "-n"]).splitlines()

        for line in route_lines[2:]:
            words = line.split()
            if len(words) < 8 :
                continue
            if words[0] == "Destination":
                continue
            route_list.append({
                "destination": words[0],
                "gateway": words[1],
                "genmask": words[2],
                "flags": words[3],
                "metric": int(words[4]),
                "ref": int(words[5]),
                "use": int(words[6]),
                "iface": words[7]
            })

        return route_list

    def get_ipv6_route_list(self):
        route_list = []
        route_lines = check_output([ROUTE_CMD, "-n", "-A", "inet6"]).splitlines()

        for line in route_lines[2:]:
            words = line.split()
            if len(words) < 7 :
                continue
            if words[0] == "Destination":
                continue
            route_list.append({
                "destination": words[0],
                "next_hop": words[1],
                "flags": words[2],
                "metric": int(words[3]),
                "ref": int(words[4]),
                "use": int(words[5]),
                "iface": words[6]
            })

        return route_list

def route_mgr():
    """return the global user manager instance"""
    return RouteManager

RouteManager = RouteManager()

# register cfg file
ModuleManager.register_module(**MODULE_INFO)








