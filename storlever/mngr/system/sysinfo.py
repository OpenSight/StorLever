"""
storlever.mngr.sysinfo
~~~~~~~~~~~~~~~~

This module implements some functions of sys infomation acquisition for mngr.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""


def cpu_list():
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





