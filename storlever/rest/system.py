"""
storlever.rest.system
~~~~~~~~~~~~~~~~

This module implements the rest API for system.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import platform
import time
import os
from datetime import datetime

import psutil
from pyramid.response import FileResponse
from pyramid.response import Response

from storlever.rest.common import get_view, post_view, put_view, delete_view
from storlever.rest.common import get_params_from_request
from storlever.mngr.system import sysinfo
from storlever.mngr.system import usermgr
from storlever.mngr.system import servicemgr
from storlever.mngr.system import cfgmgr
from storlever.lib.schema import Schema, Optional, DoNotCare, \
    Use, IntVal, Default, SchemaError
from storlever.lib.exception import StorLeverError


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
    config.add_route('download_log', '/system/log_download')
    config.add_route('sys_poweroff', '/system/poweroff')
    config.add_route('sys_reboot', '/system/reboot')
    config.add_route('sys_datetime', '/system/datetime')
    config.add_route('sys_timestamp', '/system/timestamp')
    config.add_route('user_list', '/system/user_list')
    config.add_route('user_info', '/system/user_list/{user_name}')
    config.add_route('group_list', '/system/group_list')
    config.add_route('group_info', '/system/group_list/{group_name}')
    config.add_route('service_list', '/system/service_list')
    config.add_route('service_info', '/system/service_list/{service_name}')
    config.add_route('storlever_conf', '/system/conf_tar')
    config.add_route('backup_conf_to_file', '/system/backup_conf')
    config.add_route('restore_conf_from_file', '/system/restore_conf')



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
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    cpus = sys_mgr.cpu_list()
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


@get_view(route_name='download_log')
def download_log(request):
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    sys_mgr.rm_sys_log()   # rm the exist tar log file
    log_tar_file = sys_mgr.tar_sys_log()
    response = FileResponse(log_tar_file, request=request, content_type='application/force-download')
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % (os.path.basename(log_tar_file))
    return response


@post_view(route_name='sys_poweroff')
def sys_poweroff(request):
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    sys_mgr.poweroff(user=request.client_addr)
    return Response(status=200)


@post_view(route_name='sys_reboot')
def sys_reboot(request):
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    sys_mgr.reboot(user=request.client_addr)
    return Response(status=200)


@get_view(route_name='sys_datetime')
def get_datetime(request):
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    datetime_str = sys_mgr.get_datetime()
    return {'datetime': datetime_str}


@post_view(route_name='sys_datetime')
def set_datetime(request):
    params = get_params_from_request(request)
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    sys_mgr.set_datetime(params['datetime'], user=request.client_addr)
    return Response(status=200)


@get_view(route_name='sys_timestamp')
def get_timestamp(request):
    sys_mgr = sysinfo.sys_mgr()      # get sys manager
    timestamp = sys_mgr.get_timestamp()
    return {'timestamp': timestamp}


@get_view(route_name='user_list')
def get_user_list(request):
    user_mgr = usermgr.user_mgr()      # get user manager
    return user_mgr.user_list()


user_info_schema = Schema({
    "name": Use(unicode),     # name should be string
    Optional("uid"): Default(Use(int), default=-1),  # uid must int
    Optional("password"): Default(Use(unicode), default=""),  # uid must int
    Optional("comment"): Default(Use(unicode), default=""),  # comment must int,
    Optional("primay_group"): Default(Use(int), default=-1),  # primay_group must int
    Optional("groups"): Default(Use(unicode), default=""),  # comment must int,
    DoNotCare(str): object  # for all those key we don't care
})


@post_view(route_name='user_list')
def add_user(request):
    user_info = get_params_from_request(request)
    user_info = user_info_schema.validate(user_info)
    user_mgr = usermgr.user_mgr()
    user_mgr.user_add(user_info["name"], user_info["password"], user_info["uid"],
                      user_info["primay_group"], user_info["groups"],
                      user_info["comment"], user=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('user_info', user_name=user_info["name"])
    return resp


@get_view(route_name='user_info')
def get_user_info(request):
    user_name = request.matchdict["user_name"]
    user_mgr = usermgr.user_mgr()      # get user manager
    return user_mgr.get_user_info_by_name(user_name)


@put_view(route_name='user_info')
def mod_user_info(request):
    user_name = request.matchdict["user_name"]
    user_info = get_params_from_request(request)
    user_info["name"] = user_name
    user_info = user_info_schema.validate(user_info)
    user_mgr = usermgr.user_mgr()
    user_mgr.user_mod(user_info["name"], user_info["password"], user_info["uid"],
                      user_info["primay_group"], user_info["groups"],
                      user_info["comment"], user=request.client_addr)
    return Response(status=200)


@delete_view(route_name='user_info')
def del_user(request):
    user_name = request.matchdict["user_name"]
    user_mgr = usermgr.user_mgr()      # get user manager
    user_mgr.user_del_by_name(user_name, user=request.client_addr)
    return Response(status=200)


@get_view(route_name='group_list')
def get_group_list(request):
    user_mgr = usermgr.user_mgr()      # get user manager
    return user_mgr.group_list()


group_info_schema = Schema({
    "name": Use(unicode),     # name should be string
    Optional("gid"): Default(Use(int), default=-1),  # uid must int
    DoNotCare(str): object  # for all those key we don't care
})


@post_view(route_name='group_list')
def add_group(request):
    group_info = get_params_from_request(request)
    group_info = group_info_schema.validate(group_info)
    user_mgr = usermgr.user_mgr()
    user_mgr.group_add(group_info["name"], group_info["gid"],
                       user=request.client_addr)

    # generate 201 response
    resp = Response(status=201)
    resp.location = request.route_url('group_info', group_name=group_info["name"])
    return resp


@get_view(route_name='group_info')
def get_group_info(request):
    group_name = request.matchdict["group_name"]
    user_mgr = usermgr.user_mgr()      # get user manager
    return user_mgr.get_group_by_name(group_name)


@delete_view(route_name='group_info')
def del_group(request):
    group_name = request.matchdict["group_name"]
    user_mgr = usermgr.user_mgr()      # get user manager
    user_mgr.group_del_by_name(group_name, user=request.client_addr)
    return Response(status=200)


@get_view(route_name='service_list')
def get_service_list(request):
    service_mgr = servicemgr.service_mgr()      # get service manager
    return service_mgr.service_list()



@get_view(route_name='service_info')
def get_service_info(request):
    service_name = request.matchdict["service_name"]
    service_mgr = servicemgr.service_mgr()      # get service manager
    service = service_mgr.get_service_by_name(service_name)

    service_dict = {
        "name": service_name,
        "comment": service.comment,
        "state": str(service.get_state()),
        "auto_start": str(service.get_auto_start())
    }

    return service_dict


service_mod_schema = Schema({
    Optional("state"): Use(unicode),  # state must bool
    Optional("restart"): Use(unicode),  # restart must bool
    Optional("auto_start"): Use(unicode),  # auto_start must bool
    DoNotCare(str): object  # for all those key we don't care
})


@put_view(route_name='service_info')
def put_service(request):
    service_name = request.matchdict["service_name"]
    cmd = get_params_from_request(request)
    cmd = service_mod_schema.validate(cmd)

    service_mgr = servicemgr.service_mgr()      # get service manager
    service = service_mgr.get_service_by_name(service_name)

    if "state" in cmd:
        if cmd["state"] == "True":
            service.start(request.client_addr)
        elif cmd["state"] == "False":
            service.stop(request.client_addr)
    elif "restart" in cmd:
        if cmd["restart"] == "True":
            service.restart(request.client_addr)

    if "auto_start" in cmd:
        if cmd["auto_start"] == "True":
            service.enable_auto_start(request.client_addr)
        else:
            service.disable_auto_start(request.client_addr)

    return Response(status=200)


def remove_tmp_conf_file(request):
    os.remove(request.storlever_tmp_file)


@get_view(route_name='storlever_conf')
def download_conf(request):
    cfg_mgr = cfgmgr.cfg_mgr()      # get cfg manager

    # the tmp file name
    t = datetime.today().strftime("%Y%m%d_%H%M%S")
    request.storlever_tmp_file = "/tmp/storlever_conf_%s.tar.gz" % t

    cfg_mgr.backup_to_file(request.storlever_tmp_file)
    response = FileResponse(request.storlever_tmp_file,
                            request=request,
                            content_type='application/force-download')
    response.headers['Content-Disposition'] = \
        'attachment; filename=%s' % \
        (os.path.basename(request.storlever_tmp_file))

    request.add_finished_callback(remove_tmp_conf_file)  # remove the temp file

    return response


@post_view(route_name='storlever_conf')
def upload_conf(request):
    """
    upload a config file to storlever

    the html form must be like below:

