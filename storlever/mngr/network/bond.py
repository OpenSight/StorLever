"""
storlever.mngr.network.bond
~~~~~~~~~~~~~~~~

This module implements some functions of network interface bond management.

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
MODPROBE_CONF = "/etc/modprobe.d/bond.conf"
BONDING_MASTERS = SYSFS_NET_DEV + "bonding_masters"

class BondGroup(object):
    def __init__(self, name):
        self.name = name


class BondManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        pass

    def get_group_by_name(self, name):
        list = self.group_name_list()
        if name not in list:
            raise StorLeverError("Bond Group(%s) does not exist" % name, 404)
        return BondGroup(name)

    def group_name_list(self):
        return read_file_entry(BONDING_MASTERS, "").splite()

    def add_group(self):
        pass

    def del_group(self, name):
        pass


BondManager = BondManager()


def bond_mgr():
    """return the global user manager instance"""
    return BondManager






