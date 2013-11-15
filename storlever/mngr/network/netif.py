"""
storlever.mngr.network.netif
~~~~~~~~~~~~~~~~

This module implements the class of network interface

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import time

from storlever.lib.command import check_output
from storlever.lib import logger
import logging
import ifconfig
from storlever.lib.confparse import properties


IFUP = "/sbin/ifup"
IFDOWN = "/sbin/ifdown"


class NetInterface(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self, name, file_path, type="eth"):

        self.name = name
        self.type = type
        self.conf_file_path = file_path

        # get the config file
        self.conf = properties(file_path)

        # get the interface state object
        self.ifconfig_interface = ifconfig.findif(name)

    def get_type(self):
        return self.type

    def get_ip_config(self):
        ip = self.conf.get("IPADDR", "")
        netmask = self.conf.get("NETMASK", "")
        gateway = self.conf.get("GATEWAY", "")
        return (ip, netmask, gateway)

    def get_mac(self):
        if self.ifconfig_interface is not None:
            return self.ifconfig_interface.get_mac()
        else:
            return self.conf.get("HWADDR", "00:00:00:00:00:00")


    def set_ip_config(self, ip="", netmask="", gateway="", user="unknown"):
        self.conf["IPADDR"] = ip
        self.conf["NETMASK"] = netmask
        self.conf["GATEWAY"] = gateway

        # write to config file
        self.conf.apply_to(self.conf_file_path)

        # restart this interface
        if self.ifconfig_interface is not None and \
            self.ifconfig_interface.is_up():
            check_output([IFDOWN, self.name])
            check_output([IFUP, self.name])

        # log the operation
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Network interface (%s) is configured with (IP:%s, Netmask:%s, \
                 Gateway:%s) by user(%s)" %
                   (self.name, ip, netmask, gateway, user))

    def get_state_info(self):

        valid = False
        up = False
        speed = 0
        duplex = False
        auto = False
        link_up = False

        if self.ifconfig_interface is not None:
            valid = True
            up = self.ifconfig_interface.is_up()
            speed, duplex, auto, link_up = self.ifconfig_interface.get_link_info()

        return (valid, up, speed, duplex, auto, link_up)

    def get_statistic_info(self):
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








