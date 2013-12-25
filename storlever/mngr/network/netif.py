"""
storlever.mngr.network.netif
~~~~~~~~~~~~~~~~

This module implements the class of network interface

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import time
import os

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
import ifconfig
from storlever.lib.confparse import properties


IFUP = "/sbin/ifup"
IFDOWN = "/sbin/ifdown"
IF_CONF_PATH = "/etc/sysconfig/network-scripts/"


class EthInterface(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self, name):

        self.name = name
        ifcfg_file_name = "ifcfg-" + name
        self.conf_file_path = os.path.join(IF_CONF_PATH, ifcfg_file_name)
        self.ifconfig_interface = ifconfig.Interface(name)

        # get the config file
        if os.path.exists(self.conf_file_path):
            self.conf = properties(self.conf_file_path)
        else:
            # create default if no config file
            ip = self.ifconfig_interface.ip
            mac = self.ifconfig_interface.mac
            netmask = self.ifconfig_interface.netmask
            up = self.ifconfig_interface.is_up()
            if up:
                onboot = "yes"
            else:
                onboot = "no"

            self.conf = properties(DEVICE=name,
                                   IPADDR=ip,
                                   NETMASK=netmask,
                                   BOOTPROTO="none",
                                   ONBOOT=onboot)
            # if physical, add HWADDR
            if self.ifconfig_interface.is_physical():
                self.conf["HWADDR"] = mac

    def get_ip_config(self):
        ip = self.conf.get("IPADDR", "")
        netmask = self.conf.get("NETMASK", "")
        gateway = self.conf.get("GATEWAY", "")
        return ip, netmask, gateway

    def set_ip_config(self, ip="", netmask="", gateway="", user="unknown"):
        self.conf["IPADDR"] = ip
        self.conf["NETMASK"] = netmask
        self.conf["GATEWAY"] = gateway
        self.conf["BOOTPROTO"] = "none"

        # write to config file
        self.conf.apply_to(self.conf_file_path)

        # restart this interface
        if self.ifconfig_interface.is_up():
            check_output([IFDOWN, self.name])
            check_output([IFUP, self.name])

        # log the operation
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Network interface (%s) is configured with (IP:%s, Netmask:%s, \
                 Gateway:%s) by user(%s)" %
                   (self.name, ip, netmask, gateway, user))

    def up(self, user="unknown"):

        self.conf["ONBOOT"] = "yes"
        self.save_conf()
        check_output([IFUP, self.name])

        # log the operation
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Network interface (%s) is up by user(%s)" %
                   (self.name, user))

    def down(self, user="unknown"):

        self.conf["ONBOOT"] = "no"
        self.save_conf()
        check_output([IFDOWN, self.name])

        # log the operation
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Network interface (%s) is up by user(%s)" %
                   (self.name, user))

    def save_conf(self):
        self.conf.apply_to(self.conf_file_path)

    @property
    def property_info(self):
        """return the property info of the interface

        This function would return a dict include the following keys:
        "up"  Bool    This interface is up in system or not
        "is_master" Bool this interface is the master of a bond group
        "is_slave" Bool this interface is slave of a bond group
        "mac" String mac address of interface

        """
        info = {"up": False,
                "is_master": False,
                "is_slave": False,
                "mac": self.ifconfig_interface.get_mac()}

        flags = self.ifconfig_interface.get_if_flags()
        if flags & ifconfig.IFF_UP:
            info["up"] = True
        if flags & ifconfig.IFF_SLAVE:
            info["is_slave"] = True
        if flags & ifconfig.IFF_MASTER:
            info["is_master"] = True

        return info

    @property
    def link_state(self):
        """return the current state of the net interface

        This function would return a dict include the following keys:
        "speed"  Int the speed the current link, if the link is down, it's 0
        "duplex" Bool the current link is duplex or not
        "auto"  Bool the interface support auto-negotiation or not
        "link_up" Bool the link is up or down

        """
        speed, duplex, auto, link_up = self.ifconfig_interface.get_link_info()

        state = {
            "speed": speed,
            "duplex": duplex,
            "auto": auto,
            "link_up": link_up,
        }

        return state

    @property
    def statistic_info(self):
        # get timestamp
        now = time.time()
        # if valid, get the statistic from system, or return a fake
        if self.ifconfig_interface is not None:
            stat = self.ifconfig_interface.get_stats()
        else:
            stat = {"rx_bytes":0, "rx_packets":0, "rx_errs":0, "rx_drop":0,
                    "rx_fifo":0, "rx_frame":0, "rx_compressed":0,
                    "rx_multicast":0, "tx_bytes":0, "tx_packets":0,
                    "tx_errs":0, "tx_drop":0, "tx_fifo":0, "tx_colls":0,
                    "tx_carrier":0, "tx_compressed":0}

        stat["time"] = now

        return stat


