"""
storlever.mngr.utils.smartdmgr
~~~~~~~~~~~~~~~~

This module implements smartd configuration management

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path
from stat import *

from storlever.lib.config import Config
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
from storlever.lib.utils import filter_dict
import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal, ListVal, AutoDel
from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "smartd",
    "rpms": [
        "smartmontools"
    ],
    "comment": "Provides the management of smartd configuration"
}


SMARTD_CONF_FILE_NAME = "smartd_conf.yaml"
SMARTD_ETC_CONF_DIR = "/etc/"
SMARTD_CONF_FILE = "smartd.conf"


MONITOR_CONF_SCHEMA = Schema({

    # the dev's file to monitor
    "dev":  Use(str),

    # the (e)mail address to which smartd would send when a error is detected.
    #  To  send email to more than one user, please use the following "comma separated"
    # form for the address: user1@add1,user2@add2,...,userN@addN (with no spaces).
    Optional("mail_to"): Default(Use(str), default=""),

    # test the mail. if true, send a single test email immediately upon smartd  startup.
    # This  allows one to verify that email is delivered correctly
    Optional("mail_test"): Default(BoolVal(), default=False),

    # run the executable PATH instead of the default mail command.
    # if this list is empty, smartd would run the default "/bin/mail" utility
    # to send warning email to user in "mail_to" option. Otherwise, smartd would run
    # the scripts in this option. See man smartd.conf
    # for more detail
    Optional("mail_exec"): Default(Use(str), default=""),

    # Run Self-Tests or Offline Immediate Tests,  at  scheduled  times.   A  Self-  or
    # Offline Immediate Test will be run at the end of periodic device polling, if all
    # 12 characters of the string T/MM/DD/d/HH match the extended  regular  expression
    # REGEXP. See man smartd.conf for detail.
    # if this option is empty, no schedule test at all
    Optional("schedule_regexp"): Default(Use(str), default=""),

    AutoDel(str): object  # for all other key we auto delete
})


SMARTD_FCONF_SCHEMA = Schema({
    Optional("monitor_list"): Default([MONITOR_CONF_SCHEMA], default=[]),
    AutoDel(str): object  # for all other key we auto delete
})

class SmartdManager(object):
    """contains all methods to manage NTP server in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, SMARTD_CONF_FILE_NAME)
        self.smartd_conf_schema = SMARTD_FCONF_SCHEMA
        self.smartd_monitor_conf_schema = MONITOR_CONF_SCHEMA

    def _load_conf(self):
        smartd_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            smartd_conf = \
                Config.from_file(self.conf_file, self.smartd_conf_schema).conf
        else:
            smartd_conf = self.smartd_conf_schema.validate(smartd_conf)
        return smartd_conf

    def _save_conf(self, smartd_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, smartd_conf)

    def _monitor_to_file_line(self, monitor_conf):

        monitor_line = monitor_conf["dev"]
        monitor_line += " -a"
        if monitor_conf["schedule_regexp"] != "":
            monitor_line += " -s %s" % monitor_conf["schedule_regexp"]

        if monitor_conf["mail_to"] != "":
            monitor_line += " -m %s" % monitor_conf["mail_to"]

            if monitor_conf["mail_test"]:
                monitor_line += " -M test"
        else:

            if monitor_conf["mail_exec"] != "":
                monitor_line += " -m <nomailer>"

                if monitor_conf["mail_test"]:
                    monitor_line += " -M test"

        if monitor_conf["mail_exec"] != "":
            monitor_line += " -M exec %s" % monitor_conf["mail_exec"]

        monitor_line += "\n"

        return monitor_line


    def _sync_to_system_conf(self, smartd_conf):

        if not os.path.exists(SMARTD_ETC_CONF_DIR):
            os.makedirs(SMARTD_ETC_CONF_DIR)

        smartd_etc_file = os.path.join(SMARTD_ETC_CONF_DIR, SMARTD_CONF_FILE)
        with open(os.path.join(smartd_etc_file, ), "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines[:]):
            if line.strip().startswith("DEVICESCAN"):
                lines[i] = "#" + line

        if "# begin storlever\n" in lines:
            before_storlever = lines[0:lines.index("# begin storlever\n")]
        else:
            before_storlever = lines[0:]
            if before_storlever and (not before_storlever[-1].endswith("\n")):
                before_storlever[-1] += "\n"

        if "# end storlever\n" in lines:
            after_storlever = lines[lines.index("# end storlever\n") + 1:]
        else:
            after_storlever = []

        with open(smartd_etc_file, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            for monitor_conf in smartd_conf["monitor_list"]:
                f.write(self._monitor_to_file_line(monitor_conf))
            f.write("# end storlever\n")
            f.writelines(after_storlever)



    def sync_to_system_conf(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp.conf"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            smartd_conf = self._load_conf()
            self._sync_to_system_conf(smartd_conf)

    def system_restore_cb(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            smartd_conf = self._load_conf()
            self._sync_to_system_conf(smartd_conf)

    def get_monitor_list(self):
        with self.lock:
            smartd_conf = self._load_conf()

        monitor_list = smartd_conf["monitor_list"]
        for i, monitor_conf in enumerate(monitor_list[:]):
            monitor_list[i] = filter_dict(monitor_conf, ("dev", "mail_to",
                                                         "mail_test", "mail_exec",
                                                         "schedule_regexp"))

        return monitor_list

    def set_monitor_list(self, monitor_list=[], operator="unkown"):

        monitor_list = Schema([self.smartd_monitor_conf_schema]).validate(monitor_list)
        for i, monitor_conf in enumerate(monitor_list[:]):
            monitor_list[i] = filter_dict(monitor_conf, ("dev", "mail_to",
                                                         "mail_test", "mail_exec",
                                                         "schedule_regexp"))
        with self.lock:
            smartd_conf = self._load_conf()
            smartd_conf["monitor_list"] = monitor_list

            # check validation
            for monitor_conf in smartd_conf["monitor_list"]:
                if not os.path.exists(monitor_conf["dev"]):
                    raise StorLeverError("Device (%s) not found" % (monitor_conf["dev"]), 404)
                else:
                    mode = os.stat(monitor_conf["dev"])[ST_MODE]
                    if not S_ISBLK(mode):
                        raise StorLeverError("Device (%s) not block device" % (monitor_conf["dev"]), 400)

                if monitor_conf["mail_exec"] != "" and not os.paht.exists(monitor_conf["mail_exec"]):
                    raise StorLeverError("mail_exec (%s) not found" % (monitor_conf["mail_exec"]), 404)

            # save new conf
            self._save_conf(smartd_conf)
            self._sync_to_system_conf(smartd_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Smartd monitor list is updated by operator(%s)" %
                   (operator))

SmartdManager = SmartdManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(SmartdManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(SmartdManager.system_restore_cb)
service_mgr().register_service("smartd", "smartd", "/usr/sbin/smartd",
                               "Monitor the hard drives which support SMART technology")
ModuleManager.register_module(**MODULE_INFO)

def smartd_mgr():
    """return the global user manager instance"""
    return SmartdManager

