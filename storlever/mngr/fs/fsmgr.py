"""
storlever.mngr.fs.fsmgr
~~~~~~~~~~~~~~~~

This module implements fs management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

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
    Default, DoNotCare, BoolVal

from storlever.mngr.fs import fs

from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "filesystem",
    "rpms": [
        "util-linux-ng",
        "setup",
        "quota",
        "coreutils"
    ],
    "comment": "Provides the management functions of the file system in OS"
}




FS_CONF_FILE_NAME = "fs_conf.yaml"
FSTAB_FILE_PATH = "/etc/fstab"
MOUNT_DIR = "/mnt/"


class FileSystemManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.support_fs_type = {}
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, FS_CONF_FILE_NAME)
        self.fs_conf_schema = Schema({
            "type": Use(str),     # filesystem type
            "dev_file":  Use(str),     # dev file
            "dev_uuid": Use(str),      # dev uuid
            "mount_point": Use(str),  # mount point of this fs,
            "mount_option": Use(str),  # mount option of this fs
            "check_onboot": BoolVal(),  # fsck fs on boot
            Optional("comment"): Default(Use(str), default=""),  # comment,
            DoNotCare(str): object  # for all those key we don't care
        })
        self.fs_dict_schema = Schema({
            DoNotCare(str): self.fs_conf_schema
        })

        # sync fs conf to fstab on boot
        self.sync_to_fstab()

    def _uuid_to_dev_file(self, uuid):
        try:
            return check_output(["/sbin/blkid", "-U", uuid]).strip()
        except Exception:
            return ""

    def _dev_file_to_uuid(self, dev_file):

        try:
            return subprocess.check_output(
                ["/sbin/blkid", "-s", "UUID", "-o", "value", dev_file],
                stderr=subprocess.STDOUT,
                shell=False).strip()
        except subprocess.CalledProcessError as e:
            if e.returncode == 2:
                http_status = 400
                info = "The dev file (%s) has no UUID tag. " \
                       "Make sure it exists and contains a filesystem" % dev_file
            else:
                http_status = 500
                info = e.output

            # re-raise the storlever's error
            raise StorLeverError(info, http_status)

    def _load_conf(self):
        fs_dict = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            fs_dict = \
                Config.from_file(self.conf_file, self.fs_dict_schema).conf
            # check dev_file by uuid
            for fs_name, fs_conf in fs_dict.items():
                if fs_conf["dev_uuid"] != "":
                    fs_conf["dev_file"] = self._uuid_to_dev_file(fs_conf["dev_uuid"])
        return fs_dict

    def _save_conf(self, fs_dict):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, fs_dict)

    def _fs_conf_to_fstab_line(self, fs_name, fs_conf):
        if fs_conf["dev_uuid"] == "":
            dev_file_name = fs_conf["dev_file"]
        else:
            dev_file_name = "UUID=%s" % fs_conf["dev_uuid"]

        if fs_conf["check_onboot"]:
            boot_flag = 2
        else:
            boot_flag = 0

        # get a fs object
        fs_object = self._get_fs_type_cls(fs_conf["type"])(fs_name, fs_conf)
        if fs_object.mount_options == "":
            option_flag = "defaults"
        else:
            option_flag = fs_object.mount_options

        return "%s\t%s\t%s\t%s\t0\t%d\n" % \
               (dev_file_name, fs_conf["mount_point"], fs_conf["type"],
                option_flag, boot_flag)

    def _sync_to_fstab(self, fs_dict):
        with open(FSTAB_FILE_PATH, "r") as f:
            lines = f.readlines()

        if "# begin storlever\n" in lines:
            before_storlever = lines[0:lines.index("# begin storlever\n")]
        else:
            before_storlever = lines[0:]
            if before_storlever and (not before_storlever[-1].endswith("\n")):
                before_storlever[-1] += "\n"

        if "# end storlever\n" in lines:
            after_storlever = lines[lines.index("# end storlever\n") + 1:]
        else:
            after_storlever = []

        with open(FSTAB_FILE_PATH, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            for fs_name, fs_conf in fs_dict.items():
                f.write(self._fs_conf_to_fstab_line(fs_name, fs_conf))
            f.write("# end storlever\n")
            f.writelines(after_storlever)

    def sync_to_fstab(self):
        """sync the fs conf list in storlever to /etc/fstab"""

        with self.lock:
            fs_dict = self._load_conf()
            self._sync_to_fstab(fs_dict)


    def system_restore_cb(self):
        """sync the fs conf list in storlever to /etc/fstab"""

        with self.lock:
            fs_dict = {}
            self._sync_to_fstab(fs_dict)

    def _mount_fs(self, name, fs_conf):

        # get a fs object
        fs_object = self._get_fs_type_cls(fs_conf["type"])(name, fs_conf)

        # call this object's mount method
        fs_object.mount()

    def _umount_fs(self, name, fs_conf):
        # get a fs object
        fs_object = self._get_fs_type_cls(fs_conf["type"])(name, fs_conf)

        # call this object's mount method
        fs_object.umount()

    def _get_fs_type_cls(self, type):
        cls = self.support_fs_type.get(type, fs.FileSystem)

        return cls

    def add_fs_type(self, type, cls, *args, **kwargs):
        """add the fs class with specific type name"""
        with self.lock:
            self.support_fs_type[type] = cls

    def get_fs_by_name(self, fs_name):
        """return a fs object according to the given fs name"""
        with self.lock:
            fs_dict = self._load_conf()
            if fs_name not in fs_dict:
                raise StorLeverError("Filesystem(%s) does not exist" % fs_name, 404)
            fs_conf = fs_dict[fs_name]
            cls = self._get_fs_type_cls(fs_conf["type"])

        return cls(fs_name, fs_conf)

    def get_fs_list(self):
        """get the fs object list in the storlever
        """
        with self.lock:
            fs_dict = self._load_conf()
        fs_list = []
        for fs_name, fs_conf in fs_dict.items():
            cls = self._get_fs_type_cls(fs_conf["type"])
            fs_list.append(cls(fs_name, fs_conf))

        return fs_list

    def fs_type_list(self):
        """list all fs type supported in the storlever"""
        with self.lock:
            type_list = self.support_fs_type.keys()
        return type_list

    def add_fs(self, fs_name, type, dev_file,
               mount_option="", check_onboot=False,
               comment="", user="unknown"):

        """add a filesystem with the given properties to storlever

           The new filesystem would be mount on the specific directory(/mnt/FS_NAME)
           and would be added to the storlever's fs config
        """

        # check type
        if type not in self.support_fs_type:
            raise StorLeverError("type(%s) does not support" % type, 400)

        # check mount point
        mount_point = os.path.join(MOUNT_DIR, fs_name)
        if os.path.exists(mount_point):
            if not os.path.isdir(mount_point):
                raise StorLeverError("mount point(%s) already exists and is not directory" % mount_point)
        else:
            # create mount point
            os.makedirs(mount_point)

        # don't check dev file exist, because for the network fs, the dev file is a network id
        # if not os.path.exists(dev_file):
        #     raise StorLeverError("dev file(%s) does not exist" % dev_file, 400)

        dev_uuid = ""

        if (not dev_file.startswith("/dev/mapper")) and os.path.exists(dev_file):
            dev_uuid = self._dev_file_to_uuid(dev_file)

        fs_conf = {
            "type": type,
            "dev_file": dev_file,
            "dev_uuid": dev_uuid,
            "mount_point": mount_point,
            "mount_option": mount_option,
            "check_onboot": check_onboot,
            "comment": comment
        }
        fs_conf = self.fs_conf_schema.validate(fs_conf)

        with self.lock:
            fs_dict = self._load_conf()
            if fs_name in fs_dict:
                raise StorLeverError("filesystem(%s) already exist" % fs_name, 400)

            # mount fs first
            self._mount_fs(fs_name, fs_conf)

            fs_dict[fs_name] = fs_conf
            self._save_conf(fs_dict)
            self._sync_to_fstab(fs_dict)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "New filesystem %s (dev:%s, mount_point:%s, option:%s) "
                   "is added by user(%s)" %
                   (fs_name, dev_file, mount_point, mount_option,  user))

    def del_fs(self, fs_name, user="unknown"):
        """delete a filesystem from storlever

        the file would be deleted from the storlever's config file and
        would be unmount from linux system

        """
        with self.lock:
            fs_dict = self._load_conf()
            if fs_name not in fs_dict:
                raise StorLeverError("filesystem(%s) does not exist" % fs_name, 400)
            fs_conf = fs_dict[fs_name]
            del fs_dict[fs_name]

             #umount fs first. if it failed, don't delete it in the config
            self._umount_fs(fs_name, fs_conf)

            self._save_conf(fs_dict)
            self._sync_to_fstab(fs_dict)

        try:
            os.rmdir(fs_conf["mount_point"])
        except OSError as e:
            pass


        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "filesystem %s (dev:%s, mount_point:%s, option:%s) "
                   "is deleted by user(%s)" %
                   (fs_name, fs_conf['dev_file'],
                    fs_conf['mount_point'], fs_conf['mount_option'],
                    user))

    def mkfs_on_dev(self, type, dev_file, fs_options=""):
        with self.lock:
            cls = self._get_fs_type_cls(type)
        cls.mkfs(type, dev_file, fs_options)


FileSystemManager = FileSystemManager()

cfg_mgr().register_restore_from_file_cb(FileSystemManager.sync_to_fstab)
cfg_mgr().register_system_restore_cb(FileSystemManager.system_restore_cb)
ModuleManager.register_module(**MODULE_INFO)


# disable selinux impact
set_selinux_permissive()

def fs_mgr():
    """return the global user manager instance"""
    return FileSystemManager








