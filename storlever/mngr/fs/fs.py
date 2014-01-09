"""
storlever.mngr.fs.fs
~~~~~~~~~~~~~~~~

filesystem base class. All filesystem type must inherit this class.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""
import os
import math
from storlever.lib.command import check_output


PROC_MOUNT_FILE = "/proc/mounts"


class FileSystem(object):
    def __init__(self, name, fs_conf):
        self.name = name
        self.fs_conf = fs_conf

    @classmethod
    def mkfs(cls, type, dev_file, fs_options=""):
        cmd = "/sbin/mkfs -t %s %s %s" % (type, fs_options, dev_file)
        check_output(cmd, shell=True, input_ret=[1])

    @property
    def mount_options(self):
        return self.fs_conf["mount_option"]

    def mount(self):
        check_output(["/bin/mount", "-t", self.fs_conf["type"],
                      "-o", self.mount_options,
                      self.fs_conf["dev_file"], self.fs_conf["mount_point"]],
                     input_ret=[32])

    def umount(self):
        check_output(["/bin/umount", "-f",
                      self.fs_conf["mount_point"]],
                     input_ret=[1])

    def is_available(self):
        with open(PROC_MOUNT_FILE, "r") as f:
            for line in f:
                mount_entry = line.split()
                if mount_entry[0] == self.fs_conf["dev_file"] and \
                   mount_entry[1] == self.fs_conf["mount_point"]:
                    return True
        return False

    def usage_info(self):
        if self.is_available():
            st = os.statvfs(self.fs_conf["mount_point"])
            available = (st.f_bavail * st.f_frsize)
            total = (st.f_blocks * st.f_frsize)
            used = (st.f_blocks - st.f_bfree) * st.f_frsize
            try:
                percent = (used * 100 + (total - 1)) / total
            except ZeroDivisionError:
                percent = 0
        else:
            total = 0
            available = 0
            used = 0
            percent = 0

        return {"total": total, "available": available,
                "used": used, "percent":  percent}

    def fs_meta_dump(self):
        return ""

    def grow_size(self):
        pass

    def create_share(self):
        pass

    def delete_share(self):
        pass

    def list_share(self):
        pass

    def mod_share_owner(self):
        pass

    def mod_share_mode(self):
        pass





