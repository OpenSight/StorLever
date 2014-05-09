"""
storlever.mngr.fs.ext4
~~~~~~~~~~~~~~~~

ext4 filesystem class..

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""
import os
import stat
from storlever.lib.command import check_output
from storlever.mngr.fs.fs import FileSystem
from storlever.mngr.fs.fsmgr import FileSystemManager
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "ext4",
    "rpms": [
        "e2fsprogs"
    ],
    "comment": "Provides the ext4 filesystem type support"
}

class Ext4(FileSystem):

    @classmethod
    def mkfs(cls, type, dev_file, fs_options=""):
        cmd = "/sbin/mkfs.ext4 -F -q %s %s" % (fs_options, dev_file)
        check_output(cmd, shell=True, input_ret=[1])

    def fs_meta_dump(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        return check_output(["/sbin/dumpe2fs", "-h", self.fs_conf["dev_file"]],
                            input_ret=[1])

    def grow_size(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        check_output(["/sbin/resize2fs", self.fs_conf["dev_file"]],
                     input_ret=[1])

ModuleManager.register_module(**MODULE_INFO)

# register to fs manager
FileSystemManager.add_fs_type("ext4", Ext4)





