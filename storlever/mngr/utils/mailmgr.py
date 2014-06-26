"""
storlever.mngr.utils.mailmgr
~~~~~~~~~~~~~~~~

This module implements sending mail management

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path
import subprocess

from storlever.lib.config import Config
from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError, StorLeverCmdError
from storlever.lib import logger

import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal

from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr

from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "mail",
    "rpms": [
        "mailx"
    ],
    "comment": "Provides the support to send email by mailx utility"
}


MAIL_CONF_FILE_NAME = "mail_conf.yaml"
MAIL_ETC_CONF_DIR = "/etc/"
MAIL_ETC_CONF_FILE = "mail.rc"
MAIL_CMD = "/bin/mail"


MAIL_CONF_SCHEMA = Schema({

    # the email address of user's account, it would also be place in the FROM header of the email
    Optional("email_addr"):  Default(Use(str), default=""),

    # smtp server address to send the mail
    Optional("smtp_server"):  Default(Use(str), default=""),

    # password for the account
    Optional("password"):  Default(Use(str), default=""),


    DoNotCare(str): object  # for all those key we don't care
})


class MailManager(object):
    """contains all methods to manage NTP server in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, MAIL_CONF_FILE_NAME)
        self.mail_conf_schema = MAIL_CONF_SCHEMA


    def _load_conf(self):
        mail_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            mail_conf = \
                Config.from_file(self.conf_file, self.mail_conf_schema).conf
        else:
            mail_conf = self.mail_conf_schema.validate(mail_conf)
        return mail_conf

    def _save_conf(self, mail_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, mail_conf)


    def _sync_to_system_conf(self, mail_conf):

        # get username from user address
        username, sep, host = mail_conf["email_addr"].partition("@")

        if not os.path.exists(MAIL_ETC_CONF_DIR):
            os.makedirs(MAIL_ETC_CONF_DIR)

        file_name = os.path.join(MAIL_ETC_CONF_DIR, MAIL_ETC_CONF_FILE)
        with open(file_name, "r") as f:
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

        with open(file_name, "w") as f:
            f.writelines(before_storlever)
            f.write("# begin storlever\n")
            if mail_conf["email_addr"] != "":
                f.write("set from=%s\n" % mail_conf["email_addr"])

            if mail_conf["smtp_server"] != "":
                f.write("set smtp=%s\n" % mail_conf["smtp_server"])
                if username != "":
                    f.write("set smtp-auth-user=%s\n" % username)
                if mail_conf["password"] != "":
                    f.write("set smtp-auth-password=%s\n" % mail_conf["password"])

            f.write("# end storlever\n")
            f.writelines(after_storlever)


    def sync_to_system_conf(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp.conf"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            mail_conf = self._load_conf()
            self._sync_to_system_conf(mail_conf)

    def system_restore_cb(self, *args, **kwargs):
        """sync the ntp conf to /etc/ntp"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            mail_conf = self._load_conf()
            self._sync_to_system_conf(mail_conf)


    def set_mail_conf(self, config={}, operator="unkown", *args, **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)

        with self.lock:
            mail_conf = self._load_conf()
            for name, value in config.items():
                if name in mail_conf and value is not None:
                    mail_conf[name] = value

            # check config conflict
            mail_conf = self.mail_conf_schema.validate(mail_conf)
            if mail_conf["smtp_server"] != "":
                if mail_conf["email_addr"] == "":
                    raise StorLeverError("email_addr cannot be empty if smtp_server exists", 400)
                if mail_conf["password"] == "":
                    raise StorLeverError("password cannot be empty if smtp_server exists", 400)

            # save new conf
            self._save_conf(mail_conf)
            self._sync_to_system_conf(mail_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "Mail config is updated by operator(%s)" %
                   (operator))

    def get_mail_conf(self, *args, **kwargs):
        with self.lock:
            mail_conf = self._load_conf()

        return mail_conf

    def send_email(self, to, subject, content, debug=False):
        """send email, return the debug info """
        cmds = [MAIL_CMD]
        if debug:
            cmds.append('-v')
        cmds.append('-s')
        cmds.append(str(subject))
        cmds.append(str(to))

        p = subprocess.Popen(cmds,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate(content)
        if p.returncode != 0:
            raise StorLeverCmdError(p.returncode, err, 400)
        return err



MailManager = MailManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(MailManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(MailManager.system_restore_cb)
ModuleManager.register_module(**MODULE_INFO)

def mail_mgr():
    """return the global user manager instance"""
    return MailManager

