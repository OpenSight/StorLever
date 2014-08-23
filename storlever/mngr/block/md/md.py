"""
storlever.mngr.block.md.md
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lvm manager of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import logging

from storlever.lib.command import check_output
from storlever.lib.lock import lock as lock_factory
from storlever.lib.exception import StorLeverError
from storlever.lib import logger


MODULE_INFO = {
    "module_name": "soft raid",
    "rpms": [
        "mdadm"
    ],
    "comment": "Provides the management functions of software raid (md) in OS"
}


class MDManager(object):
    def __init__(self):
        self.lock = lock_factory()

    def get_all_md(self):
        return MDs(self.lock)

class MDs():
    def __init__(self, lock):
        self.raid_list = self._list_raid()
        self._detail = {}
        self._lock = lock

    def refresh(self):
        self.raid_list = self._list_raid()
        self._detail = {}

    def _list_raid(self):
        ret = {}
        for line in check_output('/sbin/mdadm --detail --scan'.split()).splitlines():
            if ' ' not in line:
                continue
            comps = line.split()
            device = comps[1]
            ret[os.path.basename(device)] = {"dev_file": device}
            for comp in comps[2:]:
                key = comp.split('=')[0].lower()
                value = comp.split('=')[1]
                ret[device][key] = value
        return ret

    def _update_mdadm_conf(self):
        # after create or delete md raid, /etc/mdadm.conf should be updated
        # otherwise after reboot, existing md will be renamed by kernel
        update_cmd = '/sbin/mdadm --examine --scan > /etc/mdadm.conf'
        check_output(update_cmd, shell=True)

    def get_md(self, md_device):
        if md_device not in self._detail:
            self._detail[md_device] = MD(md_device, self._lock)
        return self._detail[md_device]

    def delete(self, md_device):
        '''
        Destroy a RAID device.

        WARNING This will zero the superblock of all members of the RAID array..

        CLI Example:

        .. code-block:: bash

        salt '*' raid.destroy /dev/md0
        '''
        md = MD(md_device, self._lock)

        stop_cmd = '/sbin/mdadm --stop {0}'.format(md_device)
        zero_cmd = '/sbin/mdadm --zero-superblock {0}'

        with self._lock:
            check_output(stop_cmd.split())
            for _, member in md.members.iteritems():
                try:
                    check_output(zero_cmd.format(member['device']).split())
                except StorLeverError:
                    logger.log(logging.WARNING, logger.LOG_TYPE_ERROR,
                               "Failed zero superblock of device {0}".format(md_device),
                               exc_info=True)
            self._update_mdadm_conf()
            self.refresh()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "MD {0} removed successfully".format(md_device))

    def create(self,
               name,
               level,
               devices,
               **kwargs):
        '''
        Create a RAID device.

        .. versionchanged:: Helium

        .. warning::
        Use with CAUTION, as this function can be very destructive if not used
        properly!

        CLI Examples:

        .. code-block:: bash

        salt '*' raid.create /dev/md0 level=1 chunk=256 raid_devices=2 ['/dev/xvdd', '/dev/xvde'] test_mode=True

        .. note::

        Adding ``test_mode=True`` as an argument will print out the mdadm
        command that would have been run.

        name
        The name of the array to create.

        level
        The RAID level to use when creating the raid.

        devices
        A list of devices used to build the array.

        raid_devices
        The number of devices in the array. If not specified, the number of devices will be counted.

        kwargs
        Optional arguments to be passed to mdadm.

        returns
        test_mode=True:
        Prints out the full command.
        test_mode=False (Default):
        Executes command on remote the host(s) and
        Prints out the mdadm output.

        .. note::

        It takes time to create a RAID array. You can check the progress in
        "resync_status:" field of the results from the following command:

        .. code-block:: bash

        salt '*' raid.detail /dev/md0

        For more info, read the ``mdadm(8)`` manpage
        '''
        devices_string = ' '.join(devices)

        opts = ''
        for key in kwargs:
            if not key.startswith('__'):
                if kwargs[key] is True:
                    opts += '--{0} '.format(key)
                else:
                    opts += '--{0}={1} '.format(key, kwargs[key])

        with self._lock:
            cmd = "yes | /sbin/mdadm -C {0} --force {1} -l {2} -n {3} {4}".format(name,
                                                                     opts,
                                                                     level,
                                                                     len(devices),
                                                                     devices_string)

            check_output(cmd, shell=True)
            self._update_mdadm_conf()
            self.refresh()
            self._detail[name] = MD(name, self._lock)
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "MD {0} created successfully".format(name))
        return self._detail[name]


class MD(object):
    def __init__(self, device, lock):
        self.name = os.path.basename(device)
        self.dev_file = device
        self.refresh()
        self._lock = lock

    def refresh(self):
        '''
        Show detail for a specified RAID device

        CLI Example:

        .. code-block:: bash

        salt '*' raid.detail '/dev/md0'
        '''
        self.raid_level = ''
        self.state = ''
        self.array_size = 0
        self.used_dev_size = 0
        self.raid_devices = 0
        self.total_devices = 0
        self.active_device = 0
        self.working_device = 0
        self.failed_devices = 0
        self.spare_devices = 0
        self.resync_status = 100
        self.uuid = ''
        self.creation_time = ''
        self.update_time = ''
        self.persistence = ''
        self.members = {}

        # Lets make sure the device exists before running mdadm
        if not os.path.exists(self.dev_file):
            raise StorLeverError('Device {0} does not exist'.format(self.dev_file))

        cmd = '/sbin/mdadm --detail {0}'.format(self.dev_file)
        for line in check_output(cmd.split()).splitlines():
            if line.startswith(self.dev_file):
                continue
            if ' ' not in line:
                continue
            if not ':' in line:
                if '/dev/' in line:
                    comps = line.split()
                    state = comps[4:-1]
                    self.members[comps[0]] = {
                        'device': comps[-1],
                        'major': comps[1],
                        'minor': comps[2],
                        'number': comps[0],
                        'raiddevice': comps[3],
                        'state': ' '.join(state),
                        }
                continue
            else:
                comps = line.split(' : ')
                comps[0] = comps[0].lower()
                comps[0] = comps[0].strip()
                comps[0] = comps[0].replace(' ', '_')
                if comps[0] in ('array_size', 'used_dev_size'):
                    try:
                        comps[1] = int(comps[1].split()[0])
                    except Exception:
                        logger.log(logging.WARNING, logger.LOG_TYPE_ERROR,
                                   "Failed to parse MD detail [{0}] [{1}]".format(comps[0], comps[1]))
                        continue
                elif comps[0] in ('raid_devices', 'total_devices', 'active_devices',
                                  'working_devices', 'failed_devices', 'spare_devices'):
                    try:
                        comps[1] = int(comps[1])
                    except Exception:
                        logger.log(logging.WARNING, logger.LOG_TYPE_ERROR,
                                   "Failed to parse MD detail [{0}] [{1}]".format(comps[0], comps[1]))
                        continue
                elif comps[0] == 'resync_status':
                    try:
                        comps[1] = int(comps[1].split()[0][0:-1])
                    except Exception:
                        logger.log(logging.WARNING, logger.LOG_TYPE_ERROR,
                                   "Failed to parse MD detail [{0}] [{1}]".format(comps[0], comps[1]))
                        continue

                if hasattr(self, comps[0]):
                    setattr(self, comps[0], comps[1])


    def remove_component(self, device):
        fail_cmd = '/sbin/mdadm {0} --fail {1}'.format(self.dev_file, device)
        remove_cmd = '/sbin/mdadm {0} --remove {1}'.format(self.dev_file, device)
        with self._lock:
            check_output(fail_cmd.split())
            check_output(remove_cmd.split())
        self.refresh()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Block device {0} detached from MD {1} created successfully".format(device, self.dev_file))

    def add_component(self, device):
        add_cmd = '/sbin/mdadm {0} --add {1}'.format(self.dev_file, device)
        with self._lock:
            check_output(add_cmd.split())
        self.refresh()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Block device {0} added to MD {1} successfully".format(device, self.dev_file))

    def grow_raid(self, device):
        grow_cmd = '/sbin/mdadm --grow {0} --raid-device={1}'.format(self.dev_file, device)
        with self._lock:
            check_output(grow_cmd.split())
        self.refresh()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "MD {0} grows successfully with block device {}".format(self.dev_file, device))


MDManager = MDManager()


def md_mgr():
    return MDManager
