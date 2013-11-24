"""
storlever.mngr.network.ifmgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux network interface management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import os

from storlever.lib.command import check_output, read_file_entry
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging

from storlever.mngr.network.netif import EthInterface
from storlever.mngr.network import ifconfig


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

    def interface_name_list(self):
        interfaces = []
        for dev in ifconfig.iterifs(False):
            if dev.name == "lo":    # loopback interface is not handled
                continue

            if self._get_if_encap(dev.name) != 1:
                # only support Ethernet
                continue

            interfaces.append(dev.name)

        return interfaces


EthInterfaceManager = EthInterfaceManager()


def if_mgr():
    """return the global user manager instance"""
    return EthInterfaceManager






