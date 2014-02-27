"""
storlever.mngr.nas.ftpmgr
~~~~~~~~~~~~~~~~

This module implements ftp server management.

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
from storlever.lib.confparse import properties

FTP_CONF_FILE_NAME = "ftp_conf.yaml"
VSFTPD_ETC_CONF_DIR = "/etc/vsftpd/"
VSFTPD_ETC_CONF_FILE = "vsftpd.conf"
VSFTPD_ETC_USER_LIST = "user_list"
VSFTPD_ETC_CHROOT_LIST = "chroot_list"

FTP_USER_CONF_SCHEMA = Schema({
    "user_name": Use(str),
    # When enabled, the user can log in ftp
    Optional("login_enable"): Default(BoolVal(), default=True),
    # When enabled, the user will be placed into the chroot jail
    Optional("chroot_enable"): Default(BoolVal(), default=False)
})

FTP_CONF_SCHEMA = Schema({
    Optional("listen"): Default(BoolVal(), default=False),    # ftp service listen on ipv4 port
    Optional("listen6"): Default(BoolVal(), default=False),   # ftp service listen on ipv6 port
    Optional("listen_port"): Default(IntVal(min=1, max=65535), default=21),  # ftp port number

    # The maximum amount of time between commands from a remote client.
    # Once triggered, the connection to the remote client is closed
    Optional("idle_session_timeout"): Default(Use(int), default=300),

    # the maximum data transfer rate for anonymous users in bytes per second.
    # The default value is 0, which does not limit the transfer rate.
    Optional("anon_max_rate"): Default(Use(int), default=0),
    # the maximum rate data is transferred for local users in bytes per second.
    # The default value is 0, which does not limit the transfer rate.
    Optional("local_max_rate"): Default(Use(int), default=0),

    # the maximum number of simultaneous clients allowed to connect to
    # the server when it is running in standalone mode. Any additional client
    # connections would result in an error message.
    # The default value is 0, which does not limit connections.
    Optional("max_clients"): Default(Use(int), default=0),

    # the maximum of clients allowed to connected from the same source IP address.
    # The default value is 0, which does not limit connections.
    Optional("max_per_ip"): Default(Use(int), default=0),

    # When enabled, file downloads are permitted
    Optional("download_enable"): Default(BoolVal(), default=True),
    # When enabled, FTP commands which can change the file system are allowed
    Optional("write_enable"): Default(BoolVal(), default=False),

    # When enabled, local users are allowed to log into the system
    Optional("local_enable"): Default(BoolVal(), default=False),
    # Only valid when local_enable is true. If userlist_enable == False,
    # all local user (except for some reserved user, like root, bin) can login ftp.
    # Otherwise, only the users, who is in the user list and is login enabled, can
    # login ftp
    Optional("userlist_enable"): Default(BoolVal(), default=False),
    # Specifies the directory ftpd changes to after a local user logs in. default is
    # empty, which means the user's home directory
    Optional("local_root"): Default(Use(str), default=""),

    # When enabled, local users are change-rooted to their home directories after logging in.
    Optional("chroot_enable"): Default(BoolVal(), default=False),
    # Only valid when chroot_enable is true. If chroot_list == False,
    # all local user are placed in a chroot jail upon log in.
    # Otherwise, only the users, who is in the user list and is chroot enabled, would be
    # placed in a chroot jail upon log in.
    Optional("chroot_list"): Default(BoolVal(), default=False),

    # the umask value for file creation. default is 022(18 in 10-based)
    Optional("local_umask"): Default(IntVal(min=0, max=0777), default=18),

    Optional("user_list"):  Default(Schema({DoNotCare(str): FTP_USER_CONF_SCHEMA}),
                                      default={}),

    # When enabled, anonymous users are allowed to log in.
    # The usernames anonymous and ftp are accepted.
    Optional("anonymous_enable"): Default(BoolVal(), default=False),

    # When enabled in conjunction with the write_enable directive,
    # anonymous users are allowed to create new directories within
    # a parent directory which has write permissions
    Optional("anon_mkdir_write_enable"): Default(BoolVal(), default=False),
    # When enabled in conjunction with the write_enable directive,
    # anonymous users are allowed to upload files within
    # a parent directory which has write permissions.
    Optional("anon_upload_enable"): Default(BoolVal(), default=False),

    # Specifies the local user account (listed in /etc/passwd) used for the anonymous user.
    # The home directory specified in /etc/passwd for the user is the root directory of the anonymous user.
    Optional("anon_username"): Default(Use(str), default="ftp"),

    # Specifies the directory vsftpd changes to after an anonymous user logs in. default is
    # empty, which means the anon_username user's home directory
    Optional("anon_root"): Default(Use(str), default=""),

    DoNotCare(str): Use(str)  # for all those key we don't care
})

class FtpManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, FTP_CONF_FILE_NAME)
        self.ftp_user_conf_schema = FTP_USER_CONF_SCHEMA
        self.ftp_conf_schema = FTP_CONF_SCHEMA

    def _load_conf(self):
        ftp_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            ftp_conf = \
                Config.from_file(self.conf_file, self.ftp_conf_schema).conf
        else:
            ftp_conf = self.ftp_conf_schema.validate(ftp_conf)
        return ftp_conf

    def _save_conf(self, ftp_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, ftp_conf)

    def _bool_to_yn(self, value):
        if value:
            return "YES"
        else:
            return "NO"

    def _sync_to_system_conf(self, ftp_conf):

        if not os.path.exists(VSFTPD_ETC_CONF_DIR):
            os.makedirs(VSFTPD_ETC_CONF_DIR)

        # conf file
        vsftpd_conf = properties()
        vsftpd_conf["listen"] = self._bool_to_yn(ftp_conf["listen"])
        vsftpd_conf["listen_ipv6"] = self._bool_to_yn(ftp_conf["listen6"])
        vsftpd_conf["listen_port"] = ftp_conf["listen_port"]
        vsftpd_conf["idle_session_timeout"] = ftp_conf["idle_session_timeout"]
        vsftpd_conf["anon_max_rate"] = ftp_conf["anon_max_rate"]
        vsftpd_conf["local_max_rate"] = ftp_conf["local_max_rate"]
        vsftpd_conf["max_clients"] = ftp_conf["max_clients"]
        vsftpd_conf["max_per_ip"] = ftp_conf["max_per_ip"]
        vsftpd_conf["local_max_rate"] = ftp_conf["local_max_rate"]
        vsftpd_conf["max_clients"] = ftp_conf["max_clients"]

        vsftpd_conf["download_enable"] = self._bool_to_yn(ftp_conf["download_enable"])
        vsftpd_conf["write_enable"] = self._bool_to_yn(ftp_conf["write_enable"])

        vsftpd_conf["download_enable"] = self._bool_to_yn(ftp_conf["download_enable"])
        vsftpd_conf["write_enable"] = self._bool_to_yn(ftp_conf["write_enable"])

        vsftpd_conf["local_enable"] = self._bool_to_yn(ftp_conf["local_enable"])
        if ftp_conf["local_enable"]:
            vsftpd_conf["userlist_enable"] = self._bool_to_yn(ftp_conf["userlist_enable"])
        else:
            vsftpd_conf["userlist_enable"] = "NO"
        vsftpd_conf["userlist_deny"] = "NO"
        vsftpd_conf["local_umask"] = "0%o" % ftp_conf["local_umask"]
        if len(ftp_conf["local_root"]) == 0:
            vsftpd_conf.delete("local_root")
        else:
            vsftpd_conf["local_root"] = ftp_conf["local_root"]

        if ftp_conf["chroot_enable"]:
            if ftp_conf["chroot_list"]:
                vsftpd_conf["chroot_local_user"] = "NO"
                vsftpd_conf["chroot_list_enable"] = "YES"
            else:
                vsftpd_conf["chroot_local_user"] = "YES"
                vsftpd_conf["chroot_list_enable"] = "NO"
        else:
            vsftpd_conf["chroot_local_user"] = "NO"
            vsftpd_conf["chroot_list_enable"] = "NO"

        vsftpd_conf["anonymous_enable"] = self._bool_to_yn(ftp_conf["anonymous_enable"])
        vsftpd_conf["anon_mkdir_write_enable"] = self._bool_to_yn(ftp_conf["anon_mkdir_write_enable"])
        vsftpd_conf["anon_upload_enable"] = self._bool_to_yn(ftp_conf["anon_upload_enable"])
        vsftpd_conf["ftp_username"] = ftp_conf["anon_username"]
        if len(ftp_conf["anon_root"]) == 0:
            vsftpd_conf.delete("anon_root")
        else:
            vsftpd_conf["anon_root"] = ftp_conf["anon_root"]

        conf_file = os.path.join(VSFTPD_ETC_CONF_DIR, VSFTPD_ETC_CONF_FILE)
        vsftpd_conf.apply_to(conf_file)

        # user_list file
        user_list_lines = []
        if ftp_conf["local_enable"] and ftp_conf["userlist_enable"]:
            for name, user_conf in ftp_conf["user_list"].items():
                if user_conf["login_enable"]:
                    user_list_lines.append(user_conf["user_name"] + "\n")
            if ftp_conf["anonymous_enable"]:
                user_list_lines.append("anonymous\n")
                user_list_lines.append("ftp\n")
        user_list_file = os.path.join(VSFTPD_ETC_CONF_DIR, VSFTPD_ETC_USER_LIST)
        with open(user_list_file, "w") as f:
            f.writelines(user_list_lines)

        # chroot_list file
        chroot_list_lines = []
        if ftp_conf["chroot_enable"] and ftp_conf["chroot_list"]:
            for name, user_conf in ftp_conf["user_list"].items():
                if user_conf["chroot_enable"]:
                    chroot_list_lines.append(user_conf["user_name"] + "\n")
        chroot_list_file = os.path.join(VSFTPD_ETC_CONF_DIR, VSFTPD_ETC_CHROOT_LIST)
        with open(chroot_list_file, "w") as f:
            f.writelines(chroot_list_lines)

    def sync_to_system_conf(self):
        """sync the ftp conf to /etc/vsftp/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            ftp_conf = self._load_conf()
            self._sync_to_system_conf(ftp_conf)

    def system_restore_cb(self):
        """sync the ftp conf to /etc/vsftp/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            ftp_conf = self._load_conf()
            self._sync_to_system_conf(ftp_conf)

    def set_ftp_conf(self, config={}, operator="unkown", **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)


        with self.lock:
            ftp_conf = self._load_conf()
            for name, value in config.items():
                if name == "user_list":
                    continue
                if name in ftp_conf and value is not None:
                    ftp_conf[name] = value

            # check config conflict
            ftp_conf = self.ftp_conf_schema.validate(ftp_conf)

            if ftp_conf["listen"] and ftp_conf["listen6"]:
                raise StorLeverError("listen and listen6 cannot both be true", 400)
            if ftp_conf["local_root"] != "" and \
                    (not os.path.exists(ftp_conf["local_root"])):
                 raise StorLeverError("local_root does not exist", 400)
            if ftp_conf["anon_root"] != "" and \
                    (not os.path.exists(ftp_conf["anon_root"])):
                 raise StorLeverError("anon_root does not exist", 400)
            try:
                user_mgr().get_user_info_by_name(ftp_conf["anon_username"])
            except Exception as e:
                raise StorLeverError("anon_username does not exist", 400)

            # save new conf
            self._save_conf(ftp_conf)
            self._sync_to_system_conf(ftp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "FTP config is updated by user(%s)" %
                   (operator))

    def get_ftp_conf(self):
        with self.lock:
            ftp_conf = self._load_conf()

        del ftp_conf["user_list"] # remove user_list field

        return ftp_conf

    def get_user_conf_list(self):
        user_conf_list = []
        with self.lock:
            ftp_conf = self._load_conf()
        for user_name, user_conf in ftp_conf["user_list"].items():
            user_conf_list.append({
                "user_name": user_name,
                "login_enable": user_conf["login_enable"],
                "chroot_enable": user_conf["chroot_enable"]
            })
        return user_conf_list

    def get_user_conf(self, user_name):
        with self.lock:
            ftp_conf = self._load_conf()
        user_conf = ftp_conf["user_list"].get(user_name)
        if user_conf is None:
            raise StorLeverError("user_name(%s) not found" % (user_name), 404)
        result = {
            "user_name": user_conf["user_name"],
            "login_enable": user_conf["login_enable"],
            "chroot_enable": user_conf["chroot_enable"]
        }
        return result

    def add_user_conf(self, user_name, login_enable=False, chroot_enable=False, operator="unkown"):
        with self.lock:
            ftp_conf = self._load_conf()
            if user_name in ftp_conf["user_list"]:
                 raise StorLeverError("user_name(%s) already exists" % (user_name), 404)
            try:
                user_mgr().get_user_info_by_name(user_name)
            except Exception as e:
                raise StorLeverError("user (%s) not found in system" % (user_name), 400)

            user_conf ={
                "user_name": user_name,
                "login_enable": login_enable,
                "chroot_enable": chroot_enable
            }
            ftp_conf["user_list"][user_name] = user_conf

            # save new conf
            self._save_conf(ftp_conf)
            self._sync_to_system_conf(ftp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "ftp user (%s) config is added by operator(%s)" %
                   (user_name, operator))

    def del_user_conf(self, user_name, operator="unkown"):
        with self.lock:
            ftp_conf = self._load_conf()
            user_conf = ftp_conf["user_list"].get(user_name)
            if user_conf is None:
                raise StorLeverError("user_name(%s) not found" % (user_name), 404)
            del ftp_conf["user_list"][user_name]

            # save new conf
            self._save_conf(ftp_conf)
            self._sync_to_system_conf(ftp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "ftp user (%s) config is deleted by operator(%s)" %
                   (user_name, operator))


    def set_user_conf(self, user_name, login_enable=None, chroot_enable=None, operator="unkown"):
        with self.lock:
            ftp_conf = self._load_conf()
            user_conf = ftp_conf["user_list"].get("user_name")
            if user_conf is None:
                raise StorLeverError("user_name(%s) not found" % (user_name), 404)
            if login_enable is not None:
                user_conf["login_enable"] = login_enable
            if chroot_enable is not None:
                user_conf["chroot_enable"] = chroot_enable

            # save new conf
            self._save_conf(ftp_conf)
            self._sync_to_system_conf(ftp_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "ftp user (%s) config is updated by operator(%s)" %
                   (user_name, operator))

FtpManager = FtpManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(FtpManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(FtpManager.system_restore_cb)
service_mgr().register_service("ftpd", "vsftpd", "/sbin/vsftpd", "FTP Server(vsftpd)")

# disable selinux impact
set_selinux_permissive()

def ftp_mgr():
    """return the global user manager instance"""
    return FtpManager








