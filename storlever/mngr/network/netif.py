"""
storlever.mngr.network.netif
~~~~~~~~~~~~~~~~

This module implements the class of network interface

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""



from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
import ifconfig



class NetInterface(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self, name, file):

        self.name = name
        # get the config file

        # get the interface state object
        self.ifconfig_interface = ifconfig.findif(name)

    def get_type(self):
        pass

    def get_ip_config(self):
        pass

    def set_ip_config(self, user="unknown"):
        pass

    def get_state_info(self):
        pass

    def get_statistic_info(self):
        pass








