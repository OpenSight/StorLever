"""
storlever.mngr.system.servicemgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux service management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import re

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging


INIT_SCRIPT_DIR = "/etc/init.d/"
CHKCONFIG = "/sbin/chkconfig"
CHK_LEVEL = "3"
SET_CHK_LEVEL = "2345"


class SystemService(object):
    """represent the service in the system

    each object contains the service current state, and a set of methods
    to manage this service

    """
    def __init__(self, name, init_script, comment=""):
        self.name = name
        self.init_script = init_script
        self.comment = comment

    def get_state(self):
        with open("/dev/null") as null_file:
            ret = subprocess.call([INIT_SCRIPT_DIR + self.init_script,
                                   "status"], stdout=null_file,
                                  stderr=subprocess.STDOUT)
            if ret == 0:
                return True
            else:
                return False

    def get_auto_start(self):
        service_stat = check_output([CHKCONFIG, "--list", self.init_script])
        state_list = re.split("\s+", service_stat)
        for level_state in state_list:
            if CHK_LEVEL in level_state:
                level, dummy, state = level_state.partition(":")
                if state.strip() == "on":
                    return True
                else:
                    return False
        return False

    def restart(self, user="unkown"):
        check_output([INIT_SCRIPT_DIR + self.init_script, "restart"])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Service %s is restarted by user(%s)" % (self.name, user))

    def start(self, user="unkown"):
        check_output([INIT_SCRIPT_DIR + self.init_script, "start"])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Service %s is start by user(%s)" % (self.name, user))

    def stop(self, user="unkown"):
        check_output([INIT_SCRIPT_DIR + self.init_script, "stop"])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Service %s is start by user(%s)" % (self.name, user))

    def enable_auto_start(self, user="unkown"):
        check_output([CHKCONFIG, "--level", SET_CHK_LEVEL, self.init_script, "on"])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Service %s auto start is enabled by user(%s)" % (self.name, user))

    def disable_auto_start(self, user="unkown"):
        check_output([CHKCONFIG, "--level", SET_CHK_LEVEL, self.init_script, "off"])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Service %s auto start is disabled by user(%s)" % (self.name, user))


class ServiceManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        self.managed_services = {
        "sshd": {"comment": "SSH Server", "ps": "/sbin/sshd", "init": "sshd"},

    }

    def _get_chkconfig_output(self):
        service_list = check_output([CHKCONFIG, "--list"]).split("\n")
        chkconfig_output = {}
        for service_state in service_list:
            state_list = re.split("\s+", service_state)
            service_name = state_list[0]
            chkconfig_output[service_name] = {}
            for level_state in state_list[1:]:
                level, dummy, state = level_state.partition(":")
                chkconfig_output[service_name][level] = state

        return chkconfig_output

    def service_list(self):
        ps_out = check_output(["/bin/ps", "-ef"])
        chkconfig_out = self._get_chkconfig_output()
        output_list = []
        for service, params in self.managed_services.items():
            service_info = {
                "name": service,
                "comment": params["comment"],
                "state": params["ps"] in ps_out,
                "auto_start": chkconfig_out[params["init"]][CHK_LEVEL] == "on"
            }

            if params["ps"] == "":
                # slow path
                service = \
                    SystemService(service,
                                  self.managed_services[service]["init"],
                                  self.managed_services[service]["comment"])
                service_info["state"] = service.get_state();

            output_list.append(service_info)

        return output_list

    def get_service_by_name(self, name):
        if name in self.managed_services:
            return SystemService(name,
                                 self.managed_services[name]["init"],
                                 self.managed_services[name]["comment"])
        else:
            raise StorLeverError("service does not exist", 404)

    def register_service(self, name, init_script, ps_pattern="", comment=""):
        """register a service into service manager to handle.

        other module can register its self service to service manager, so that
        its associated service can be handled by service manager in a uniform
        approach. this method is not thread safe

        args:
        name: service name
        init_script: the init script name, it must be equal to the script base file name(no path)
                     which locate at /etc/init.d/
        ps_pattern: service manager use ps output to check the service state, if output cantain
                    this given pattern string, it's consider running. if pattern is "", manager
                    would use the init script to check its state which is much slower
        comment: service description
        """
        self.managed_services[name] = {
            "comment": comment,
            "ps": ps_pattern,
            "init": init_script,
        }


service_manager = ServiceManager()


def service_mgr():
    """return the global user manager instance"""
    return service_manager






