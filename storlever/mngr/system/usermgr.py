"""
storlever.mngr.system.usermgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux user management.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import shutil
import datetime
import time


user_manager = None


class UserManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        pass


def user_mgr():
    """return the global user manager instance"""
    global user_manager
    if user_manager is None:
        user_manager = UserManager()
    return user_manager






