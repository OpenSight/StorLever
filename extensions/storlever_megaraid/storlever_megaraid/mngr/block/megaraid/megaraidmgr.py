"""
storlever_megaraid.mngr.block.megaraid.megaraidmgr
~~~~~~~~~~~~~~~~

This module provide the support for megaraid to storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "megaraid",
    "comment": "Provides the support for Megaraid controller, which can manage "
               "the the logical disk output by megaraid driver"
}

BLOCKDEV_CMD = "/sbin/blockdev"
LSBLK_CMD = "/bin/lsblk"

class MegaraidManager(object):
    """contains all methods to manage block device in linux system"""

    def get_block_dev_list(self):
        block_list = []
        lines = check_output([LSBLK_CMD, "-ribn", "-o",
                              "NAME,MAJ:MIN,TYPE,SIZE,RO,FSTYPE,MOUNTPOINT"]).splitlines()
        for line in lines:
            line_list = line.split(" ")
            maj, sep, min = line_list[1].partition(":")
            if int(line_list[4]) == 0:
                ro = False
            else:
                ro = True
            if os.path.exists(os.path.join("/dev/", line_list[0])):
                dev_file = os.path.join("/dev/", line_list[0])
            elif os.path.exists(os.path.join("/dev/mapper/", line_list[0])):
                dev_file = os.path.join("/dev/mapper/", line_list[0])
            else:
                dev_file = os.path.join("/dev/block/", line_list[1])

            block_list.append({
                "name": line_list[0],
                "major": int(maj),
                "minor": int(min),
                "size": int(line_list[3]),
                "type": line_list[2],
                "readonly": ro,
                "dev_file": dev_file,
                "fs_type": line_list[5],
                "mount_point": line_list[6]
            })

        return block_list

    def flush_block_buf(self, block_name):
        if os.path.exists(block_name):
            dev_file = block_name
        elif os.path.exists(os.path.join("/dev/mapper/", block_name)):
            dev_file = os.path.join("/dev/mapper/", block_name)
        elif os.path.exists(os.path.join("/dev/", block_name)):
            dev_file = os.path.join("/dev/", block_name)
        else:
            raise StorLeverError("Device (%s) Not Found" % block_name, 404)

        check_output([BLOCKDEV_CMD, "--flushbufs", dev_file])


MegaraidManager = MegaraidManager()
ModuleManager.register_module(**MODULE_INFO)

def megaraid_mgr():
    """return the global block manager instance"""
    return MegaraidManager








