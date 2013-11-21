"""
storlever.mngr.network.bond
~~~~~~~~~~~~~~~~

This module implements some functions of network interface bond management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import os
import re

from storlever.lib.command import check_output, read_file_entry
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging


from storlever.mngr.network.netif import EthInterface, IF_CONF_PATH, \
    IFUP, IFDOWN
from storlever.mngr.network.ifmgr import SYSFS_NET_DEV, if_mgr
from storlever.mngr.network import ifconfig
from storlever.lib.confparse import properties



MODPROBE_CONF = "/etc/modprobe.d/bond.conf"
BONDING_MASTERS = SYSFS_NET_DEV + "bonding_masters"


modeMap = {
    0: 'balance-rr',
    1: 'active-backup',
    2: 'balance-xor',
    3: 'broadcast',
    4: '802.3ad',
    5: 'balance-tlb',
    6: 'balance-alb',
}


class BondGroup(EthInterface):

    @property
    def miimon(self):
        """return miimon in ms"""
        path = os.path.join(SYSFS_NET_DEV, self.name, "/bonding/miimon")
        return int(read_file_entry(path))

    @property
    def mode(self):
        """return mode"""
        path = os.path.join(SYSFS_NET_DEV, self.name, "/bonding/mode")
        return int(read_file_entry(path))

    def set_bond_config(self, miimon, mode):
        if mode not in modeMap:
            StorLeverError("mdoe(%d) is not supported" % mode, 400)

        self.conf["BONDING_OPTS"] = \
            '%s miimon=%d mode=%d' % (self.name, miimon, mode)
        self.save_conf()

        if self.ifconfig_interface.is_up():
            check_output([IFDOWN, self.name])
            check_output([IFUP, self.name])


class BondManager(object):
    """contains all methods to manage the bond group in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        pass

    def _find_max_index(self):
        list = self.group_name_list()
        max = 0
        pattern = re.compile(r"^bond(\d+)$")
        for bond_name in list:
            match = pattern.match(bond_name)
            if match is None:
                continue
            index = int(match.group(1))
            if index > max:
                max = index
        return max

    def _add_bond_to_conf(self, name):
        with open(MODPROBE_CONF, 'a+') as conf_file:
            conf_file.write('alias %s bonding\n' % name)

    def _del_bond_from_conf(self, name):
        with open(MODPROBE_CONF, 'r+') as conf_file:
            lines = conf_file.readlines()
            for line in lines:
                if name in line:
                    lines.remove(line)
            conf_file.truncate(0)
            conf_file.writelines(lines)





    def get_group_by_name(self, name):
        list = self.group_name_list()
        if name not in list:
            raise StorLeverError("Bond Group(%s) does not exist" % name, 404)
        return BondGroup(name)

    def group_name_list(self):
        return read_file_entry(BONDING_MASTERS, "").splite()

    def add_group(self, miimon, mode, ifs = [],
                  ip="", netmask="", gateway="",
                  user="unknown"):
        """ add a bond group

        parameters:
        miimon, int, link detect interval in ms
        mode, int, bond mode
        ifs, Array of string, the array of the slave interface name

        return the new bond group name (bond interface name)

        """

        # get mutex

        if mode not in modeMap:
            StorLeverError("mdoe(%d) is not supported" % mode, 400)

        # check slave ifs exist and not slave
        exist_if_list = if_mgr().interface_name_list()
        for slave_if in ifs:
            if slave_if not in exist_if_list:
                StorLeverError("%s is not supported" % slave_if, 400)
            if ifconfig.Interface(slave_if).is_slave():
                StorLeverError("%s is already a slave of other bond group"
                               % slave_if, 400)

        # find the available bond name
        max_index = self._find_max_index()
        bond_name = "bond%d" % (max_index + 1)

        # change bond.conf
        self._add_bond_to_conf(bond_name)

        # create ifcfg-bond*
        conf = properties(DEVICE=bond_name,
                          IPADDR=ip,
                          NETMASK=netmask,
                          BOOTPROTO="none",
                          ONBOOT="yes",
                          BONDING_OPTS='"%s miimon=%d, mode=%d"'
                                       % (bond_name, miimon, mode))
        ifcfg_name = "ifcfg-%s" % bond_name
        conf.apply_to(os.path.join(IF_CONF_PATH, ifcfg_name))

        # modify the slave's ifcfg


        # restart network
        check_output([IFUP, bond_name])

        return bond_name


    def del_group(self, name):
        # check exist

        # get mutex

        # change bond.conf

        # modify the slaves conf, especial for the first one,
        # copy the bond ip config to it

        # delete ifcfg-bond*

        # change bond.conf

        # restart network
        pass

BondManager = BondManager()

def bond_mgr():
    """return the global user manager instance"""
    return BondManager






