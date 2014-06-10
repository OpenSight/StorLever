"""
storlever.mngr.block.blockmgr
~~~~~~~~~~~~~~~~

This module implements block device manager

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "block",
    "rpms": [
        "util-linux-ng",
    ],
    "comment": "Provides the management functions for block device"
}

BLOCKDEV_CMD = "/sbin/blockdev"
LSBLK_CMD = "/bin/lsblk"
DD_CMD = "/bin/dd"

def _block_name_to_dev_file(name):

    if os.path.exists(os.path.join("/dev/", name)):
        dev_file = os.path.join("/dev/", name)
    elif os.path.exists(os.path.join("/dev/mapper/", name)):
        dev_file = os.path.join("/dev/mapper/", name)
    else:
        raise StorLeverError("Device File (%s) Not Found" % name, 404)

    return dev_file


class BlockDev(object):
    def __init__(self, name, major, minor, size, type, readonly,
                 fs_type, mount_point):
        self.name = name
        self.major = int(major)
        self.minor = int(minor)
        self.size = size
        self.type = type
        self.readonly = readonly
        self.fs_type = fs_type
        self.mount_point = mount_point
        try:
            self.dev_file = _block_name_to_dev_file(self.name)
        except StorLeverError as e:
            self.dev_file = \
                os.path.join("/dev/block/", "%d:%d" % (self.major, self.minor))


    def refresh_property(self):
        lines = check_output([LSBLK_CMD, "-ribn", "-o",
                              "NAME,MAJ:MIN,TYPE,SIZE,RO,FSTYPE,MOUNTPOINT",
                              self.dev_file]).splitlines()
        if not lines:
            raise StorLeverError("Device (%s) has been removed from system" % self.dev_file, 404)

        line = lines[0]
        line_list = line.split(" ")
        maj_num, sep, min_num = line_list[1].partition(":")
        if int(line_list[4]) == 0:
            ro = False
        else:
            ro = True
        self.name = line_list[0]
        self.major = int(maj_num)
        self.minor = int(min_num)
        self.size = int(line_list[3])
        self.type = line_list[2]
        self.readonly = ro
        self.fs_type = line_list[5]
        self.mount_point = line_list[6]

    def flush_block_buf(self):
        check_output([BLOCKDEV_CMD, "--flushbufs", self.dev_file])

    def clean_meta(self):
        '''clean the meta data(lvm, md, fs, etc) on this block dev

        In detail, this method would clean the start 4M and end 4M space of the dev
        '''
        bs = 4096
        count = 1024 # 4M / 4K
        seek = int((self.size + 4095) / 4096) - count
        check_output([DD_CMD, "if=/dev/zero",
                      "of=%s" % self.dev_file,
                      "oflag=direct",
                      "seek=0",
                      "bs=%d" % bs,
                      "count=%d" % count])

        check_output([DD_CMD, "if=/dev/zero",
                      "of=%s" % self.dev_file,
                      "oflag=direct",
                      "seek=%d" % seek,
                      "bs=%d" % bs,
                      "count=%d" % count])


class BlockManager(object):
    """contains all methods to manage block device in linux system"""

    def get_block_dev_list(self):
        block_list = []
        lines = check_output([LSBLK_CMD, "-ribn", "-o",
                              "NAME,MAJ:MIN,TYPE,SIZE,RO,FSTYPE,MOUNTPOINT"]).splitlines()
        for line in lines:
            line_list = line.split(" ")
            maj_num, sep, min_num = line_list[1].partition(":")
            if int(line_list[4]) == 0:
                ro = False
            else:
                ro = True
            block_list.append(BlockDev(line_list[0],int(maj_num), int(min_num),
                                       int(line_list[3]), line_list[2], ro,
                                       line_list[5], line_list[6]))

        return block_list

    def get_block_dev_by_name(self, name):
        dev_file = _block_name_to_dev_file(name)

        lines = check_output([LSBLK_CMD, "-ribn", "-o",
                              "NAME,MAJ:MIN,TYPE,SIZE,RO,FSTYPE,MOUNTPOINT",
                              dev_file]).splitlines()
        if not lines:
            raise StorLeverError("Device (%s) Not Block Device" % name, 404)

        line = lines[0]

        line_list = line.split(" ")
        maj_num, sep, min_num = line_list[1].partition(":")
        if int(line_list[4]) == 0:
            ro = False
        else:
            ro = True

        return BlockDev(line_list[0],int(maj_num), int(min_num),
                        int(line_list[3]), line_list[2], ro,
                        line_list[5], line_list[6])




BlockManager = BlockManager()
ModuleManager.register_module(**MODULE_INFO)

def block_mgr():
    """return the global block manager instance"""
    return BlockManager








