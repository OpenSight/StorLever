"""
storlever.mngr.system.sysinfo
~~~~~~~~~~~~~~~~

This module implements some functions of sys infomation acquisition for mngr.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import subprocess
import shutil
import datetime
import time


LOG_DIR = "/var/log/"
LOG_FILE_PATH_PREFIX = "/tmp/syslog"


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
        subprocess.check_call(shell_cmd, shell=True)

    def tar_sys_log(self):
        """compress the whole system log directory to a temp"""

        # get current date time
        now_date = datetime.datetime.now()
        file_base_name = LOG_FILE_PATH_PREFIX + \
            ("_%d-%d-%d_%d-%d-%d" %
             (now_date.year, now_date.month, now_date.day,
              now_date.hour, now_date.minute, now_date.second))

        # archive the log dir to file
        file_path_name = shutil.make_archive(file_base_name, "gztar", "/", LOG_DIR)

        return file_path_name

    def poweroff(self):
        """shutdown the system"""
        subprocess.check_call("(sleep 1;/sbin/poweroff)&", shell=True)

    def reboot(self):
        """reboot the system"""
        subprocess.check_call("(sleep 1;/sbin/reboot)&", shell=True)

    def get_datetime(self):
        """get system date time string with iso8601 format"""
        return subprocess.check_output(["/bin/date", "-Iseconds"]).strip()

    def set_datetime(self, datetime_str):
        """set system date time by datetime_string"""

        # because linux date command cannot recognize iso 8601 format string with timezone,
        # change it with a valid format

        set_string = datetime_str.replace("T", " ")
        subprocess.check_output(["/bin/date", "-s%s" % set_string])
        subprocess.check_output(["/sbin/hwclock", "-w"])  # sync the system time to hw time

    def get_timestamp(self):
        """get the timestamp of the system"""
        return time.time()


sys_manager = SysManager()


def sys_mgr():
    """return the global system manager instance"""
    return sys_manager






