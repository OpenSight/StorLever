"""
storlever.mngr.fs.fs
~~~~~~~~~~~~~~~~

filesystem base class. All filesystem type must inherit this class.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""
import os
import stat
from storlever.lib.command import check_output
from storlever.mngr.system.usermgr import user_mgr
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging

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

    def create_share(self, name, user=None, group=None, mode=0777, operator="unknown"):
        # make sure fs is available
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        umgr = user_mgr()
        if user is None:
            uid = -1
        else:
            uid = umgr.get_user_info_by_name(user)["uid"]
        if group is None:
            gid = -1
        else:
            gid = umgr.get_group_info_by_name(group)["gid"]
        uid = umgr.get_user_info_by_name()
        mount_point = self.fs_conf["mount_point"]
        path = os.path.join(mount_point, name)
        os.mkdir(path, mode)
        os.chown(path, uid, gid)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Share directory (%s) is created"
                   " by user(%s)" %
                   (path, operator))

    def delete_share(self, name, user="unknown"):
        # make sure fs is available
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        path = os.path.join(self.fs_conf["mount_point"], name)
        if not os.path.exists(path):
            raise StorLeverError("Share directory not found", 404)
        check_output(["/bin/rm", "-rf", path],
                     input_ret=[1])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Share directory (%s) is deleted"
                   " by user(%s)" %
                   (path, user))

    def _get_uid_map(self):
        umgr = user_mgr();
        ulist = umgr.user_list()
        uid_map = {}
        for user in ulist:
            uid_map[user["uid"]] = user

        return uid_map

    def _get_gid_map(self):
        umgr = user_mgr();
        glist = umgr.groupr_list()
        gid_map = {}
        for group in glist:
            gid_map[group["gid"]] = group

        return gid_map


    def share_list(self):
        mount_point = self.fs_conf["mount_point"]
        share_list = os.listdir(mount_point)
        uid_map = self._get_uid_map()
        gid_map = self._get_gid_map()
        output_list = []
        for entry in share_list:
            path = os.path.join(mount_point, entry)
            entry_stat = os.stat(path)
            if not stat.S_ISDIR(entry_stat.st_mode):
                continue    # filter out all file
            name = entry
            mode = stat.S_IMODE(entry_stat.st_mode)
            if entry_stat.st_uid in uid_map:
                user = uid_map[entry_stat.st_uid]["name"]
            else:
                user = str(entry_stat.st_uid)
            if entry_stat.st_gid in gid_map:
                group = gid_map[entry_stat.st_gid]["name"]
            else:
                group = str(entry_stat.st_gid)

            output_list.append({
                "name": name,
                "path": path,
                "mode": mode,
                "user": user,
                "group": group
            })

        return output_list

    def mod_share_owner(self, name, user = None, group = None, operator="unknown"):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        path = os.path.join(self.fs_conf["mount_point"], name)
        if not os.path.exists(path):
            raise StorLeverError("Share directory not found", 404)
        umgr = user_mgr()
        if user is None:
            uid = -1
        else:
            uid = umgr.get_user_info_by_name(user)["uid"]
        if group is None:
            gid = -1
        else:
            gid = umgr.get_group_info_by_name(group)["gid"]
        os.chown(path, uid, gid)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Share directory (%s) owner is changed to (%s:%s)"
                   " by user(%s)" %
                   (path, user, group, operator))

    def mod_share_mode(self, name, mode, operator="unknown"):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        path = os.path.join(self.fs_conf["mount_point"], name)
        if not os.path.exists(path):
            raise StorLeverError("Share directory not found", 404)
        os.chmode(path, mode)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Share directory (%s) mode is changed to 0%o"
                   " by user(%s)" %
                   (path, mode, operator))




