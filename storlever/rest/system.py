"""
storlever.rest.system
~~~~~~~~~~~~~~~~

This module implements the rest API for system.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import platform

import psutil

from storlever.rest.common import get_view, post_view, put_view, delete_view

from storlever.mngr.system import sysinfo


def includeme(config):
    config.add_route('cpu_list', '/system/cpu_list')
    config.add_route('uname', '/system/uname')
    config.add_route('cpu_percent', '/system/cpu_percent')
    config.add_route('per_cpu_percent', '/system/per_cpu_percent')
    config.add_route('cpu_times', '/system/cpu_times')
    config.add_route('per_cpu_times', '/system/per_cpu_times')
    config.add_route('memory', '/system/memory')
    config.add_route('ps', '/system/ps')
    config.add_route('disk_io_counter', '/system/disk_io_counter')
    config.add_route('per_disk_io_counters', '/system/per_disk_io_counters')
    config.add_route('net_io_counter', '/system/net_io_counter')
    config.add_route('per_net_io_counters', '/system/per_net_io_counters')


@get_view(route_name='uname')
def system_uname_get(request):
    sys_uname = platform.uname()
    sys_uname_dict = {'system': sys_uname[0],
                      'node': sys_uname[1],
                      'release': sys_uname[2],
                      'version': sys_uname[3],
                      'machine': sys_uname[4],
                      'processor': sys_uname[5]}
    return sys_uname_dict


@get_view(route_name='cpu_list')
def system_cpu_list_get(request):
    cpus = sysinfo.cpu_list()
    cpu_list_dict = []
    for cpu in cpus:
        cpu_info = {'processor': cpu["processor"],
                    'model_name': cpu["model name"],
                    'cpu_MHz': cpu["cpu MHz"],
                    'cache_size': cpu["cache size"],
                    'physical_id': cpu["physical id"]}
        cpu_list_dict.append(cpu_info)
    return cpu_list_dict
