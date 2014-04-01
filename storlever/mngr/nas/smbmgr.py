"""
storlever.mngr.nas.smbmgr
~~~~~~~~~~~~~~~~

This module implements samba server management.

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


SMB_CONF_FILE_NAME = "smb_conf.yaml"
SMB_ETC_CONF_DIR = "/etc/samba/"
SMB_ETC_CONF_FILE = "smb.conf"
SMBSTATUS_CMD = "/usr/bin/smbstatus"
PDBEDIT_CMD = "/usr/bin/pdbedit"

SHARE_CONF_SCHEMA = Schema({
    # Name of this share
    "share_name": Use(str),

    # This parameter specifies a directory to which the user of the service is to
    # be given access.default is empty
    Optional("path"): Default(Use(str), default=""),

    # This is a text field that is seen next to a share when a client does a
    # queries the server, either via the network neighborhood or via net view to
    # list what shares are available. Default is empty
    Optional("comment"): Default(Use(str), default=""),


    # When a file is created, the necessary permissions are calculated according
    # to the mapping from DOS modes to UNIX permissions, and the resulting UNIX
    # mode is then bit-wise ?AND?ed with this parameter. This parameter may be
    # thought of as a bit-wise MASK for the UNIX modes of a file. Any bit not set
    # here will be removed from the modes set on a file when it is created.
    # Default is 0744, which means  removes the group and other write and
    # execute bits from the UNIX modes.
    Optional("create_mask"): Default(IntVal(min=0, max=0777), default=0744),

    # This parameter is the octal modes which are used when converting DOS modes
    # to UNIX modes when creating UNIX directories.
    # When a directory is created, the necessary permissions are calculated
    # according to the mapping from DOS modes to UNIX permissions, and the
    # resulting UNIX mode is then bit-wise ANDed with this parameter. This
    # parameter may be thought of as a bit-wise MASK for the UNIX modes of a
    # directory. Any bit not set here will be removed from the modes set on a
    # directory when it is created
    # default is 755, which means removes the ?group? and ?other? write
    # bits from the UNIX mode, allowing only the user who owns the directory to
    # modify it.
    Optional("directory_mask"): Default(IntVal(min=0, max=0777), default=0755),

    #  If this parameter is True for a share, then no password is required to
    # connect to the share. Privileges will be those of the guest account..
    Optional("guest_ok"): Default(BoolVal(), default=False),

    #  If this parameter is true, then users of a service may not create or modify
    # files in the service?s directory..
    Optional("read_only"): Default(BoolVal(), default=True),

    # This controls whether this share is seen in the list of available shares in
    # a net view and in the browse list..
    Optional("browseable"): Default(BoolVal(), default=True),


    # This is a list of users that should be allowed to login to this service.
    # If this is empty (the default) then any user can login
    Optional("valid_users"): Default(Use(str), default=""),

    # This is a list of users that are given read-write access to a service. If
    # the connecting user is in this list then they will be given write access,
    # no matter what the read only option is set to.
    Optional("write_list"): Default(Use(str), default=""),

    # This is a list of files and directories that are neither visible nor
    # accessible. Each entry in the list must be separated by a /, which allows
    # spaces to be included in the entry. * and ? can be used to specify
    # multiple files or directories as in DOS wildcards.
    # Each entry must be a unix path, not a DOS path and must not include the
    # unix directory separator /
    Optional("veto_files"): Default(Use(str), default=""),

    # This parameter specifies a set of UNIX mode bit permissions that will
    # always be set on a file created by Samba. This is done by bitwise ORing
    # these bits onto the mode bits of a file that is being created. The default
    # for this parameter is (in octal) 000. The modes in this parameter are
    # bitwise ORed onto the file mode after the mask set in the create mask
    # parameter is applied.
    Optional("force_create_mode"): Default(IntVal(min=0, max=0777), default=0),

    # This parameter specifies a set of UNIX mode bit permissions that will
    # always be set on a directory created by Samba. This is done by bitwise
    # ?OR?ing these bits onto the mode bits of a directory that is being created.
    # The default for this parameter is (in octal) 0000 which will not add any
    # extra permission bits to a created directory. This operation is done after
    # the mode mask in the parameter directory mask is applied
    Optional("force_directory_mode"): Default(IntVal(min=0, max=0777), default=0),

    DoNotCare(str): Use(str)  # for all those key we don't care

})

SMB_CONF_SCHEMA = Schema({
    # workgroup controls what workgroup your server will appear to be in when queried
    # by clients. Note that this parameter also controls the Domain name used
    #  with the security = domain setting,
    Optional("workgroup"): Default(Use(str), default="MYGROUP"),

    # This controls what string will show up in the printer comment box in print
    # manager and next to the IPC connection in net view. It can be any string
    # that you wish to show to your users.
    Optional("server_string"): Default(Use(str), default="Storlever Samba %v"),

    #  This sets the NetBIOS name by which a Samba server is known. By default it
    # is empty, means the same as the first component of the host's DNS name. If a machine is
    # a browse server or logon server this name (or the first component of the
    # hosts DNS name) will be the name that these services are advertised under
    Optional("netbios_name"): Default(Use(str), default=""),

    # This parameter is a comma, space, or tab delimited set of hosts which are
    # permitted to access a service. Default is empty, means all hosts can access
    Optional("hosts_allow"): Default(Use(str), default=""),

    # This option affects how clients respond to Samba, which can share/user/server/domain/ads
    # default is user
    Optional("security"): Default(Use(str), default="user"),

    # This option allows the administrator to chose which backend will be used
    # for storing user and possibly group information. This allows you to swap
    # between different storage mechanisms without recompile. default is tdbsam
    Optional("passdb_backend"): Default(Use(str), default="tdbsam"),

    # specifying the name of another SMB server or Active Directory domain
    # controller with this option, and using security = [ads|domain|server] it is
    # possible to get Samba to do all its username/password validation using a
    # specific remote server. Default is empty, means auto locate.
    Optional("password_server"): Default(Use(str), default=""),

    # This option specifies the kerberos realm to use. The realm is used as the
    # ADS equivalent of the NT4 domain. It is usually set to the DNS name of the
    # kerberos server..
    Optional("realm"): Default(Use(str), default=""),

    #  This is a username which will be used for access to services which are
    # specified as guest ok (see below). Whatever privileges this user has will
    # be available to any client connecting to the guest service. This user must
    # exist in the password file, but does not require a valid login..
    Optional("guest_account"): Default(Use(str), default="nobody"),

    # This controls whether the auto-home share is seen in the list of available shares in
    # a net view and in the browse list
    Optional("browseable"): Default(BoolVal(), default=False),

    Optional("share_list"):  Default(Schema({DoNotCare(str): SHARE_CONF_SCHEMA}),
                                       default={}),

    DoNotCare(str): Use(str)  # for all those key we don't care
})

class SmbManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, SMB_CONF_FILE_NAME)
        self.share_conf_schema = SHARE_CONF_SCHEMA
        self.smb_conf_schema = SMB_CONF_SCHEMA

    def _load_conf(self):
        smb_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            smb_conf = \
                Config.from_file(self.conf_file, self.smb_conf_schema).conf
        else:
            smb_conf = self.smb_conf_schema.validate(smb_conf)
        return smb_conf

    def _save_conf(self, smb_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, smb_conf)

    def _bool_to_yn(self, value):
        if value:
            return "yes"
        else:
            return "no"

    def _sync_to_system_conf(self, smb_conf):

        if not os.path.exists(SMB_ETC_CONF_DIR):
            os.makedirs(SMB_ETC_CONF_DIR)

        smb_etc_conf_file = os.path.join(SMB_ETC_CONF_DIR, SMB_ETC_CONF_FILE)
        if os.path.exists(smb_etc_conf_file):
            smb_etc_conf = ini(smb_etc_conf_file)
        else:
            smb_etc_conf = ini()

        # global configs
        if "global" not in smb_etc_conf:
            smb_etc_conf["global"] = properties()

        if smb_conf["workgroup"] == "":
            smb_etc_conf["global"].delete("workgroup")
        else:
            smb_etc_conf["global"]["workgroup"] = smb_conf["workgroup"]

        smb_etc_conf["global"]["server string"] = smb_conf["server_string"]

        if smb_conf["netbios_name"] == "":
            smb_etc_conf["global"].delete("netbios name")
        else:
            smb_etc_conf["global"]["netbios name"] = smb_conf["netbios_name"]

        if smb_conf["hosts_allow"] == "":
            smb_etc_conf["global"].delete("hosts allow")
        else:
            smb_etc_conf["global"]["hosts allow"] = smb_conf["hosts_allow"]

        smb_etc_conf["global"]["security"] = smb_conf["security"]

        if smb_conf["passdb_backend"] == "":
            smb_etc_conf["global"].delete("passdb backend")
        else:
            smb_etc_conf["global"]["passdb backend"] = smb_conf["passdb_backend"]

        if smb_conf["password_server"] == "":
            smb_etc_conf["global"].delete("password server")
        else:
            smb_etc_conf["global"]["password server"] = smb_conf["password_server"]

        if smb_conf["realm"] == "":
            smb_etc_conf["global"].delete("realm")
        else:
            smb_etc_conf["global"]["realm"] = smb_conf["realm"]

        if smb_conf["guest_account"] == "":
            smb_etc_conf["global"].delete("guest account")
        else:
            smb_etc_conf["global"]["guest account"] = smb_conf["guest_account"]

        smb_etc_conf["global"]["browseable"] = self._bool_to_yn(smb_conf["browseable"])

        # for share configs
        for share_name, share_conf in smb_conf["share_list"].items():
            if share_name not in smb_etc_conf:
                smb_etc_conf[share_name] = properties()

            if share_conf["path"] == "":
                smb_etc_conf[share_name].delete("path")
            else:
                smb_etc_conf[share_name]["path"] = share_conf["path"]

            if share_conf["comment"] == "":
                smb_etc_conf[share_name].delete("comment")
            else:
                smb_etc_conf[share_name]["comment"] = share_conf["comment"]

            smb_etc_conf[share_name]["create mask"] = "0%03o" % share_conf["create_mask"]

            smb_etc_conf[share_name]["directory mask"] = "0%03o" % share_conf["directory_mask"]

            smb_etc_conf[share_name]["guest ok"] = self._bool_to_yn(share_conf["guest_ok"])

            smb_etc_conf[share_name]["read only"] = self._bool_to_yn(share_conf["read_only"])

            smb_etc_conf[share_name]["browseable"] = self._bool_to_yn(share_conf["browseable"])

            smb_etc_conf[share_name]["force create mode"] = "0%03o" % share_conf["force_create_mode"]

            smb_etc_conf[share_name]["force directory mode"] = "0%03o" % share_conf["force_directory_mode"]

            if share_conf["valid_users"] == "":
                smb_etc_conf[share_name].delete("valid users")
            else:
                smb_etc_conf[share_name]["valid users"] = share_conf["valid_users"]

            if share_conf["write_list"] == "":
                smb_etc_conf[share_name].delete("write list")
            else:
                smb_etc_conf[share_name]["write list"] = share_conf["write_list"]

            if share_conf["veto_files"] == "":
                smb_etc_conf[share_name].delete("veto files")
            else:
                smb_etc_conf[share_name]["veto files"] = share_conf["veto_files"]

        # delete other shares
        old_share_list = smb_etc_conf.keys()
        for share_name in old_share_list:
            if share_name != "global" and share_name not in smb_conf["share_list"]:
                del smb_etc_conf[share_name]

        smb_etc_conf.write()

    def sync_to_system_conf(self):
        """sync the smb conf to /etc/samba/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            smb_conf = self._load_conf()
            self._sync_to_system_conf(smb_conf)

    def system_restore_cb(self):
        """sync the smb conf to /etc/samba/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            smb_conf = self._load_conf()
            self._sync_to_system_conf(smb_conf)

    def set_smb_conf(self, config={}, operator="unkown", **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)

        if "guest_account" in config and config["guest_account"] is not None:
            try:
                user_mgr().get_user_info_by_name(config["guest_account"])
            except Exception as e:
                raise StorLeverError("guest_account does not exist", 400)

        with self.lock:
            smb_conf = self._load_conf()
            for name, value in config.items():
                if name == "share_list":
                    continue
                if name in smb_conf and value is not None:
                    smb_conf[name] = value

            # check config conflict
            smb_conf = self.smb_conf_schema.validate(smb_conf)

            # save new conf
            self._save_conf(smb_conf)
            self._sync_to_system_conf(smb_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Samba config is updated by user(%s)" %
                   (operator))

    def get_smb_conf(self):
        with self.lock:
            smb_conf = self._load_conf()

        del smb_conf["share_list"] # remove user_list field

        return smb_conf

    def get_share_conf_list(self):
        share_conf_list = []
        with self.lock:
            smb_conf = self._load_conf()
        for share_name, share_conf in smb_conf["share_list"].items():
            share_conf_list.append(share_conf)
        return share_conf_list

    def get_share_conf(self, share_name):
        with self.lock:
            smb_conf = self._load_conf()
        share_conf = smb_conf["share_list"].get(share_name)
        if share_conf is None:
            raise StorLeverError("share_name(%s) not found" % (share_name), 404)

        return share_conf

    def add_share_conf(self, share_name, path="", comment="",
                       create_mask=0744, directory_mask=0755, guest_ok=False,
                       read_only=True, browseable=True, force_create_mode=0,
                       force_directory_mode=0, valid_users="", write_list="",
                       veto_files="", operator="unkown"):

        if path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        share_conf ={
            "share_name": share_name,
            "path": path,
            "comment": comment,
            "create_mask": create_mask,
            "directory_mask": directory_mask,
            "guest_ok": guest_ok,
            "read_only": read_only,
            "browseable": browseable,
            "force_create_mode": force_create_mode,
            "force_directory_mode": force_directory_mode,
            "valid_users": valid_users,
            "write_list": write_list,
            "veto_files": veto_files
        }
        share_conf = self.share_conf_schema.validate(share_conf)

        with self.lock:
            smb_conf = self._load_conf()
            if share_name in smb_conf["share_list"]:
                 raise StorLeverError("share_name(%s) already exists" % (share_name), 400)



            smb_conf["share_list"][share_name] = share_conf

            # save new conf
            self._save_conf(smb_conf)
            self._sync_to_system_conf(smb_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "samba share (%s) config is added by operator(%s)" %
                   (share_name, operator))

    def del_share_conf(self, share_name, operator="unkown"):
        with self.lock:
            smb_conf = self._load_conf()
            share_conf = smb_conf["share_list"].get(share_name)
            if share_conf is None:
                raise StorLeverError("share_name(%s) not found" % (share_name), 404)
            del smb_conf["share_list"][share_name]

            # save new conf
            self._save_conf(smb_conf)
            self._sync_to_system_conf(smb_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "samba share (%s) config is deleted by operator(%s)" %
                   (share_name, operator))

    def set_share_conf(self, share_name, path=None, comment=None,
                       create_mask=None, directory_mask=None, guest_ok=None,
                       read_only=None, browseable=None, force_create_mode=None,
                       force_directory_mode=None, valid_users=None, write_list=None,
                       veto_files=None, operator="unkown"):

        if path is not None and path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        with self.lock:
            smb_conf = self._load_conf()
            share_conf = smb_conf["share_list"].get(share_name)
            if share_conf is None:
                raise StorLeverError("share_conf(%s) not found" % (share_conf), 404)

            if path is not None:
                share_conf["path"] = path
            if comment is not None:
                share_conf["comment"] = comment
            if create_mask is not None:
                share_conf["create_mask"] = create_mask
            if directory_mask is not None:
                share_conf["directory_mask"] = directory_mask
            if guest_ok is not None:
                share_conf["guest_ok"] = guest_ok
            if read_only is not None:
                share_conf["read_only"] = read_only
            if browseable is not None:
                share_conf["browseable"] = browseable
            if force_create_mode is not None:
                share_conf["force_create_mode"] = force_create_mode
            if force_directory_mode is not None:
                share_conf["force_directory_mode"] = force_directory_mode
            if valid_users is not None:
                share_conf["valid_users"] = valid_users
            if write_list is not None:
                share_conf["write_list"] = write_list
            if veto_files is not None:
                share_conf["veto_files"] = veto_files


            # save new conf
            self._save_conf(smb_conf)
            self._sync_to_system_conf(smb_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "samba share (%s) config is updated by operator(%s)" %
                   (share_name, operator))

    def get_connection_list(self):
        connections = []
        pids = {}

        ll = check_output([SMBSTATUS_CMD, '-p']).splitlines()
        if len(ll) >= 5 and "anonymous mode" in ll[4]:
            return connections
        for l in ll[4:]:
            s = l.split()
            if len(s) > 0:
                pids[s[0]] = (s[1], ' '.join(s[3:]))

        ll = check_output([SMBSTATUS_CMD, '-S']).splitlines()
        for l in ll[3:]:
            s = l.split()
            if len(s) > 0 and s[1] in pids:
                c = {
                    "share_name": s[0],
                    "pid": s[1],
                    "user": pids[s[1]][0],
                    "machine":  pids[s[1]][1],
                    "when": ' '.join(s[3:])
                }
                connections.append(c)

        return connections

    def add_smb_account(self, username, password, operator="unkown"):
        p = subprocess.Popen([PDBEDIT_CMD, '-at', '-u', username],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.communicate('%s\n%s\n\n' % (password, password))
        if p.returncode != 0:
            raise StorLeverError("failed to add user(%s)" % (username), 400)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Samba user (%s) is added into password DB by operator(%s)" %
                   (username, operator))

    def del_smb_account(self,username, operator="unkown"):
        check_output([PDBEDIT_CMD, '-x', '-u', username])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Samba user (%s) is delete from password DB by operator(%s)" %
                   (username, operator))

    def get_smb_account_list(self):
        account_list = []
        for un in [s.split(':')[0] for s in check_output([PDBEDIT_CMD, '-L', '-d0']).split('\n')]:
            if un and not ' ' in un and not un.startswith('WARNING'):
                lines = subprocess.check_output(['pdbedit', '-Lv', '-d0', '-u', un]).split('\n')
                fields = {}
                for l in lines:
                    if l and ':' in l:
                        l = l.split(':', 1)
                        fields[l[0]] = l[1].strip()
                u = {
                    "username": un,
                    "sid": fields['User SID']
                }
                account_list.append(u)
        return account_list

    def set_smb_account_passwd(self, username, password, operator="unkown"):
        p = subprocess.Popen([PDBEDIT_CMD, '-at', '-u', username],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.communicate('%s\n%s\n\n' % (password, password))
        if p.returncode != 0:
            raise StorLeverError("failed to add user(%s)" % (username), 400)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Samba user (%s) password is updated operator(%s)" %
                   (username, operator))


SmbManager = SmbManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(SmbManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(SmbManager.system_restore_cb)
service_mgr().register_service("smb", "smb", "smbd", "Samba Server")
service_mgr().register_service("nmb", "nmb", "smbd", "Netbios Name Server")

# disable selinux impact
set_selinux_permissive()

def smb_mgr():
    """return the global user manager instance"""
    return SmbManager








