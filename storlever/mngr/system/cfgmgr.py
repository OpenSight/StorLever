"""
storlever.mngr.system.cfgrmgr
~~~~~~~~~~~~~~~~

This module implements some functions of storlever cfg management.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import shutil
import datetime
import time


cfg_manager = None


class CfgManager(object):
    """contains all methods to manage the storlever cfg"""

    def __init__(self):
        pass


def cfg_mgr():
    """return the global user manager instance"""
    global cfg_manager
    if cfg_manager is None:
        cfg_manager = CfgManager()
    return cfg_manager






