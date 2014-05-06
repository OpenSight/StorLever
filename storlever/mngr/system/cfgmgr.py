"""
storlever.mngr.system.cfgmgr
~~~~~~~~~~~~~~~~

This module implements some functions of storlever cfg management.

:copyright: (c) 2014 by OpenSight (opensight.com.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import subprocess
import datetime
import time
import shutil
import re
import tarfile
import os

from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
from modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "config",
    "rpms": [
    ],
    "comment": "Provides the configure management for storlever, "
               "like reset/backup/restore"
}



STORLEVER_CONF_DIR = "/etc/storlever"


class TarFilter(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __call__(self, filename):
        if os.path.isdir(filename):      # dir always include
            return False
        base_name = os.path.basename(filename)
        if self.pattern.match(base_name) is None:
            return True
        else:
            return False


class CfgManager(object):
    """contains all methods to manage the storlever cfg"""

    def __init__(self):
        self.managed_config_files = [
            {"name": STORLEVER_CONF_DIR, "pattern": None},
            {"name": "/etc/passwd", "pattern": None},
            {"name": "/etc/shadow", "pattern": None},
            {"name": "/etc/group", "pattern": None},
            {"name": "/etc/gshadow", "pattern": None},
            {"name": "/etc/storlever_test", "pattern": None},  # for unit test
        ]
        self.restore_from_file_cb = []
        self.system_restore_cb = []

    def register_config_file(self, file_name, pattern=None):
        """register a config to cfg mananger

        Other module can register its config file(except in STORLEVER_CONF_DIR) to cfg manager
        so that cfg manager can take this file into its process including backup/restore cfg.

        args:
        file_name: file/directory path name(include the absolute path, like "etc/passwd")
        pattern: if present, cfg manager would filter the file in the path base on it,
                 it must be a regular expression
        """
        self.managed_config_files.append({"name": file_name, "patten": pattern})

    def register_restore_from_file_cb(self, fun):
        """ register a callback function after cfg manager restore the config from file
        """
        self.restore_from_file_cb.append(fun)

    def register_system_restore_cb(self, fun):
        """register a callback function after cfg manager perform a system restore
        """
        self.system_restore_cb.append(fun)

    def _del_all_config_files(self):
        for config_file in self.managed_config_files:
            file_name = config_file["name"]
            pattern = config_file["pattern"]

            if os.path.exists(file_name):
                if pattern is None:
                    if os.path.isfile(file_name):
                        os.remove(file_name)
                    elif os.path.isdir(file_name):
                        shutil.rmtree(file_name)
                else:
                    cp = re.compile(pattern)
                    if os.path.isfile(file_name):
                        if cp.match(file_name):
                            os.remove(file_name)
                    elif os.path.isdir(file_name):
                        for path, subdirs, files in os.walk(file_name):
                            for name in files:
                                if cp.match(name):
                                    os.remove(os.path.join(path, name))

    def backup_to_file(self, filename):

        # check input filename
        if not os.path.isdir(os.path.dirname(filename)):
            raise StorLeverError("File path (%s) does not exist" % os.path.dirname(filename), 400)

        self.check_conf_dir()     # make sure config dir exist

        tar_file = tarfile.open(filename, 'w:gz')
        for config_file in self.managed_config_files:
            if os.path.exists(config_file.get("name")):
                if config_file.get("pattern") is None:
                    tar_file.add(config_file["name"])
                else:
                    filter = TarFilter(config_file["pattern"])
                    tar_file.add(config_file["name"], exclude=filter)
        tar_file.close()

    def restore_from_file(self, filename, user="unkown"):

        # check input file
        if not os.path.exists(filename):
            raise StorLeverError("File (%s) does not exist" % filename, 400)
        if not tarfile.is_tarfile(filename):
            raise StorLeverError("File (%s) is not a config archive" % filename, 400)

        self._del_all_config_files()
        tar_file = tarfile.open(filename, 'r')
        tar_file.extractall("/")
        tar_file.close()

        # call the register callback function for restore config
        for callback in self.restore_from_file_cb:
            callback()

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Storlever conf is restored from file by user(%s)" % user)		

    def check_conf_dir(self):
        """check the root conf dir for storlever exist or not

        If it does not exist, make it at once

        """
        if not os.path.isdir(STORLEVER_CONF_DIR):
            if os.path.exists(STORLEVER_CONF_DIR):
                raise StorLeverError("storlever conf path(%s) is not a directory" % STORLEVER_CONF_DIR)
            else:
                os.makedirs(STORLEVER_CONF_DIR)

    def _clear_conf_dir(self):
        shutil.rmtree(STORLEVER_CONF_DIR, True)

    def system_restore(self, user="unkown"):

        # call the register callback function for system_restore
        for callback in self.system_restore_cb:
            callback()

        self._clear_conf_dir()

        # invoke the other module's interface to restore
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Storlever system is totally restored by user(%s)" % user)			


CfgManager = CfgManager()

ModuleManager.register_module(**MODULE_INFO)

def cfg_mgr():
    """return the global cfg manager instance"""
    return CfgManager






