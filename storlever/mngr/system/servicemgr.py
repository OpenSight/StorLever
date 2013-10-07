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


service_manager = None


class ServiceManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        pass


def service_mgr():
    """return the global user manager instance"""
    global service_manager
    if service_manager is None:
        service_manager = ServiceManager()
    return service_manager






