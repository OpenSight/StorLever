"""
storlever.rest.system
~~~~~~~~~~~~~~~~

This module implements the rest API for system.

:copyright: (c) 2013 by Jiankai Wang.
:license: GPLv3, see LICENSE for more details.

"""

import platform
import time

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
    config.add_route('disk_io_counters', '/system/disk_io_counters')
    config.add_route('per_disk_io_counters', '/system/per_disk_io_counters')
    config.add_route('net_io_counters', '/system/net_io_counters')
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
                    'cache_size': cpu["cache size"]}
        cpu_list_dict.append(cpu_info)
    return cpu_list_dict


@get_view(route_name='cpu_percent')
def system_cpu_percent_get(request):
    interval = float(request.params.get('interval', '1'))
    cpu_percent = psutil.cpu_percent(interval=interval)
    return cpu_percent


@get_view(route_name='per_cpu_percent')
def system_per_cpu_percent_get(request):
    interval = float(request.params.get('interval', '1'))
    per_cpu_percent_list = psutil.cpu_percent(interval=interval, percpu=True)
    return per_cpu_percent_list


@get_view(route_name='cpu_times')
def system_cpu_time_get(request):
    cpu_time = psutil.cpu_times()
    cpu_time_output = {'user': cpu_time.user,
                       'system': cpu_time.system,
                       'idle': cpu_time.idle,
                       'nice': cpu_time.nice,
                       'iowait': cpu_time.iowait,
                       'irq': cpu_time.irq,
                       'softirq': cpu_time.softirq,
                       'steal': cpu_time.steal,
                       'guest': cpu_time.guest}

    return cpu_time_output


@get_view(route_name='per_cpu_times')
def system_per_cpu_time_get(request):
    cpu_time_list = psutil.cpu_times(percpu=True)
    cpu_time_list_output = []
    for cpu_time in cpu_time_list:
        cpu_time_output = {'user': cpu_time.user,
                           'system': cpu_time.system,
                           'idle': cpu_time.idle,
                           'nice': cpu_time.nice,
                           'iowait': cpu_time.iowait,
                           'irq': cpu_time.irq,
                           'softirq': cpu_time.softirq,
                           'steal': cpu_time.steal,
                           'guest': cpu_time.guest}
        cpu_time_list_output.append(cpu_time_output)

    return cpu_time_list_output


@get_view(route_name='memory')
def system_memory_get(request):
    memory_info = psutil.virtual_memory()
    memory_info_output = {'total': memory_info.total,
                          'available': memory_info.available,
                          'percent': memory_info.percent,
                          'used': memory_info.used,
                          'free': memory_info.free,
                          'buffers': memory_info.buffers,
                          'cached': memory_info.cached}

    return memory_info_output



@get_view(route_name='disk_io_counters')
def system_disk_io_counters_get(request):
    io_counters = psutil.disk_io_counters()
    now = time.time()
    io_counters_output = {'time': now,
                          'disk_name': "all",
                          'read_count': io_counters.read_count,
                          'write_count': io_counters.write_count,
                          'read_bytes': io_counters.read_bytes,
                          'write_bytes': io_counters.write_bytes,
                          'read_time': io_counters.read_time,
                          'write_time': io_counters.write_time}

    return io_counters_output


@get_view(route_name='per_disk_io_counters')
def system_per_disk_io_counters_get(request):
    io_counters_dict = psutil.disk_io_counters(perdisk=True)
    now = time.time()
    io_counters_list_output = []
    for disk_name, io_counters in io_counters_dict.items():
        io_counters_output = {'time': now,
                              'disk_name': disk_name,
                              'read_count': io_counters.read_count,
                              'write_count': io_counters.write_count,
                              'read_bytes': io_counters.read_bytes,
                              'write_bytes': io_counters.write_bytes,
                              'read_time': io_counters.read_time,
                              'write_time': io_counters.write_time}
        io_counters_list_output.append(io_counters_output)

    return io_counters_list_output


@get_view(route_name='net_io_counters')
def system_net_io_counters_get(request):
    io_counters = psutil.net_io_counters()
    now = time.time()
    io_counters_output = {'time': now,
                          'if_name': "all",
                          'bytes_sent': io_counters.bytes_sent,
                          'bytes_recv': io_counters.bytes_recv,
                          'packets_sent': io_counters.packets_sent,
                          'packets_recv': io_counters.packets_recv,
                          'errin': io_counters.errin,
                          'errout': io_counters.errout,
                          'dropin': io_counters.dropin,
                          'dropout': io_counters.dropout}

    return io_counters_output


@get_view(route_name='per_net_io_counters')
def system_per_net_io_counters_get(request):
    io_counters_dict = psutil.net_io_counters(pernic=True)
    now = time.time()
    io_counters_list_output = []
    for nic_name, io_counters in io_counters_dict.items():
        io_counters_output = {'time': now,
                              'if_name': nic_name,
                              'bytes_sent': io_counters.bytes_sent,
                              'bytes_recv': io_counters.bytes_recv,
                              'packets_sent': io_counters.packets_sent,
                              'packets_recv': io_counters.packets_recv,
                              'errin': io_counters.errin,
                              'errout': io_counters.errout,
                              'dropin': io_counters.dropin,
                              'dropout': io_counters.dropout}
        io_counters_list_output.append(io_counters_output)

    return io_counters_list_output


@get_view(route_name='ps')
def system_ps_get(request):
    ps_list_output = []
    for proc in psutil.process_iter():
        now = time.time()
        io_counters = proc.get_io_counters()
        cpu_times = proc.get_cpu_times()
        memory_info = proc.get_memory_info()
        ps_output = {'pid': proc.pid,
                     'ppid': proc.ppid,
                     'name': proc.name,
                     'cmdline': proc.cmdline,
                     'nice': proc.get_nice(),
                     'status': str(proc.status),
                     'current_time': now,
                     'create_time': proc.create_time,
                     'user_time': cpu_times.user,
                     'system_time': cpu_times.system,
                     'vms': memory_info.vms,
                     'rss': memory_info.rss,
                     'memory_percent': proc.get_memory_percent(),
                     'read_count': io_counters.read_count,
                     'write_count': io_counters.write_count,
                     'read_bytes': io_counters.read_bytes,
                     'write_bytes': io_counters.write_bytes}
        ps_list_output.append(ps_output)

    return ps_list_output