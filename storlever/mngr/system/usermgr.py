"""
storlever.mngr.system.usermgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux user management.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import pwd
import grp
from crypt import crypt
import os

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging
from modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "user",
    "rpms": [
        "shadow-utils",
        "setup"
    ],
    "comment": "Provides the user/group management of the system, "
               "like query/add/del/configure user/group"
}



NO_LOGIN_SHELL = "/sbin/nologin"
LOGIN_SHELL = "/bin/bash"

class UserManager(object):
    """contains all methods to manage the user and group in linux system"""

    def __init__(self):
        pass

    def _get_groups_for_user(self, user):
        groups = grp.getgrall()
        user_groups = []
        for entry in groups:
            if user in entry.gr_mem:
                user_groups.append(entry.gr_name)
        return user_groups

    def _get_groups_for_all_user(self):
        groups = grp.getgrall()
        users = pwd.getpwall()
        user_groups = {}
        for entry in users:
            user_groups[entry.pw_name] = []

        for entry in groups:
            for member in entry.gr_mem:
                user_groups[member].append(entry.gr_name)

        return user_groups

    def _get_gid_name_dict(self):
        groups = grp.getgrall()
        gid_name = {}
        for entry in groups:
            gid_name[entry.gr_gid] = entry.gr_name
        return gid_name

    def user_list(self):
        gid_name = self._get_gid_name_dict()
        user_groups = self._get_groups_for_all_user()
        users = pwd.getpwall()

        return_list = []
        for entry in users:

            return_entry = {
                "name": entry.pw_name,
                "uid": entry.pw_uid,
                "password": entry.pw_passwd,
                "comment": entry.pw_gecos,
                "primary_group": gid_name.get(entry.pw_gid, "unknown"),
                "groups": ",".join(user_groups[entry.pw_name]),
                "home_dir": entry.pw_dir,
                "login": "nologin" not in entry.pw_shell
            }

            return_list.append(return_entry)
        return return_list

    def get_user_info_by_name(self, name):
        try:
            user = pwd.getpwnam(name)
            return_entry = {
                "name": user.pw_name,
                "uid": user.pw_uid,
                "password": user.pw_passwd,
                "comment": user.pw_gecos,
                "primary_group": grp.getgrgid(user.pw_gid).gr_name,
                "groups": ",".join(self._get_groups_for_user(name)),
                "home_dir": user.pw_dir,
                "login": "nologin" not in user.pw_shell
            }
            return return_entry
        except KeyError as e:
            raise StorLeverError(str(e), 404)

    def group_list(self):
        groups = grp.getgrall()
        return_groups = []
        for entry in groups:
            return_entry = {
                "name": entry.gr_name,
                "gid": entry.gr_gid,
                "member": entry.gr_mem
            }
            return_groups.append(return_entry)
        return return_groups

    def get_group_by_name(self, name):
        try:
            group = grp.getgrnam(name)
            return_entry = {
                "name": group.gr_name,
                "gid": group.gr_gid,
                "member": group.gr_mem
            }
            return return_entry
        except KeyError as e:
            raise StorLeverError(str(e), 404)

    def user_add(self, name, password=None, uid=None,
                 primary_group=None, groups=None,
                 home_dir=None, login=None,
                 comment=None, user="unknown"):
        cmds = ["/usr/sbin/useradd"]
        if uid is not None:
            cmds.append("-u")
            cmds.append("%d" % int(uid))
        if primary_group is not None:
            cmds.append("-g")
            cmds.append(primary_group)
        if groups is not None:
            cmds.append("-G")
            cmds.append(groups)
        if comment is not None:
            cmds.append("-c")
            cmds.append(comment)
        if password is not None:
            cmds.append("-p")
            enc_passwd = crypt(password, "ab")
            cmds.append(enc_passwd)
        if login is not None:
            cmds.append("-s")
            if not login:
                cmds.append(NO_LOGIN_SHELL)
            else:
                cmds.append(LOGIN_SHELL)

        if home_dir is not None:
            cmds.append("-d")
            cmds.append(home_dir)

        cmds.append(name)
        check_output(cmds, input_ret=[2, 3, 4, 6, 9])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "New system user %s is created by user(%s)" %
                   (name, user))

    def group_add(self, name, gid=None, user="unknown"):
        cmds = ["/usr/sbin/groupadd"]
        if gid is not None:
            cmds.append("-g")
            cmds.append("%d" % int(gid))
        cmds.append(name)
        check_output(cmds, input_ret=[2, 3, 4, 9])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "New system group %s is created by user(%s)" %
                   (name, user))

    def user_del_by_name(self, name, user="unknown"):
        if name == "root":
            raise StorLeverError("cannot del user root", 400)
        cmds = ["/usr/sbin/userdel"]
        cmds.append(name)
        check_output(cmds, input_ret=[2, 6, 8])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "System user %s is deleted by user(%s)" %
                   (name, user))

    def user_mod(self, name, password=None, uid=None,
                 primary_group=None, groups=None,
                 home_dir=None, login=None,
                 comment=None, user="unknown"):

        if name == "root":
            raise StorLeverError("cannot modify user root", 400)

        cmds = ["/usr/sbin/usermod"]
        if uid is not None:
            cmds.append("-u")
            cmds.append("%d" % int(uid))
        if primary_group is not None:
            cmds.append("-g")
            cmds.append(primary_group)
        if groups is not None:
            cmds.append("-G")
            cmds.append(groups)
        if comment is not None:
            cmds.append("-c")
            cmds.append(comment)
        if password is not None:
            cmds.append("-p")
            enc_passwd = crypt(password, "ab")
            cmds.append(enc_passwd)
        if login is not None:
            cmds.append("-s")
            if not login:
                cmds.append(NO_LOGIN_SHELL)
            else:
                cmds.append(LOGIN_SHELL)

        if home_dir is not None:
            cmds.append("-d")
            cmds.append(home_dir)
            if not os.path.exists(home_dir):
                cmds.append("-m")


        cmds.append(name)
        if len(cmds) > 2:
            check_output(cmds, input_ret=[4, 6, 12])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "System user %s is modified by user(%s)" %
                   (name, user))

    def group_del_by_name(self, name, user="unknown"):
        if name == "root":
            raise StorLeverError("cannot del group root", 400)
        cmds = ["/usr/sbin/groupdel"]
        cmds.append(name)
        check_output(cmds, input_ret=[2, 6, 8])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "System group %s is deleted by user(%s)" %
                   (name, user))

UserManager = UserManager()

ModuleManager.register_module(**MODULE_INFO)

def user_mgr():
    """return the global user manager instance"""
    return UserManager






