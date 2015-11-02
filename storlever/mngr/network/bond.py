"""
storlever.mngr.network.bond
~~~~~~~~~~~~~~~~

This module implements some functions of network interface bond management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path
import re

from storlever.lib.command import check_output, read_file_entry, \
    write_file_entry
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
from storlever.lib.lock import lock


from storlever.mngr.network.netif import EthInterface, IF_CONF_PATH, \
    IFUP, IFDOWN
from storlever.mngr.network.ifmgr import SYSFS_NET_DEV, if_mgr, \
    check_network_manager_exist
from storlever.mngr.network import ifconfig
from storlever.lib.confparse import properties
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "bond",
    "rpms": [
        "initscripts",
    ],
    "comment": "Provides the management functions for bonding network interface"
}

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
        path = os.path.join(SYSFS_NET_DEV, self.name, "bonding/miimon")
        return int(read_file_entry(path))

    @property
    def mode(self):
        """return mode"""
        path = os.path.join(SYSFS_NET_DEV, self.name, "bonding/mode")
        mode = read_file_entry(path).split()[1]
        return int(mode)

    @property
    def slaves(self):
        path = os.path.join(SYSFS_NET_DEV, self.name, "bonding/slaves")
        return read_file_entry(path).split()

    def set_bond_config(self, miimon=None, mode=None, user="unknown"):

        if mode not in modeMap:
            StorLeverError("mdoe(%d) is not supported" % mode, 400)

        if miimon is None:
            miimon = self.miimon

        if mode is None:
            mode = self.mode

        self.conf["BONDING_OPTS"] = \
            '"miimon=%d mode=%d"' % (miimon, mode)

        self.save_conf()

        if self.ifconfig_interface.is_up():
            check_output([IFDOWN, self.name])
            check_output([IFUP, self.name])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "bond group(%s) config is updated by  user(%s)" %
                   (self.name, user))


class BondManager(object):
    """contains all methods to manage the bond group in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()

    def _find_max_index(self):
        list = self.group_name_list()
        max = -1
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
        if os.path.exists(MODPROBE_CONF):        
            with open(MODPROBE_CONF, 'r') as conf_file:
                lines = conf_file.readlines()
        else:
            lines = []

        for line in lines:
            if name in line:
                break
        else:
            lines.append('alias %s bonding\n' % name)

        with open(MODPROBE_CONF, 'w') as conf_file:
            conf_file.writelines(lines)


    def _del_bond_from_conf(self, name):
        if not os.path.exists(MODPROBE_CONF):        
            return
        with open(MODPROBE_CONF, 'r') as conf_file:
            lines = conf_file.readlines()
        lines = [line for line in lines if (name not in line)]
        with open(MODPROBE_CONF, 'w') as conf_file:
            conf_file.writelines(lines)

    def get_group_by_name(self, name):
        list = self.group_name_list()
        if name not in list:
            raise StorLeverError("Bond Group(%s) does not exist" % name, 404)
        return BondGroup(name)

    def get_group_list(self):
        group_list = []
        name_list = read_file_entry(BONDING_MASTERS, "").split()
        for group_name in name_list:
            group_list.append(BondGroup(group_name))
        return group_list

    def group_name_list(self):
        return read_file_entry(BONDING_MASTERS, "").split()

    def add_group(self, miimon, mode, ifs=[],
                  ip="", netmask="", gateway="",
                  user="unknown"):
        """ add a bond group

        parameters:
        miimon, int, link detect interval in ms
        mode, int, bond mode
        ifs, Array of string, the array of the slave interface name

        return the new bond group name (bond interface name)

        """

        if mode not in modeMap:
            StorLeverError("mdoe(%d) is not supported" % mode, 400)

        # get mutex
        with self.lock:
            # check slave ifs exist and not slave
            exist_if_list = if_mgr().interface_name_list()
            for slave_if in ifs:
                if slave_if not in exist_if_list:
                    raise StorLeverError("%s not found" % slave_if, 404)

                if ifconfig.Interface(slave_if).is_slave():
                    raise StorLeverError("%s is already a slave of other bond group"
                                         % slave_if, 400)

            # find the available bond name
            max_index = self._find_max_index()
            bond_name = "bond%d" % (max_index + 1)

            # change bond.conf
            self._add_bond_to_conf(bond_name)

            # create ifcfg-bond*
            conf = properties(DEVICE=bond_name,
                              IPADDR="",
                              NETMASK="",
                              GATEWAY="",
                              BOOTPROTO="none",
                              NM_CONTROLLED="no",
                              ONBOOT="yes",
                              BONDING_OPTS='"miimon=%d, mode=%d"'
                                           % (miimon, mode))
            ifcfg_name = "ifcfg-%s" % bond_name
            conf.apply_to(os.path.join(IF_CONF_PATH, ifcfg_name))

            # modify the slave's ifcfg
            for slave_if in ifs:
                slave_object = EthInterface(slave_if)
                slave_object.conf.delete("IPADDR")
                slave_object.conf.delete("NETMASK")
                slave_object.conf.delete("GATEWAY")
                slave_object.conf["BOOTPROTO"] = "none"
                slave_object.conf["ONBOOT"] = "yes"
                slave_object.conf["MASTER"] = bond_name
                slave_object.conf["SLAVE"] = "yes"
                slave_object.save_conf()

        # remove the if's ip avoid ip conflict
        # for slave_if in ifs:
            # check_output([IFDOWN, slave_if])
            # ifconfig.Interface(slave_if).set_ip("0.0.0.0")
            # check_output([IFUP, slave_if])

        # restart network
        check_output([IFUP, bond_name])

        # set real ip
        if ip != "" or netmask != "" or gateway != "":
            with self.lock:
                conf = properties(IPADDR=ip,
                                  NETMASK=netmask,
                                  GATEWAY=gateway)
                conf.apply_to(os.path.join(IF_CONF_PATH, ifcfg_name))
            check_output([IFDOWN, bond_name])
            check_output([IFUP, bond_name])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "New bond group %s (mode:%d, miimon:%d, slaves:[%s]) "
                   "is added by user(%s)" %
                   (bond_name, mode, miimon, ",".join(ifs),  user))

        return bond_name

    def del_group(self, bond_name, user="unknown"):
        # check exist
        group_name_list = self.group_name_list()
        if bond_name not in group_name_list:
            raise StorLeverError("%s not found" % bond_name, 404)
        if bond_name == "bond0":
            # if want to delete bond0, there must be no other
            # group, because bonding driver would auto create bond0 interface
            # if there is another bond interface beyond bond0
            if (len(group_name_list) > 1) or \
                    (group_name_list[0] != bond_name):
                raise StorLeverError("Other bonding group must be "
                               "deleted before bond0 can be deleted", 400)

        bond_group = BondGroup(bond_name)
        bond_slaves = bond_group.slaves

        check_output([IFDOWN, bond_name])

        # get mutex
        with self.lock:
            # change bond.conf
            self._del_bond_from_conf(bond_name)

            # modify the slaves conf, especial for the first one,
            # copy the bond ip config to it
            is_first = True
            for slave in bond_slaves:
                slave_object = EthInterface(slave)
                if is_first:
                    slave_object.conf["IPADDR"] = \
                        bond_group.conf.get("IPADDR", "")
                    slave_object.conf["NETMASK"] = \
                        bond_group.conf.get("NETMASK", "")
                    slave_object.conf["GATEWAY"] = \
                        bond_group.conf.get("GATEWAY", "")
                    is_first = False
                else:
                    slave_object.conf["IPADDR"] = ""
                    slave_object.conf["NETMASK"] = ""
                    slave_object.conf["GATEWAY"] = ""

                slave_object.conf.delete("MASTER")
                slave_object.conf.delete("SLAVE")
                slave_object.save_conf()


            # delete ifcfg-bond*
            ifcfg_name = os.path.join(IF_CONF_PATH, "ifcfg-%s" % bond_name)
            if os.path.isfile(ifcfg_name):
                os.remove(ifcfg_name)

        # restart network
        if os.path.exists(BONDING_MASTERS):
            write_file_entry(BONDING_MASTERS, "-%s\n" % bond_name)
        for slave_if in bond_slaves:
            check_output([IFUP, slave_if])

        # if_mgr()._restart_network()

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "bond group %s (slaves:[%s]) "
                   "is deleted by user(%s)" %
                   (bond_name, ",".join(bond_slaves),  user))


BondManager = BondManager()


def bond_mgr():
    """return the global user manager instance"""
    return BondManager






