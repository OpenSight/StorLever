"""
storlever.mngr.system.cfgrmgr
~~~~~~~~~~~~~~~~

This module implements some functions of storlever cfg management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import shutil
import datetime
import time


class CfgManager(object):
    """contains all methods to manage the storlever cfg"""

    def __init__(self):
        pass


cfg_manager = CfgManager()


def cfg_mgr():
    """return the global cfg manager instance"""
    return cfg_manager






