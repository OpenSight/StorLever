"""
storlever.mngr.block.md.md
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lvm manager of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError


class MD(object):

    def list_raid(self):
        ret = {}
        for line in check_output('mdadm --detail --scan', shell=True):
            if ' ' not in line:
                continue
            comps = line.split()
            device = comps[1]
            ret[device] = {"device": device}
            for comp in comps[2:]:
                key = comp.split('=')[0].lower()
                value = comp.split('=')[1]
                ret[device][key] = value
        return ret

    def detail(self, device='/dev/md0'):
        '''
        Show detail for a specified RAID device

        CLI Example:

        .. code-block:: bash

        salt '*' raid.detail '/dev/md0'
        '''
        ret = {}
        ret['members'] = {}

        # Lets make sure the device exists before running mdadm
        if not os.path.exists(device):
            raise StorLeverError('Device {0} does not exist'.format(device))

        cmd = 'mdadm --detail {0}'.format(device)
        for line in check_output(cmd, shell=True).splitlines():
            if line.startswith(device):
                continue
            if ' ' not in line:
                continue
            if not ':' in line:
                if '/dev/' in line:
                    comps = line.split()
                    state = comps[4:-1]
                    ret['members'][comps[0]] = {
                        'device': comps[-1],
                        'major': comps[1],
                        'minor': comps[2],
                        'number': comps[0],
                        'raiddevice': comps[3],
                        'state': ' '.join(state),
                        }
                continue
            comps = line.split(' : ')
            comps[0] = comps[0].lower()
            comps[0] = comps[0].strip()
            comps[0] = comps[0].replace(' ', '_')
            ret[comps[0]] = comps[1].strip()
        return ret

    def delete(self, device):
        '''
        Destroy a RAID device.

        WARNING This will zero the superblock of all members of the RAID array..

        CLI Example:

        .. code-block:: bash

        salt '*' raid.destroy /dev/md0
        '''
        try:
            details = self.detail(device)
        except StorLeverError:
            raise StorLeverError('No such raid {0} exits'.format(device))

        stop_cmd = 'mdadm --stop {0}'.format(device)
        zero_cmd = 'mdadm --zero-superblock {0}'

        try:
            check_output(stop_cmd, shell=True)
            for number in details['members']:
                try:
                    check_output(zero_cmd.format(number['device']))
                except StorLeverError:
                    pass
        except StorLeverError:
            pass


    def create(name,
               level,
               devices,
               raid_devices=None,
               test_mode=False,
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
        cmd_args = {}

        cmd_args['name'] = name
        cmd_args['level'] = level
        cmd_args['devices'] = ' '.join(devices)

        if raid_devices is None:
            cmd_args['raid-devices'] = len(devices)

        opts = ''
        for key in kwargs:
            if not key.startswith('__'):
                if kwargs[key] is True:
                    opts += '--{0} '.format(key)
                else:
                    opts += '--{0}={1} '.format(key, kwargs[key])

        cmd_args['raw_args'] = opts

        cmd = "mdadm -C {0} -v {1}-l {2} -n {3} {4}".format(cmd_args['name'],
                                                            cmd_args['raw_args'],
                                                            cmd_args['level'],
                                                            cmd_args['raid-devices'],
                                                            cmd_args['devices'])

        check_output(cmd)