<form action="..." method="post" accept-charset="utf-8" enctype="multipart/form-data">
    <label for="conf">conf</label>
    <input id="conf" name="conf" type="file" value="" />
    <input type="submit" value="submit" />
</form>

    """

    # the name of file input of HTML form must be "conf"
    input_file = request.POST['conf'].file

    t = datetime.today().strftime("%Y%m%d_%H%M%S")
    file_path = "/tmp/storlever_conf_%s.tar.gz" % t

    with open(file_path, 'wb') as output_file:
        # Finally write the data to a temporary file
        input_file.seek(0)
        while True:
            data = input_file.read(2 << 16)
            if not data:
                break
            output_file.write(data)

    cfg_mgr = cfgmgr.cfg_mgr()      # get cfg manager
    cfg_mgr.restore_from_file(file_path, user=request.client_addr)   # restore the config

    os.remove(file_path)

    return Response(status=200)


@post_view(route_name='backup_conf_to_file')
def backup_conf_to_file(request):

    params = get_params_from_request(request)

    # check params
    if "file" not in params:
        raise StorLeverError("\"file\" params must be given")

    cfg_mgr = cfgmgr.cfg_mgr()      # get cfg manager

    cfg_mgr.backup_to_file(params["file"])

    return Response(status=200)


@post_view(route_name='restore_conf_from_file')
def restore_conf_from_file(request):

    params = get_params_from_request(request)

    # check params
    if "file" not in params:
        raise StorLeverError("\"file\" params must be given")

    cfg_mgr = cfgmgr.cfg_mgr()      # get cfg manager

    cfg_mgr.restore_from_file(params["file"], user=request.client_addr)

    return Response(status=200)