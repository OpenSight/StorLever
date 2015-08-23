"""
storlever.mngr.system.sysinfo
~~~~~~~~~~~~~~~~

This module implements some functions of sys infomation acquisition for mngr.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import datetime
import time
import tarfile
import os
from platform import linux_distribution
import socket

from storlever.lib import logger
from storlever.lib.command import check_output, write_file_entry
import logging
from storlever.lib.confparse import properties
from modulemgr import ModuleManager
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, AutoDel
from cfgmgr import cfg_mgr

MODULE_INFO = {
    "module_name": "system",
    "rpms": [
        "util-linux-ng",
        "upstart",
        "coreutils",
        "libselinux-utils",
        "net-tools"
        "setup"
    ],
    "comment": "Provides the fundamental functions of the low-lever system, "
               "like date, time, log, shutdown, reboot, and etc"
}


LOG_DIR = "/var/log"
LOG_FILE_PATH_PREFIX = "/tmp/syslog"

SELINUX_CONF_DIR = "/etc/selinux/"
SELINUX_CONF_FILE = "config"

ETC_HOSTS_FILE = "/etc/hosts"
ETC_NETWORK_FILE = "/etc/sysconfig/network"



HOST_LIST_SCHEMA = Schema([{
    "addr": Use(str),

    "hostname": Use(str),

    Optional("alias"): Default(Use(str), default=""),

    AutoDel(str): object  # for all other key we auto delete
}])

class SysManager(object):
    """contains all methods to manage the system"""

    def __init__(self):
        self.dist_name = None
        self.dist_version = None
        self.dist_id = None

    def system_restore_cb(self):
        self.set_hostname("localhost", "System Restore")

    def get_hostname(self):
        return socket.gethostname()

    def set_hostname(self, hostname, user="unknown"):
        # get old hostname
        old_hostname = self.get_hostname()

        # change hostname in system
        check_output(["/bin/hostname", hostname])

        # change hostname in /etc/sysconfig/network
        network_propeties = properties(HOSTNAME=hostname)
        network_propeties.apply_to(ETC_NETWORK_FILE)

        # add ip for this hostname
        host_list = self.get_host_list()
        exist = False
        for host in host_list:
            if host["hostname"] == old_hostname:
                host["hostname"] = hostname
                exist = True
        if not exist:
            # ipv4
            host_list.append({
                "addr": "127.0.0.1",
                "hostname": hostname,
                "alias": ""
            })
            # ipv6
            host_list.append({
                "addr": "::1",
                "hostname": hostname,
                "alias": ""
            })
        self.set_host_list(host_list, user=user)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "hostname is changed to %s by user(%s)" %
                   (hostname, user))

    def get_host_list(self):
        # add ip for this hostname
        if os.path.exists("/etc/hosts"):
            with open("/etc/hosts", "r") as f:
                lines = f.readlines()
        else:
            lines = []

        if "# begin storlever\n" not in lines:
            return []
        elif "# end storlever\n" not in lines:
            return []
        start = lines.index("# begin storlever\n") + 1
        end = lines.index("# end storlever\n")

        host_list = []
        for line in lines[start:end]:
            if line.strip().startswith("#"):
                continue
            elements = line.split()
            if len(elements) >= 3:
                alias = elements[2]
            else:
                alias = ""
            host_list.append({
                "addr": elements[0],
                "hostname": elements[1],
                "alias": alias
            })

        return host_list

    def set_host_list(self, host_list, user="unknown"):
        host_list = HOST_LIST_SCHEMA.validate(host_list)

        if os.path.exists(ETC_HOSTS_FILE):
            with open(ETC_HOSTS_FILE, "r") as f:
                lines = f.readlines()
        else:
            lines = []

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

        with open(ETC_HOSTS_FILE, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            for host in host_list:
                f.write("%s %s %s\n" % (
                    host["addr"],
                    host["hostname"],
                    host["alias"]
                ))
            f.write("# end storlever\n")
            f.writelines(after_storlever)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Host list is updated by user(%s)" % user)

    def get_dist_info(self):
        if self.dist_name is None:
            self.dist_name, self.dist_version, self.dist_id = \
                linux_distribution()
        return self.dist_name, self.dist_version, self.dist_id

    def get_cpu_list(self):
        """get every cpu info from system"""

        cpu = []
        cpu_info = {}
        f = open("/proc/cpuinfo")
        lines = f.readlines()
        f.close()
        for line in lines:
            if line == "\n":
                cpu.append(cpu_info)
                cpu_info = {}
            if len(line) < 2:
                continue
            name = line.split(':')[0].rstrip()
            var = line.split(':')[1]
            cpu_info[name] = var

        return cpu

    def rm_sys_log(self):
        """make use of rm cmd to delete all the existed sys log file"""

        shell_cmd = "/bin/rm -rf " + LOG_FILE_PATH_PREFIX + "*"
        check_output(shell_cmd, shell=True)

    def tar_sys_log(self):
        """compress the whole system log directory to a temp"""

        # get current date time
        now_date = datetime.datetime.now()
        file_path_name = LOG_FILE_PATH_PREFIX + \
            ("_%d-%d-%d_%d-%d-%d.tar.gz" %
             (now_date.year, now_date.month, now_date.day,
              now_date.hour, now_date.minute, now_date.second))

        # archive the log dir to file
        tar_file = tarfile.open(file_path_name, 'w:gz')
        try:
            tar_file.add(LOG_DIR)
        finally:
            tar_file.close()

        return file_path_name

    def poweroff(self, user="unknown"):
        """shutdown the system"""
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "system is powered off by user(%s)" % user)
        check_output("(sleep 1;/sbin/poweroff)&", shell=True)

    def reboot(self, user="unknown"):
        """reboot the system"""
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "system is rebooted by user(%s)" % user)
        check_output("(sleep 1;/sbin/reboot)&", shell=True)

    def get_datetime(self):
        """get system date time string with iso8601 format"""
        return check_output(["/bin/date", "-Iseconds"]).strip()

    def set_datetime(self, datetime_str, user="unknown"):
        """set system date time by datetime_string"""

        # because linux date command cannot recognize iso 8601 format string with timezone,
        # change it with a valid format

        set_string = datetime_str.replace("T", " ")
        check_output(["/bin/date", "-s%s" % set_string])
        check_output(["/sbin/hwclock", "-w"])  # sync the system time to hw time
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "system date time is update to %s by user(%s)" %
                   (datetime_str, user))

    def get_timestamp(self):
        """get the timestamp of the system"""
        return time.time()

    def flush_page_cache(self):
        """flush page cache from memory"""
        # sync
        check_output(["/bin/sync"])
        # clean cache
        write_file_entry("/proc/sys/vm/drop_caches", "3\n")

    def get_selinux_state(self):
        output = check_output(["/usr/sbin/getenforce"]).lower().strip()
        return output

    def set_selinux_state(self, state, user="unknown"):
        state_str_to_int = {
            "enforcing": 1,
            "permissive": 0,
            "disabled": 0
        }
        param = state_str_to_int.get(state)
        if param is not None:
            old_state = check_output(["/usr/sbin/getenforce"]).lower().strip()
            if old_state != "disabled":
                check_output(["/usr/sbin/setenforce", str(param)])

        if not os.path.exists(SELINUX_CONF_DIR):
            os.makedirs(SELINUX_CONF_DIR)
        conf_path = os.path.join(SELINUX_CONF_DIR, SELINUX_CONF_FILE)
        conf = properties()
        conf.delete("SELINUX")
        conf.apply_to(conf_path)
        with open(conf_path, "r") as f:
            content = f.read()
        if content.endswith("\n") or len(content) == 0:
            content += "SELINUX=%s\n" % state
        else:
            content += "\nSELINUX=%s\n" % state
        with open(conf_path, "w") as f:
            f.write(content)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "selinux state is set to %s by user(%s)" %
                   (state, user))


SysManager = SysManager()


cfg_mgr().register_config_file(ETC_HOSTS_FILE)
cfg_mgr().register_config_file(ETC_NETWORK_FILE)
cfg_mgr().register_system_restore_cb(SysManager.system_restore_cb)

ModuleManager.register_module(**MODULE_INFO)

def sys_mgr():
    """return the global system manager instance"""
    return SysManager






