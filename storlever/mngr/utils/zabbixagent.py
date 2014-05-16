"""
storlever.mngr.utils.ntpmgr
~~~~~~~~~~~~~~~~

This module implements ntp server management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path
import subprocess

from storlever.lib.config import Config
from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
from storlever.lib.utils import filter_dict
import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal
from storlever.lib.confparse import properties
from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "zabbix_agent",
    "rpms": [
        "zabbix-agent"
    ],
    "comment": "Provides the support of zabbix agent config for storlever"
}


ZABBIX_AGENT_CONF_FILE_NAME = "zabbix_agentd_conf.yaml"
ZABBIX_AGENT_ETC_CONF_DIR = "/etc/zabbix/"
ZABBIX_AGENT_CONF_FILE = "zabbix_agentd.conf"



ZABBIX_AGENT_CONF_SCHEMA = Schema({


    Optional("hostname"):  Default(Use(str), default=""),

    # How often list of active checks is refreshed, in seconds.
    # Note that after failing to refresh active checks the next refresh
    # will be attempted after 60 seconds.
    Optional("refresh_active_check"): Default(IntVal(min=60, max=3600), default=120),


    # the server ip:port list for active check.zabbix_agent would get the active check list
    # from each server at the refresh_active_check frequency. Entry string Format is IP:PORT
    Optional("active_check_server_list"):  Default([Use(str)], default=[]),

    # the server ip list for passive check. each passive check's source ip must
    # exist in this list. Entry string Format is IP
    Optional("passive_check_server_list"):  Default([Use(str)], default=[]),


    DoNotCare(str): object  # for all those key we don't care
})


class ZabbixAgentManager(object):
    """contains all methods to manage NTP server in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, ZABBIX_AGENT_CONF_FILE_NAME)
        self.zabbix_agentd_conf_schema = ZABBIX_AGENT_CONF_SCHEMA

    def _load_conf(self):
        zabbix_agent_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            zabbix_agent_conf = \
                Config.from_file(self.conf_file, self.zabbix_agentd_conf_schema).conf
        else:
            zabbix_agent_conf = self.zabbix_agentd_conf_schema.validate(zabbix_agent_conf)
        return zabbix_agent_conf

    def _save_conf(self, zabbix_agent_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, zabbix_agent_conf)


    def _sync_to_system_conf(self, zabbix_agent_conf):

        if not os.path.exists(ZABBIX_AGENT_ETC_CONF_DIR):
            os.makedirs(ZABBIX_AGENT_ETC_CONF_DIR)

        # conf file
        zabbix_agent_property = properties()

        # active server
        if zabbix_agent_conf["active_check_server_list"]:
            zabbix_agent_property["ServerActive"] = \
                ",".join(zabbix_agent_conf["active_check_server_list"])
        else:
            zabbix_agent_property.delete("ServerActive")

        # Server
        server_list = list(zabbix_agent_conf["passive_check_server_list"])
        if not server_list:
            server_list.append("127.0.0.1")
        zabbix_agent_property["Server"] = ",".join(server_list)

        # hostname
        if zabbix_agent_conf["hostname"] == "":
            zabbix_agent_property.delete("Hostname")
        else:
            zabbix_agent_property["Hostname"] = zabbix_agent_conf["hostname"]

        # RefreshActiveChecks
        zabbix_agent_property["RefreshActiveChecks"] = str(zabbix_agent_conf["refresh_active_check"])

        etc_conf_file = os.path.join(ZABBIX_AGENT_ETC_CONF_DIR, ZABBIX_AGENT_CONF_FILE)
        zabbix_agent_property.apply_to(etc_conf_file)


    def sync_to_system_conf(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp.conf"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            zabbix_agent_conf = self._load_conf()
            self._sync_to_system_conf(zabbix_agent_conf)

    def system_restore_cb(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            zabbix_agent_conf = self._load_conf()
            self._sync_to_system_conf(zabbix_agent_conf)


    def set_agent_conf(self, config={}, operator="unkown", *args, **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)
        not_allow_keys = (
            "active_check_server_list",
            "passive_check_server_list"
        )
        config = filter_dict(config, not_allow_keys, True)

        with self.lock:
            zabbix_agent_conf = self._load_conf()
            for name, value in config.items():
                if name in zabbix_agent_conf and value is not None:
                    zabbix_agent_conf[name] = value

            # check config conflict
            zabbix_agent_conf = self.zabbix_agentd_conf_schema.validate(zabbix_agent_conf)

            # save new conf
            self._save_conf(zabbix_agent_conf)
            self._sync_to_system_conf(zabbix_agent_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Zabbix agent config is updated by operator(%s)" %
                   (operator))

    def get_agent_conf(self, *args, **kwargs):
        with self.lock:
            zabbix_agent_conf = self._load_conf()

        not_allow_keys = (
            "active_check_server_list",
            "passive_check_server_list"
        )
        zabbix_agent_conf = filter_dict(zabbix_agent_conf, not_allow_keys, True)

        return zabbix_agent_conf

    def get_passive_check_server_list(self, *args, **kwargs):
        with self.lock:
            zabbix_agent_conf = self._load_conf()
        return zabbix_agent_conf["passive_check_server_list"]

    def set_passive_check_server_list(self, servers=[], operator="unkown", *args, **kwargs):
        with self.lock:
            zabbix_agent_conf = self._load_conf()
            zabbix_agent_conf["passive_check_server_list"] = servers
            # check config conflict
            zabbix_agent_conf = self.zabbix_agentd_conf_schema.validate(zabbix_agent_conf)

            # save new conf
            self._save_conf(zabbix_agent_conf)
            self._sync_to_system_conf(zabbix_agent_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Zabbix agent passive server list is updated by operator(%s)" %
                   (operator))

    def get_active_check_server_list(self, *args, **kwargs):
        with self.lock:
            zabbix_agent_conf = self._load_conf()
        return zabbix_agent_conf["active_check_server_list"]


    def set_active_check_server_list(self, servers=[], operator="unkown",
                                     *args, **kwargs):
        with self.lock:
            zabbix_agent_conf = self._load_conf()
            zabbix_agent_conf["active_check_server_list"] = servers
            # check config conflict
            zabbix_agent_conf = self.zabbix_agentd_conf_schema.validate(zabbix_agent_conf)

            # save new conf
            self._save_conf(zabbix_agent_conf)
            self._sync_to_system_conf(zabbix_agent_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Zabbix agent active server list is updated by operator(%s)" %
                   (operator))

ZabbixAgentManager = ZabbixAgentManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(ZabbixAgentManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(ZabbixAgentManager.system_restore_cb)
service_mgr().register_service("zabbix-agent", "zabbix-agent", "/usr/sbin/zabbix_agentd",
                               "zabbix agent for system/network monitor")
ModuleManager.register_module(**MODULE_INFO)

def zabbix_agent_mgr():
    """return the global user manager instance"""
    return ZabbixAgentManager

