"""
storlever.mngr.network.ifmgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux network interface management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os

from storlever.lib.command import check_output, read_file_entry
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.cfgmgr import cfg_mgr

from storlever.mngr.network.netif import EthInterface
from storlever.mngr.network import ifconfig
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "ethernet",
    "rpms": [
        "initscripts",
    ],
    "comment": "Provides the management functions for ethernet interface in the system, "
               "like configure, get state/info, statistic and etc"

}



SYSFS_NET_DEV = "/sys/class/net/"

def check_network_manager_exist():
    if os.path.exists('/var/run/NetworkManager/NetworkManager.pid'):
        pid = open('/var/run/NetworkManager/NetworkManager.pid').read().strip()
        if os.path.exists('/proc/%s/cmdline' % pid) and \
                ('NetworkManager'in open('/proc/%s/cmdline' % pid).read()):
            raise StorLeverError("NetworkManager must be shutdown", 500)


class EthInterfaceManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        pass

    def _restart_network(self):
        check_output(["/sbin/service", "network", "restart"])

    def _get_if_encap(self, name):
        type_path = os.path.join(SYSFS_NET_DEV, name, "type")
        return int(read_file_entry(type_path, 1))

    def get_interface_by_name(self, name):

        if name == "lo":    # loopback interface is not handled
            raise StorLeverError("Interface(%s) cannot support" % name, 404)

        dev = ifconfig.findif(name, False)
        if dev is None:
            raise StorLeverError("Interface(%s) does not exist" % name, 404)

        encap_type = self._get_if_encap(dev.name)
        if encap_type != 1:
            raise StorLeverError("Interface(%s)'s type(%d) is not supported by storlever"
                                 % (name, encap_type), 400)

        return EthInterface(dev.name)

    def get_interface_list(self):

        interfaces_name = []
        for dev in ifconfig.iterifs(False):
            if dev.name == "lo":    # loopback interface is not handled
                continue

            if self._get_if_encap(dev.name) != 1:
                # only support Ethernet
                continue

            interfaces_name.append(dev.name)
        interfaces_name.sort()

        interfaces = []
        for name in interfaces_name:
            interfaces.append(EthInterface(name))

        return interfaces

    def interface_name_list(self):
        interfaces = []
        for dev in ifconfig.iterifs(False):
            if dev.name == "lo":    # loopback interface is not handled
                continue

            if self._get_if_encap(dev.name) != 1:
                # only support Ethernet
                continue

            interfaces.append(dev.name)

        interfaces.sort()

        return interfaces


EthInterfaceManager = EthInterfaceManager()
		
def if_mgr():
    """return the global user manager instance"""
    return EthInterfaceManager



# register cfg file
cfg_mgr().register_config_file("/etc/modprobe.d/bond.conf")
cfg_mgr().register_config_file("/etc/sysconfig/network-scripts", r"^ifcfg-(.+)$")
ModuleManager.register_module(**MODULE_INFO)









