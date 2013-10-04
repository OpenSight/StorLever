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


LOG_DIR = "/var/log/"
LOG_FILE_PATH_PREFIX = "/tmp/syslog"

sys_manager = None


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
        subprocess.call(shell_cmd, shell=True)

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


def sys_mgr():
    """return the global system manager instance"""
    global sys_manager
    if sys_manager is None:
        sys_manager = SysManager()
    return sys_manager






