"""
storlever.mngr.network.ifmgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux network interface management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""



from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging





class NetInterfaceManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        # need a mutex to provide thread-safe
        pass

    def _restart_network(self):
        pass

    def get_interface_by_name(self, name):
        pass

    def iter_interface(self):
        pass

    def remove_interface(self, name, user="unknown"):
        pass

    def add_bond_interface(self, name, user="unknown"):
        pass



interface_manager = NetInterfaceManager()


def if_mgr():
    """return the global user manager instance"""
    return interface_manager






