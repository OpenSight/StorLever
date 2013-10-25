"""
storlever.mngr.system.cfgrmgr
~~~~~~~~~~~~~~~~

This module implements some functions of storlever cfg management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import datetime
import time
import shutil
import re
import tarfile
import os

from storlever.lib.exception import StorLeverError


STORLEVER_CONF_DIR = "/etc/storlever"


class TarFilter(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __call__(self, tarinfo):
        if tarinfo.isdir():      # dir always include
            return tarinfo

        if self.pattern.match(tarinfo.name) is None:
            return None
        else:
            return tarinfo


class CfgManager(object):
    """contains all methods to manage the storlever cfg"""

    managed_config_files = [
        {"name": STORLEVER_CONF_DIR, "pattern": None},
        {"name": "/etc/passwd", "pattern": None},
        {"name": "/etc/shadow", "pattern": None},
        {"name": "/etc/group", "pattern": None},
        {"name": "/etc/gshadow", "pattern": None},
        {"name": "/etc/storlever_test", "pattern": None},  # for unit test

    ]

    def __init__(self):
        pass

    def backup_to_file(self, filename):
        self.check_conf_dir()     # make sure config dir exist
        tar_file = tarfile.open(filename, 'w:gz')
        for config_file in CfgManager.managed_config_files:
            if os.path.exists(config_file.get("name")):
                if config_file.get("pattern") is None:
                    tar_file.add(config_file["name"])
                else:
                    filter = TarFilter(config_file["pattern"])
                    tar_file.add(config_file["name"], filter=filter)
        tar_file.close()

    def restore_from_file(self, filename):
        tar_file = tarfile.open(filename, 'r')
        tar_file.extractall("/")
        tar_file.close()

    def check_conf_dir(self):
        """check the root conf dir for storlever exist or not

        If it does not exist, make it at once

        """
        if not os.path.isdir(STORLEVER_CONF_DIR):
            if os.path.exists(STORLEVER_CONF_DIR):
                raise StorLeverError("storlever conf path(%) is not a directory" % STORLEVER_CONF_DIR)
            else:
                os.makedirs(STORLEVER_CONF_DIR)

    def _clear_conf_dir(self):
        shutil.rmtree(STORLEVER_CONF_DIR, True)

    def system_restore(self):
        self._clear_conf_dir()

        # invoke the other module's interface to restore


cfg_manager = CfgManager()


def cfg_mgr():
    """return the global cfg manager instance"""
    return cfg_manager






