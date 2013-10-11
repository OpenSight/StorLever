"""
storlever.mngr.system.servicemgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux service management.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import shutil
import datetime
import time


class SystemService(object):
    """represent the service in the system

    each object contains the service current state, and a set of methods
    to manage this service

    """
    def __init__(self, name):
        pass

    def get_state(self):
        pass

    def get_auto_start(self):
        pass

    def restart(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def enable_auto_start(self):
        pass

    def disable_auto_start(self):
        pass


class ServiceManager(object):
    """contains all methods to manage the user and group in linux system"""

    managed_service_list = [



    ]

    def __init__(self):
        pass

    def service_list(self):
        pass

    def get_service_by_name(self, name):
        pass




service_manager = ServiceManager()


def service_mgr():
    """return the global user manager instance"""
    return service_manager






