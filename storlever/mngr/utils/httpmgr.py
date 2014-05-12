"""
storlever.mngr.utils.httpmgr
~~~~~~~~~~~~~~~~

This module implements ntp server management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from storlever.mngr.system.servicemgr import service_mgr
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "http",
    "rpms": [
        "httpd"
    ],
    "comment": "Provides some simple support for the http server"
}


service_mgr().register_service("http", "httpd", "/usr/sbin/httpd", "HTTP Server(apache httpd)")
ModuleManager.register_module(**MODULE_INFO)



