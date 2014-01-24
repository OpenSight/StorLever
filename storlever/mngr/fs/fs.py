"""
storlever.mngr.fs.fs
~~~~~~~~~~~~~~~~

filesystem base class. All filesystem type must inherit this class.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""
import os
import stat
import re
from storlever.lib.command import check_output
from storlever.mngr.system.usermgr import user_mgr
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging


PROC_MOUNT_FILE = "/proc/mounts"
QUOTACHECK_BIN = "/sbin/quotacheck"
QUOTAON_BIN = "/sbin/quotaon"
REPQUOTA_BIN = "/usr/sbin/repquota"
SETQUOTA_BIN = "/usr/sbin/setquota"

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
        quota_enabled = False
        quotaon_args = [QUOTAON_BIN]
        quotacheck_args = [QUOTACHECK_BIN, "-c", "-f"]
        if "usrquota" in self.mount_options:
            quota_enabled = True
            quotaon_args.append("-u")
            quotacheck_args.append("-u")
        if "grpquota" in self.mount_options:
            quota_enabled = True
            quotaon_args.append("-g")
            quotacheck_args.append("-g")

        if quota_enabled:
            try:
                check_output(quotacheck_args)
                check_output(quotaon_args)
            except Exception as e:
                pass # omit the exception


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

    #
    # share related
    #

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
            gid = umgr.get_group_by_name(group)["gid"]

        mount_point = self.fs_conf["mount_point"]
        path = os.path.join(mount_point, name)
        os.umask(0)
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
        umgr = user_mgr()
        glist = umgr.group_list()
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
            gid = umgr.get_group_by_name(group)["gid"]
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
        os.umask(0)
        os.chmod(path, mode)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Share directory (%s) mode is changed to 0%o"
                   " by user(%s)" %
                   (path, mode, operator))



    #
    # quota related
    #

    def quota_check(self):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)

        check_output([QUOTACHECK_BIN, "-ugf",
                      self.fs_conf["mount_point"]])

    def quota_user_report(self):
        uq_list = []
        uq_lines = check_output([REPQUOTA_BIN, "-up", self.fs_conf["mount_point"]]).splitlines()
        table_start = False
        start_pattern = re.compile(r"^(-)+$")
        entry_pattern = re.compile(r"^[-\+][-\+]$")
        for line in uq_lines:
            if table_start:
                if len(line) == 0:
                    break
                elements = line.split()
                if len(elements) < 10:
                    break
                if entry_pattern.match(elements[1]) is None:
                    break

                uq_list.append({
                    "name": elements[0],
                    "block_used": int(elements[2]),
                    "block_softlimit": int(elements[3]),
                    "block_hardlimit": int(elements[4]),
                    "inode_used": int(elements[6]),
                    "inode_softlimit":int(elements[7]),
                    "inode_softlimit":int(elements[8])
                })

            elif start_pattern.match(line) is not None:
                table_start = True

        return uq_list


    def quota_group_report(self):
        gq_list = []
        gq_lines = check_output([REPQUOTA_BIN, "-gp", self.fs_conf["mount_point"]]).splitlines()
        table_start = False
        start_pattern = re.compile(r"^(-)+$")
        entry_pattern = re.compile(r"^[-\+][-\+]$")
        for line in gq_lines:
            if table_start:
                if len(line) == 0:
                    break
                elements = line.split()
                if len(elements) < 10:
                    break
                if entry_pattern.match(elements[1]) is None:
                    break

                gq_list.append({
                    "name": elements[0],
                    "block_used": int(elements[2]),
                    "block_softlimit": int(elements[3]),
                    "block_hardlimit": int(elements[4]),
                    "inode_used": int(elements[6]),
                    "inode_softlimit":int(elements[7]),
                    "inode_softlimit":int(elements[8])
                })

            elif start_pattern.match(line) is not None:
                table_start = True

        return gq_list

    def quota_user_set(self, user,
                       block_softlimit=0,
                       block_hardlimit=0,
                       inode_softlimit=0,
                       inode_hardlimit=0,
                       operator="unknown"):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        setquota_agrs = [
            SETQUOTA_BIN,
            "-u",
            user,
            str(block_softlimit),
            str(block_hardlimit),
            str(inode_softlimit),
            str(inode_hardlimit),
            self.fs_conf["mount_point"]
        ]
        check_output(setquota_agrs)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "File System(%s) quota for user(%s) is changed to "
                   "(%d,%d,%d,%d)"
                   " by user(%s)" %
                   (self.name, user,
                    block_softlimit, block_hardlimit,
                    inode_softlimit, inode_hardlimit,
                    operator))


    def quota_group_set(self, group,
                        block_softlimit=0,
                        block_hardlimit=0,
                        inode_softlimit=0,
                        inode_hardlimit=0,
                        operator="unknown"):
        if not self.is_available():
            raise StorLeverError("File system is unavailable", 400)
        setquota_agrs = [
            SETQUOTA_BIN,
            "-g",
            group,
            str(block_softlimit),
            str(block_hardlimit),
            str(inode_softlimit),
            str(inode_hardlimit),
            self.fs_conf["mount_point"]
        ]
        check_output(setquota_agrs)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "File System(%s) quota for group(%s) is changed to "
                   "(%d,%d,%d,%d)"
                   " by user(%s)" %
                   (self.name, group,
                    block_softlimit, block_hardlimit,
                    inode_softlimit, inode_hardlimit,
                    operator))




