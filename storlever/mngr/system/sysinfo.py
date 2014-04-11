"""
storlever.mngr.system.sysinfo
~~~~~~~~~~~~~~~~

This module implements some functions of sys infomation acquisition for mngr.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import datetime
import time
import tarfile
import os

from storlever.lib import logger
from storlever.lib.command import check_output, write_file_entry
import logging
from storlever.lib.confparse import properties

LOG_DIR = "/var/log"
LOG_FILE_PATH_PREFIX = "/tmp/syslog"

SELINUX_CONF_DIR = "/etc/selinux/"
SELINUX_CONF_FILE = "config"


class SysManager(object):
    """contains all methods to manage the system"""

    def __init__(self):
        pass

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


def sys_mgr():
    """return the global system manager instance"""
    return SysManager






