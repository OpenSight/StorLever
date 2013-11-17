"""
storlever.mngr.network.ifmgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux network interface management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import os

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging

from storlever.mngr.network.netif import EthInterface
from storlever.mngr.network import ifconfig


SYSFS_NET_DEV = "/sys/class/net/"


class EthInterfaceManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        # need a mutex to provide thread-safe

        # construct a Interface type mapping table
        pass

    def _restart_network(self):
        check_output(["/etc/init.d/network", "restart"])

    def _get_if_encap(self, name):
        encap_type = 1
        type_path = os.path.join(SYSFS_NET_DEV, name, "type")
        with open(type_path, "r") as type_file:
            encap_type = int(type_file.read())
        return encap_type

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

        return EthInterface(dev.name, dev)

    def interface_list(self):
        interfaces = []
        for dev in ifconfig.iterifs(False):
            if dev.name == "lo":    # loopback interface is not handled
                continue

            if self._get_if_encap(dev.name) != 1:
                # only support Ethernet
                continue

            interfaces.append(EthInterface(dev.name, dev))

        return interfaces


EthInterfaceManager = EthInterfaceManager()


def if_mgr():
    """return the global user manager instance"""
    return EthInterfaceManager






