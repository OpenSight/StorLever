"""
storlever.mngr.block.blockmgr
~~~~~~~~~~~~~~~~

This module implements block device manager

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import os
import os.path
import subprocess

from storlever.lib.config import Config
from storlever.lib.command import check_output, set_selinux_permissive
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal
from storlever.mngr.system.usermgr import user_mgr
from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from storlever.lib.confparse import properties, ini



BLOCKDEV_CMD = "/sbin/blockdev"
LSBLK_CMD = "/bin/lsblk"

class BlockManager(object):
    """contains all methods to manage block device in linux system"""

    def get_block_dev_list(self):
        pass

    def flush_buf(self, block_name):
        if os.path.exists(block_name):
            dev_file = block_name
        elif os.path.exists(os.path.join("/dev/mapper/", block_name)):
            dev_file = os.path.join("/dev/mapper/", block_name)
        elif os.path.exists(os.path.join("/dev/", block_name)):
            dev_file = os.path.join("/dev/", block_name)
        else:
            raise StorLeverError("Device (%s) Not Found" % block_name, 404)

        check_output([BLOCKDEV_CMD, "--flushbufs", dev_file])


BlockManager = BlockManager()

def block_mgr():
    """return the global block manager instance"""
    return BlockManager








