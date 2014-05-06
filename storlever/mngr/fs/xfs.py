"""
storlever.mngr.fs.xfs
~~~~~~~~~~~~~~~~

xfs filesystem class..

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

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
    "module_name": "xfs",
    "rpms": [
        "xfsprogs"
    ],
    "comment": "Provides the xfs filesystem type support"
}

class Xfs(FileSystem):

    @classmethod
    def mkfs(cls, type, dev_file, fs_options=""):
        cmd = "/sbin/mkfs.xfs -f -q %s %s" % (fs_options, dev_file)
        check_output(cmd, shell=True, input_ret=[1])

    def mount(self):
        check_output(["/bin/mount", "-t", self.fs_conf["type"],
                      "-o", self.mount_options,
                      self.fs_conf["dev_file"], self.fs_conf["mount_point"]],
                     input_ret=[32])
        # xfs does not support and no needs quota_check and quota_on

    def fs_meta_dump(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 500)
        return check_output(["/usr/sbin/xfs_info", self.fs_conf["mount_point"]],
                            input_ret=[1])

    def grow_size(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 500)
        check_output(["/usr/sbin/xfs_growfs", self.fs_conf["mount_point"]],
                     input_ret=[1])

    def quota_check(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 500)
        # xfs no needs and has no quota check function
        pass

ModuleManager.register_module(**MODULE_INFO)
# register to fs manager
FileSystemManager.add_fs_type("xfs", Xfs)





