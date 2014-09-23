"""
storlever.mngr.san.tgt.tgtmgr
~~~~~~~~~~~~~~~~

This module implements iscsi targets management.
Linux has multi kinds of targets manage utils, this manager make use of stgt
to output iscsi targets

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path

from storlever.lib.config import Config
from storlever.lib.command import check_output, set_selinux_permissive
from storlever.lib.exception import StorLeverError
from storlever.lib.utils import filter_dict
from storlever.lib import logger
import logging
from storlever.lib.schema import Schema, Use, Optional, \
    Default, DoNotCare, BoolVal, IntVal, AutoDel


TGT_CONF_FILE_NAME = "tgt_conf.yaml"
TGT_ETC_CONF_DIR = "/etc/tgt/"
TGT_ETC_CONF_FILE = "targets.conf"
TGT_ETC_STORLEVER_FILE = "targets.storlever.conf"
TGTADMIN_CMD = "/usr/sbin/tgt-admin"

from storlever.lib.lock import lock
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from target import Target
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "tgt",
    "rpms": [
        "scsi-target-utils",
    ],
    "comment": "Provides the management functions for iscsi target server(tgt)"
}



LUN_CONF_SCHEMA = Schema({

    # lun number
    "lun": IntVal(1, 255),

    # path to a regular file, or block device, or a sg char device
    "path": Use(str),

    # the type of device . Possible device-types are:
    # disk    : emulate a disk device
    # tape    : emulate a tape reader
    # ssc     : same as tape
    # cd      : emulate a DVD drive
    # changer : emulate a media changer device
    # pt      : passthrough type to export a /dev/sg device
    Optional("device_type"): Default(Use(str), default="disk"),

    # the type of backend storage. Possible backend types are:
    # rdwr    : Use normal file I/O. This is the default for disk devices
    # aio     : Use Asynchronous I/O
    # sg      : Special backend type for passthrough devices
    #  ssc     : Special backend type for tape emulation
    Optional("bs_type"): Default(Use(str), default="rdwr"),

    # if true, a direct mapped logical unit (LUN) with the same properties as the
    # physical device (such as VENDOR_ID, SERIAL_NUM, etc.)
    Optional("direct_map"): Default(BoolVal(), default=False),

    # enable write cache or not
    Optional("write_cache"): Default(BoolVal(), default=True),

    # readonly an read-write
    Optional("readonly"): Default(BoolVal(), default=False),

    # online or offline
    Optional("online"): Default(BoolVal(), default=True),
    
    # scsi id, if empty, it would automatically be set to a default value
    Optional("scsi_id"): Default(Use(str), default=""),

    # scsi id, if empty, it would automatically be set to a default value
    Optional("scsi_sn"): Default(Use(str), default=""),

    AutoDel(str): object  # for all other key we auto delete
})


TARGET_CONF_SCHEMA = Schema({
    # iqn of this target
    "iqn": Use(str),

    # Allows connections only from the specified IP address. Defaults to ALL if
    # no initiator-address directive is specified.
    Optional("initiator_addr_list"): Default([Use(str)], default=[]),

    # Allows connections only from the specified initiator name.
    Optional("initiator_name_list"): Default([Use(str)], default=[]),

    # Define iscsi incoming authentication setting. If no "incominguser" is
    # specified, it is not used.
    Optional("incominguser_list"): Default([Use(str)], default=[]),

    # Define iscsi outgoing authentication setting. If no "outgoinguser" is
    # specified, it is not used.
    Optional("outgoinguser_list"): Default([Use(str)], default=[]),

    Optional("lun_list"): Default([LUN_CONF_SCHEMA], default=[]),

    AutoDel(str): object  # for all other key we auto delete

})

TGT_CONF_SCHEMA = Schema({


    # Define iscsi incoming discovery authentication setting. If it is
    # empty, no authentication is performed. The format is username:passwd
    Optional("incomingdiscoveryuser"): Default(Use(str), default=""),

    # Define iscsi outgoing discovery authentication setting. If it is
    # empty, no authentication is performe  The format is username:passwd
    Optional("outgoingdiscoveryuser"): Default(Use(str), default=""),

    # target list
    Optional("target_list"):  Default([TARGET_CONF_SCHEMA], default=[]),

    AutoDel(str): object  # for all other key we auto delete
})

class TgtManager(object):
    """contains all methods to manage ethernet interface in linux system"""

    def __init__(self):
        # need a mutex to protect create/delete bond interface
        self.lock = lock()
        self.conf_file = os.path.join(STORLEVER_CONF_DIR, TGT_CONF_FILE_NAME)
        self.lun_conf_schema = LUN_CONF_SCHEMA
        self.target_conf_schema = TARGET_CONF_SCHEMA
        self.tgt_conf_schema = TGT_CONF_SCHEMA

    def _load_conf(self):
        tgt_conf = {}
        cfg_mgr().check_conf_dir()
        if os.path.exists(self.conf_file):
            tgt_conf = \
                Config.from_file(self.conf_file, self.tgt_conf_schema).conf
        else:
            tgt_conf = self.tgt_conf_schema.validate(tgt_conf)
        return tgt_conf

    def _save_conf(self, tgt_conf):
        cfg_mgr().check_conf_dir()
        Config.to_file(self.conf_file, tgt_conf)

    def _get_target_conf(self, iqn):
        tgt_conf = self._load_conf()
        for target_conf in tgt_conf["target_list"]:
            if target_conf["iqn"] == iqn:
                return target_conf
        raise StorLeverError("Target (iqn:%s) Not Found" % iqn, 404)

    def _set_target_conf(self, iqn, new_target_conf):
        tgt_conf = self._load_conf()
        for i, target_conf in enumerate(tgt_conf["target_list"]):
            if target_conf["iqn"] == iqn:
                tgt_conf["target_list"][i] = new_target_conf
                self._save_conf(tgt_conf)
                self._sync_to_system_conf(tgt_conf)
                return
        raise StorLeverError("Target (iqn:%s) Not Found" % iqn, 404)


    def _lun_conf_to_line(self, lun_conf):
        if lun_conf["direct_map"]:
            line = "<direct-store %s>\n" % lun_conf["path"]
        else:
            line = "<backing-store %s>\n" % lun_conf["path"]

        line += "lun %d\n" % lun_conf["lun"]
        line += "device-type %s\n" % lun_conf["device_type"]
        line += "bs-type %s\n" % lun_conf["bs_type"]
        if lun_conf["scsi_id"] != "":
            line += "scsi_id %s\n" % lun_conf["scsi_id"]
        if lun_conf["scsi_sn"] != "":
            line += "scsi_sn %s\n" % lun_conf["scsi_sn"]
        if lun_conf["write_cache"]:
            line += "write-cache on\n"
        else:
            line += "write-cache off\n"

        if lun_conf["readonly"]:
            line += "readonly 1\n"
        else:
            line += "readonly 0\n"

        if lun_conf["online"]:
            line += "online 1\n"
        else:
            line += "online 0\n"

        if lun_conf["direct_map"]:
            line += "</direct-store>\n"
        else:
            line += "</backing-store>\n"

        return line

    def _target_conf_to_line(self, target_conf):
        line = "<target %s>\n" % target_conf["iqn"]

        for initiator_addr in target_conf["initiator_addr_list"]:
            line += "initiator-address %s\n" % initiator_addr

        for initiator_name in target_conf["initiator_name_list"]:
            line += "initiator-name %s\n" % initiator_name

        for incominguser in target_conf["incominguser_list"]:
            line += "incominguser %s\n" % incominguser.replace(":", " ")

        for outgoinguser in target_conf["outgoinguser_list"]:
            line += "outgoinguser %s\n" % outgoinguser.replace(":", " ")

        for lun_conf in target_conf["lun_list"]:
            line += self._lun_conf_to_line(lun_conf)

        line += "</target>\n"

        return line

    def _sync_to_system_conf(self, tgt_conf):
        if not os.path.exists(TGT_ETC_CONF_DIR):
            os.makedirs(TGT_ETC_CONF_DIR)

        # write the etc storlever config
        storlever_file_name = os.path.join(TGT_ETC_CONF_DIR, TGT_ETC_STORLEVER_FILE)
        with open(storlever_file_name, "w") as f:
            if tgt_conf["incomingdiscoveryuser"] != "":
                f.write("incomingdiscoveryuser %s\n" %
                        tgt_conf["incomingdiscoveryuser"].replace(":", " "))

            if tgt_conf["outgoingdiscoveryuser"] != "":
                f.write("outgoingdiscoveryuser %s\n" %
                        tgt_conf["outgoingdiscoveryuser"].replace(":", " "))
            f.write("# target list\n")
            for target_conf in tgt_conf["target_list"]:
                f.write(self._target_conf_to_line(target_conf))
            f.write("\n\n")

        # add storlever config to ntp.conf
        file_name = os.path.join(TGT_ETC_CONF_DIR, TGT_ETC_CONF_FILE)
        with open(file_name, "r") as f:
            lines = f.readlines()

        # filter some line
        lines = [line for line in lines
                 if (not line.strip().startswith("incomingdiscoveryuser")) and
                    (not line.strip().startswith("incomingdiscoveryuser"))]

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
            f.write("include %s\n" % storlever_file_name)
            f.write("# end storlever\n")
            f.writelines(after_storlever)

    def sync_to_system_conf(self):
        """sync the smb conf to /etc/samba/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        with self.lock:
            tgt_conf = self._load_conf()
            self._sync_to_system_conf(tgt_conf)

    def system_restore_cb(self):
        """sync the smb conf to /etc/samba/"""

        if not os.path.exists(self.conf_file):
            return  # if not conf file, don't change the system config

        os.remove(self.conf_file)

        with self.lock:
            tgt_conf = self._load_conf()
            self._sync_to_system_conf(tgt_conf)

    def set_tgt_conf(self, config={}, operator="unkown", **kwargs):
        if not isinstance(config, dict):
            raise StorLeverError("Parameter type error", 500)
        if len(config) == 0 and len(kwargs) == 0:
            return
        config.update(kwargs)
        not_allowed_keys = (
            "target_list",
        )
        config = filter_dict(config, not_allowed_keys, True)

        with self.lock:
            tgt_conf = self._load_conf()
            for name, value in config.items():
                if name in tgt_conf and value is not None:
                    tgt_conf[name] = value

            # check config conflict
            tgt_conf = self.tgt_conf_schema.validate(tgt_conf)

            # save new conf
            self._save_conf(tgt_conf)
            self._sync_to_system_conf(tgt_conf)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt config is updated by user(%s)" %
                   (operator))

    def get_tgt_conf(self):
        with self.lock:
            tgt_conf = self._load_conf()

        not_allowed_keys = (
            "target_list",
        )
        tgt_conf = filter_dict(tgt_conf, not_allowed_keys, True)

        # hide the password
        if tgt_conf["incomingdiscoveryuser"] != "":
            name, sep, password = tgt_conf["incomingdiscoveryuser"].partition(":")
            tgt_conf["incomingdiscoveryuser"] = name.strip() + ":" + "*"
        if tgt_conf["outgoingdiscoveryuser"] != "":
            name, sep, password = tgt_conf["outgoingdiscoveryuser"].partition(":")
            tgt_conf["outgoingdiscoveryuser"] = name.strip() + ":" + "*"

        return tgt_conf

    def get_target_iqn_list(self):
        with self.lock:
            tgt_conf = self._load_conf()
        iqn_list = []
        for target_conf in tgt_conf["target_list"]:
            iqn_list.append(target_conf["iqn"])

        return iqn_list

    def get_target_by_iqn(self, iqn):
        with self.lock:
            tgt_conf = self._load_conf()
        for target_conf in tgt_conf["target_list"]:
            if target_conf["iqn"] == iqn:
                return Target(iqn, target_conf, self)

        raise StorLeverError("tgt target (iqn:%s) Not Found" % (iqn), 404)

    def create_target(self, iqn, operator="unkown"):

        target_conf ={
            "iqn": iqn,
            "initiator_addr_list": [],
            "initiator_name_list": [],
            "incominguser_list": [],
            "outgoinguser_list": [],
        }
        target_conf = self.target_conf_schema.validate(target_conf)
        with self.lock:
            tgt_conf = self._load_conf()
            # check duplicate
            for target_conf in tgt_conf["target_list"]:
                if target_conf["iqn"] == iqn:
                    raise StorLeverError("Target (iqn:%s) Already exist" % iqn, 400)

            tgt_conf["target_list"].append(target_conf)

            # save new conf
            self._save_conf(tgt_conf)
            self._sync_to_system_conf(tgt_conf)

        try:
            check_output([TGTADMIN_CMD, "--execute"])
        except StorLeverError:
            pass

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) config is added by operator(%s)" %
                   (iqn, operator))

    def remove_target_by_iqn(self, iqn, operator="unkown"):
        with self.lock:
            tgt_conf = self._load_conf()
            delete_conf = None
            for target_conf in tgt_conf["target_list"]:
                if target_conf["iqn"] == iqn:
                    delete_conf = target_conf
            if delete_conf is None:
                raise StorLeverError("tgt target (iqn:%s) Not Found" % (iqn), 404)
            else:
                tgt_conf["target_list"].remove(delete_conf)

            # save new conf
            self._save_conf(tgt_conf)
            self._sync_to_system_conf(tgt_conf)

        try:
            check_output([TGTADMIN_CMD, "-f", "--delete", iqn])
        except StorLeverError:
            pass

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) is deleted by operator(%s)" %
                   (iqn, operator))

TgtManager = TgtManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_restore_from_file_cb(TgtManager.sync_to_system_conf)
cfg_mgr().register_system_restore_cb(TgtManager.system_restore_cb)
service_mgr().register_service("tgt", "tgtd", "tgtd", "iSCSI Target Server")
ModuleManager.register_module(**MODULE_INFO)

def tgt_mgr():
    """return the global user manager instance"""
    return TgtManager








