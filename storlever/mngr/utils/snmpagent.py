"""
storlever.mngr.utils.snmpagent
~~~~~~~~~~~~~~~~

This module implements snmp agent configuration management.

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
    Default, DoNotCare, BoolVal, IntVal, AutoDel

from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr


SNMP_CONF_FILE_NAME = "snmp_conf.yaml"
SNMP_ETC_CONF_DIR = "/etc/snmp/"
SNMP_ETC_CONF_FILE = "snmpd.conf"


SNMP_MONITOR_CONF_SCHEMA = Schema({

    # monitor name
    "monitor_name": Use(str),

    # options to control the monitor's behavior,
    # see monitor options section of man snmpd.conf for more detail
    Optional("option"): Default(Use(str), default=""),

    # expression to check of this monitor,
    #  see monitor expression of man snmpd.conf for more detail
    "expression":  Use(str),

    AutoDel(str): object  # for all other key we auto delete
})



SNMP_SINK_CONF_SCHEMA = Schema({

    # address of the host to which send the trap
    "host": Use(str),

    # trap type, can only be set to trap/trap2/inform,
    # which would send SNMPv1 TRAPs, SNMPv2c TRAP2s,
    # or SNMPv2 INFORM notifications respectively
    Optional("type"): Default(Use(str), default="trap"),

    # community name used by this sink
    Optional("community"):  Default(Use(str), default="public"),

    AutoDel(str): object  # for all other key we auto delete
})

SNMP_COMMUNITY_CONF_SCHEMA = Schema({


    "community_name": Use(str),

    # if set to True, it would be forced to resolve the host name to
    # ipv6 address in DNS resolution
    Optional("ipv6"):  Default(BoolVal(), default=False),

    # restrict  access from the specified source.
    #  A restricted source  can either be a specific hostname (or address), or a subnet - repre-
    # sented  as  IP/MASK  (e.g.  10.10.10.0/255.255.255.0),  or   IP/BITS   (e.g.
    # 10.10.10.0/24), or the IPv6 equivalents.
    # if it's empty, it would give access to any system, that means "global" range
    Optional("source"): Default(Use(str), default=""),

    #  this field restricts access for that community to  the
    # subtree rooted at the given OID.
    # if it's empty, the whole tree would be access
    Optional("oid"): Default(Use(str), default=""),

    # if set to True, this commnunity can only read the oid tree.
    # Or, it can set the the oid tree
    Optional("read_only"):  Default(BoolVal(), default=False),

    AutoDel(str): object  # for all other key we auto delete
})


SNMP_CONF_SCHEMA = Schema({

    # set the system location,  system  contact  or  system  name  (sysLocation.0,
    # sysContact.0  and  sysName.0)  for the agent respectively.  Ordinarily these
    # objects are writeable via suitably authorized SNMP SET  requests if these object
    # are empty,  However, specifying one of these directives makes the corresponding object read-only,
    # and attempts to SET it will result in a notWritable error response.
    Optional("sys_location"):  Default(Use(str), default=""),
    Optional("sys_contact"):  Default(Use(str), default=""),
    Optional("sys_name"):  Default(Use(str), default=""),

    # defines  a  list  of  listening addresses(separated by commas), on which to receive incoming SNMP
    # requests.  See the section LISTENING ADDRESSES in the snmpd(8)  manual  page
    # for more information about the format of listening addresses.
    # if it's empty, it would be the default address and port
    Optional("agent_address"):  Default(Use(str), default=""),

    # specifies  the  default  SNMPv3  username,  to  be used when making internal
    # queries to retrieve any necessary information  (either  for  evaluating  the
    # monitored  expression,  or building a notification payload).  These internal
    # queries always use SNMPv3, even if normal querying  of  the  agent  is  done
    # using SNMPv1 or SNMPv2c.
    Optional("iquery_sec_name"): Default(Use(str), default="internaluser"),

    # monitor the interface link up and down
    Optional("link_up_down_notifications"): Default(BoolVal(), default=False),

    # enable the default monitors for system
    Optional("default_monitors"): Default(BoolVal(), default=False),

    # system 1 minutes load max threshold for default load monitor,
    # if it's 0, this monitor never report error
    Optional("load_max"): Default(Use(float), default=0),

    # swap space min threshold for default memory monitor, in kB
    Optional("swap_min"): Default(Use(int), default=16384),

    # disk space min percent for the default disk usage monitor, 0 means never report error
    Optional("disk_min_percent"): Default(IntVal(0, 99), default=0),

    Optional("community_list"):  Default([SNMP_COMMUNITY_CONF_SCHEMA], default=[]),

    Optional("trapsink_list"):  Default([SNMP_SINK_CONF_SCHEMA], default=[]),

    Optional("monitor_list"):  Default([SNMP_MONITOR_CONF_SCHEMA], default=[]),

    AutoDel(str): object  # for all other key we auto delete
})


class SnmpAgentManager(object):
    """contains all methods to manage NTP server in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, SNMP_CONF_FILE_NAME)
        self.monitor_conf_schema = SNMP_MONITOR_CONF_SCHEMA
        self.sink_conf_schema = SNMP_SINK_CONF_SCHEMA
        self.community_conf_schema = SNMP_COMMUNITY_CONF_SCHEMA
        self.snmp_conf_schema = SNMP_CONF_SCHEMA

    def _load_conf(self):
        snmp_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            snmp_conf = \
                Config.from_file(self.conf_file, self.snmp_conf_schema).conf
        else:
            snmp_conf = self.snmp_conf_schema.validate(snmp_conf)
        return snmp_conf

    def _save_conf(self, snmp_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, snmp_conf)

    def _global_conf_to_etc_lines(self, snmp_conf):
        result = ""
        if snmp_conf["sys_location"] != "":
            result += "sysLocation %s\n" % snmp_conf["sys_location"]
        if snmp_conf["sys_contact"] != "":
            result += "sysContact %s\n" % snmp_conf["sys_contact"]
        if snmp_conf["sys_name"] != "":
            result += "sysName %s\n" % snmp_conf["sys_name"]

        if snmp_conf["agent_address"] != "":
            result += "agentaddress %s\n" % snmp_conf["agent_address"]

        if snmp_conf["load_max"] == 0:
            result += "load 0\n"
        else:
            result += "load %.2f\n" % snmp_conf["load_max"]

        result += "swap %d\n" % snmp_conf["swap_min"]

        if snmp_conf["disk_min_percent"] != 0:
            result += "includeAllDisks %d" % snmp_conf["disk_min_percent"]
            result += "%\n"

        result += "createUser %s\n" % snmp_conf["iquery_sec_name"]
        result += "rwuser %s noauth\n" % snmp_conf["iquery_sec_name"]
        result += "iquerySecName %s\n" % snmp_conf["iquery_sec_name"]

        if snmp_conf["link_up_down_notifications"]:
            result += "linkUpDownNotifications yes\n"
        else:
            result += "linkUpDownNotifications no\n"

        if snmp_conf["default_monitors"]:
            result += "defaultMonitors yes\n"
        else:
            result += "defaultMonitors no\n"

        return result

    def _community_to_etc_line(self, community_conf):

        if community_conf["read_only"]:
            if community_conf["ipv6"]:
                line = "rocommunity6"
            else:
                line = "rocommunity"
        else:
            if community_conf["ipv6"]:
                line = "rwcommunity6"
            else:
                line = "rwcommunity"

        line += " " + community_conf["community_name"]

        if community_conf["source"] == "":
            line += " default"
        else:
            line += " " + community_conf["source"]

        line += " " + community_conf["oid"]

        line += "\n"

        return line

    def _trapsink_to_etc_line(self, sink_conf):

        if sink_conf["type"] == "trap":
            line = "trapsink"
        elif sink_conf["type"] == "trap2":
            line = "trap2sink"
        elif sink_conf["type"] == "inform":
            line = "informsink"
        else:
            line = "trapsink"

        line += " " + sink_conf["host"]

        line += " " + sink_conf["community"]

        line += "\n"

        return line

    def _monitor_to_etc_line(self, monitor_conf):

        line = "monitor"
        if monitor_conf["option"] != "":
            line += " " + monitor_conf["option"]
        line += " " + monitor_conf["monitor_name"]
        line += " " + monitor_conf["expression"]
        line += "\n"

        return line

    def _sync_to_system_conf(self, snmp_conf):

        if not os.path.exists(SNMP_ETC_CONF_DIR):
            os.makedirs(SNMP_ETC_CONF_DIR)

        # add storlever config to ntp.conf
        file_name = os.path.join(SNMP_ETC_CONF_DIR, SNMP_ETC_CONF_FILE)
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        # filter the sensitive lines
        new_lines = []
        for line in lines:
            lower_line = line.strip().lower()
            if lower_line.startswith("syslocation") or \
                    lower_line.startswith("syscontact") or \
                    lower_line.startswith("sysname") or \
                    lower_line.startswith("agentaddress") or \
                    lower_line.startswith("linkupdownnotifications") or \
                    lower_line.startswith("defaultmonitors") or \
                    lower_line.startswith("iquerysecname") or \
                    lower_line.startswith("agentsecname") or \
                    lower_line.startswith("load") or \
                    lower_line.startswith("swap") or \
                    lower_line.startswith("includealldisks"):
                continue
            new_lines.append(line)
        lines = new_lines

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

        with open(file_name, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            f.write(self._global_conf_to_etc_lines(snmp_conf))
            for community_conf in snmp_conf["community_list"]:
                f.write(self._community_to_etc_line(community_conf))
            for trap_sink_conf in snmp_conf["trapsink_list"]:
                f.write(self._trapsink_to_etc_line(trap_sink_conf))
            for monitor_conf in snmp_conf["monitor_list"]:
                f.write(self._monitor_to_etc_line(monitor_conf))
            f.write("# end storlever\n")
            f.writelines(after_storlever)

    def sync_to_system_conf(self):
        """sync the ntp conf to /etc/ntp.conf"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            snmp_conf = self._load_conf()
            self._sync_to_system_conf(snmp_conf)

    def system_restore_cb(self):
        """sync the ntp conf to /etc/ntp"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            snmp_conf = self._load_conf()
            self._sync_to_system_conf(snmp_conf)

    def get_basic_conf(self):
        with self.lock:
            snmp_conf = self._load_conf()

        not_allowed_keys = (
            "community_list",
            "trapsink_list",
            "monitor_list"
        )
        snmp_conf = filter_dict(snmp_conf, not_allowed_keys, True)

        return snmp_conf

    def set_basic_conf(self,  config={}, operator="unkown", **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)
        not_allowed_keys = (
            "community_list",
            "trapsink_list",
            "monitor_list"
        )
        config = filter_dict(config, not_allowed_keys, True)
        with self.lock:
            snmp_conf = self._load_conf()
            for name, value in config.items():
                if name in snmp_conf and value is not None:
                    snmp_conf[name] = value

            # check config conflict
            snmp_conf = self.snmp_conf_schema.validate(snmp_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP basic config is updated by operator(%s)" %
                   (operator))

    def get_community_list(self):
        with self.lock:
            snmp_conf = self._load_conf()
        return snmp_conf["community_list"]

    def get_community_conf(self, community_name):
        with self.lock:
            snmp_conf = self._load_conf()
        community_list = snmp_conf["community_list"]
        for community in community_list:
            if community["community_name"] == community_name:
                result_community = community
                break
        else:
            raise StorLeverError("Community(%s) not found" % (community_name), 404)

        return result_community

    def add_community_conf(self, community_name,
                           ipv6=False, source="", oid="", read_only=True,
                           operator="unknown"):
        new_community_conf = {
            "community_name": community_name,
            "ipv6": ipv6,
            "source": source,
            "oid": oid,
            "read_only": read_only,
        }
        new_community_conf = self.community_conf_schema.validate(new_community_conf)

        with self.lock:
            snmp_conf = self._load_conf()
            community_list = snmp_conf["community_list"]

            # check duplicate
            for community_conf in community_list:
                if community_conf["community_name"] == community_name:
                    raise StorLeverError("Community (%s) Already exist" % community_name, 400)

            community_list.append(new_community_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP New Community (%s) is added by operator(%s)" %
                   (community_name, operator))

    def del_community_conf(self, community_name, operator="unknown"):
        with self.lock:
            snmp_conf = self._load_conf()
            delete_community = None
            for community_conf in snmp_conf["community_list"]:
                if community_conf["community_name"] == community_name:
                    delete_community = community_conf
                    break
            else:
                raise StorLeverError("Community (%s) Not Found" % (community_name), 404)

            snmp_conf["community_list"].remove(delete_community)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP Community (%s) is deleted by operator(%s)" %
                   (community_name, operator))

    def update_community_conf(self, community_name,
                              ipv6=None, source=None, oid=None, read_only=None,
                              operator="unknown"):
        with self.lock:
            snmp_conf = self._load_conf()
            community_list = snmp_conf["community_list"]
            update_comunity_index = 0
            for index, community_conf in enumerate(community_list):
                if community_conf["community_name"] == community_name:
                    update_comunity_index = index
                    break
            else:
                raise StorLeverError("Community (%s) Not Found" % (community_name), 404)

            community_conf = community_list[update_comunity_index]

            if ipv6 is not None:
                community_conf["ipv6"] = ipv6
            if source is not None:
                community_conf["source"] = source
            if oid is not None:
                community_conf["oid"] = oid
            if read_only is not None:
                community_conf["read_only"] = read_only

            community_list[update_comunity_index] = \
                self.community_conf_schema.validate(community_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP Community (%s) config is updated by operator(%s)" %
                   (community_name, operator))

    def get_trap_sink_list(self):
        with self.lock:
            snmp_conf = self._load_conf()
        return snmp_conf["trapsink_list"]

    def set_trap_sink_list(self, trap_sink_list=[], operator="unknown"):
        trap_sink_list = Schema([self.sink_conf_schema]).validate(trap_sink_list)
        with self.lock:
            snmp_conf = self._load_conf()
            snmp_conf["trapsink_list"] = trap_sink_list
            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP trap sink list is updated by operator(%s)" %
                   operator)

    def get_monitor_list(self):
        with self.lock:
            snmp_conf = self._load_conf()
        return snmp_conf["monitor_list"]

    def get_monitor_conf(self, monitor_name):
        with self.lock:
            snmp_conf = self._load_conf()
        monitor_list = snmp_conf["monitor_list"]
        for monitor in monitor_list:
            if monitor["monitor_name"] == monitor_name:
                result_monitor = monitor
                break
        else:
            raise StorLeverError("monitor(%s) not found" % (monitor_name), 404)

        return result_monitor

    def add_monitor_conf(self, monitor_name, expression, option="",
                         operator="unknown"):

        new_monitor_conf = {
            "monitor_name": monitor_name,
            "expression": expression,
            "option": option,
        }
        new_monitor_conf = self.monitor_conf_schema.validate(new_monitor_conf)

        with self.lock:
            snmp_conf = self._load_conf()
            monitor_list = snmp_conf["monitor_list"]

            # check duplicate
            for monitor_conf in monitor_list:
                if monitor_conf["monitor_name"] == monitor_name:
                    raise StorLeverError("monitor_name (%s) Already exist" % monitor_name, 400)

            monitor_list.append(new_monitor_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP New Monitor (%s) is added by operator(%s)" %
                   (monitor_name, operator))

    def del_monitor_conf(self, monitor_name, operator="unknown"):
        with self.lock:
            snmp_conf = self._load_conf()
            for monitor_conf in snmp_conf["monitor_list"]:
                if monitor_conf["monitor_name"] == monitor_name:
                    break
            else:
                raise StorLeverError("Monitor (%s) Not Found" % (monitor_name), 404)

            snmp_conf["monitor_list"].remove(monitor_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP Monitor (%s) is deleted by operator(%s)" %
                   (monitor_name, operator))

    def update_monitor_conf(self, monitor_name, expression=None, option=None,
                                operator="unknown"):

        with self.lock:
            snmp_conf = self._load_conf()
            monitor_list = snmp_conf["monitor_list"]
            update_monitor_index = 0
            for index, monitor_conf in enumerate(monitor_list):
                if monitor_conf["monitor_name"] == monitor_name:
                    update_monitor_index = index
                    break
            else:
                raise StorLeverError("Monitor (%s) Not Found" % (monitor_name), 404)

            if expression is not None:
                monitor_conf["expression"] = expression
            if option is not None:
                monitor_conf["option"] = option

            monitor_list[update_monitor_index] = \
                self.monitor_conf_schema.validate(monitor_conf)

            # save new conf
            self._save_conf(snmp_conf)
            self._sync_to_system_conf(snmp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "SNMP Monitor (%s) config is updated by operator(%s)" %
                   (monitor_name, operator))

SnmpAgentManager = SnmpAgentManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(SnmpAgentManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(SnmpAgentManager.system_restore_cb)
service_mgr().register_service("snmpd", "snmpd", "/usr/sbin/snmpd", "SNMP Agent(NET-SNMP)")


def snmp_agent_mgr():
    """return the global user manager instance"""
    return SnmpAgentManager

