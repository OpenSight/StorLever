"""
storlever.mngr.system.modulemgr
~~~~~~~~~~~~~~~~

This module implements some functions of storlever module management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import subprocess
import datetime
import time
import shutil
import re
import tarfile
import os

from storlever.lib.exception import StorLeverCmdError, StorLeverError
from storlever.lib.command import check_output
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal



MODULE_CONF_SCHEMA = Schema({

    "module_name":  Use(str),

    Optional("rpms"):  Default([Use(str)], default=[]),

    Optional("extra_files"):  Default([Use(str)], default=[]),

    Optional("comment"): Default(Use(str), default=""),

    DoNotCare(str): object  # for all those key we don't care
})

RPM_CMD = "/bin/rpm"

class ModuleManager(object):
    """contains all methods to manage the storlever cfg"""

    def __init__(self):
        self.managed_modules = {}
        self.module_schema = MODULE_CONF_SCHEMA

    def register_module(self, module_name, rpms=[], extra_files=[], comment="", *args, **kwargs):
        module_conf = {
            "module_name": module_name,
            "rpms": rpms,
            "extra_files": extra_files,
            "comment": comment
        }

        module_conf = self.module_schema.validate(module_conf)

        self.managed_modules[module_name] = module_conf

    def unregister_module(self, module_name):
        if module_name not in self.managed_modules:
            raise StorLeverError("Module(%s) Not Found" % (module_name), 404)
        del self.managed_modules[module_name]

    def get_modules_name_list(self):
        """ list all module in the storlever Manager layer
        """
        return self.managed_modules.keys()

    def get_module_info(self, module_name):
        """ get the specific module info/state in the storlever Manager layer
        """
        if module_name not in self.managed_modules:
            raise StorLeverError("Module(%s) Not Found" % (module_name), 404)
        module_conf = self.managed_modules[module_name]
        deps_info_list = []
        for rpm in module_conf["rpms"]:
            installed = True
            try:
                check_output([RPM_CMD, "-q", rpm])
            except StorLeverCmdError:
                installed = False
            deps_info_list.append({
                "name": rpm,
                "type": "rpm",
                "installed": installed
            })
        for file_path in module_conf["extra_files"]:
            deps_info_list.append({
                "name": file_path,
                "type": "file",
                "installed": os.path.exists(file_path)
            })

        module_info = {
            "module_name": module_conf["module_name"],
            "requires": deps_info_list,
            "comment": module_conf["comment"],
        }

        return module_info

ModuleManager = ModuleManager()

def module_mgr():
    """return the global cfg manager instance"""
    return ModuleManager






