"""
storlever.mngr.system.usermgr
~~~~~~~~~~~~~~~~

This module implements some functions of linux user management.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import pwd
import grp
from crypt import crypt

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
import logging


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
                "primay_group": gid_name.get(entry.pw_gid, "unknown"),
                "groups": ",".join(user_groups[entry.pw_name])
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
                "primay_group": grp.getgrgid(user.pw_gid).gr_name,
                "groups": ",".join(self._get_groups_for_user(name))
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

    def user_add(self, name, password="", uid=-1, primary_group=-1, groups="", comment="", user="unknown"):
        cmds = ["/usr/sbin/useradd"]
        if uid != -1:
            cmds.append("-u")
            cmds.append("%d" % int(uid))
        if primary_group != -1:
            cmds.append("-g")
            cmds.append(primary_group)
        if groups != "":
            cmds.append("-G")
            cmds.append(groups)
        if comment != "":
            cmds.append("-c")
            cmds.append(comment)
        if password != "":
            cmds.append("-p")
            enc_passwd = crypt(password, "ab")
            cmds.append(enc_passwd)

        cmds.append("-M")
        cmds.append(name)
        check_output(cmds, input_ret=[2, 3, 4, 6, 9])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "New system user %s is created by user(%s)" %
                   (name, user))

    def group_add(self, name, gid=-1, user="unknown"):
        cmds = ["/usr/sbin/groupadd"]
        if gid != -1:
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

    def user_mod(self, name, password="", uid=-1, primary_group=-1, groups="", comment="", user="unknown"):

        if name == "root":
            raise StorLeverError("cannot modify user root", 400)

        cmds = ["/usr/sbin/usermod"]
        if uid != -1:
            cmds.append("-u")
            cmds.append("%d" % int(uid))
        if primary_group != -1:
            cmds.append("-g")
            cmds.append(primary_group)
        if groups != "":
            cmds.append("-G")
            cmds.append(groups)
        if comment != "":
            cmds.append("-c")
            cmds.append(comment)
        if password != "":
            cmds.append("-p")
            enc_passwd = crypt(password, "ab")
            cmds.append(enc_passwd)

        cmds.append(name)
        check_output(cmds, input_ret=[4, 6])
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

user_manager = UserManager()


def user_mgr():
    """return the global user manager instance"""
    return user_manager






