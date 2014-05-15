"""
storlever.mngr.san.tgt.target
~~~~~~~~~~~~~~~~

This module implements tgt target class.


:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.lib import logger
from storlever.lib.utils import filter_dict
import logging
from tgtadmparse import TgtStatus
from tgtmgr import TGTADMIN_CMD


class Target(object):
    """contains all methods to tgt iscsi target manage"""

    def __init__(self, iqn, conf, mgr):
        self.iqn = iqn
        self.conf = conf
        self.mgr = mgr

    def _update_target(self):
        try:
            check_output([TGTADMIN_CMD, "-f", "--update", self.iqn])
        except StorLeverError:
            pass

    # initiator_addr_list
    def get_initiator_addr_list(self):
        return self.conf["initiator_addr_list"]

    def set_initiator_addr_list(self, initiator_addr_list=[], operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            conf["initiator_addr_list"] = initiator_addr_list
            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) initiator_addr_list is updated by operator(%s)" %
                   (self.iqn, operator))

    # initiator_name_list
    def get_initiator_name_list(self):
        return self.conf["initiator_name_list"]

    def set_initiator_name_list(self, initiator_name_list=[], operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            conf["initiator_name_list"] = initiator_name_list
            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) initiator_name_list is updated by operator(%s)" %
                   (self.iqn, operator))

    # incominguser_list
    def get_incominguser_list(self):
        user_list = []
        for user in self.conf["incominguser_list"]:
            name, sep, password = user.partition(":")
            user_list.append( name.strip())
        return user_list

    def set_incominguser(self, name, passwd, operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = False
            for index, user in enumerate(conf["incominguser_list"]):
                user_name, sep, password = user.partition(":")
                if user_name == name:
                    conf["incominguser_list"][index] = name.strip() + ":" + passwd.strip()
                    found = True

            if not found:
                conf["incominguser_list"].append(name.strip() + ":" + passwd.strip())

            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) incominguser (%s) is set by operator(%s)" %
                   (self.iqn, name, operator))

    def del_incominguser(self, name, operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = None
            for user in conf["incominguser_list"]:
                user_name, sep, password = user.partition(":")
                if user_name == name:
                    found = user

            if found is None:
                raise StorLeverError("tgt target (iqn:%s) incominguser (%s) Not Found" %
                                     (self.iqn, name), 404)
            else:
                conf["incominguser_list"].remove(found)

            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) incominguser (%s) is deleted by operator(%s)" %
                   (self.iqn, name, operator))

    # incominguser_list
    def get_outgoinguser_list(self):
        user_list = []
        for user in self.conf["outgoinguser_list"]:
            name, sep, password = user.partition(":")
            user_list.append( name.strip())
        return user_list

    def set_outgoinguser(self, name, passwd, operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = False
            for index, user in enumerate(conf["outgoinguser_list"]):
                user_name, sep, password = user.partition(":")
                if user_name == name:
                    conf["outgoinguser_list"][index] = name.strip() + ":" + passwd.strip()
                    found = True

            if not found:
                conf["outgoinguser_list"].append(name.strip() + ":" + passwd.strip())

            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) outgoinguser (%s) is set by operator(%s)" %
                   (self.iqn, name, operator))

    def del_outgoinguser(self, name, operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = None
            for user in conf["outgoinguser_list"]:
                user_name, sep, password = user.partition(":")
                if user_name == name:
                    found = user

            if found is None:
                raise StorLeverError("tgt target (iqn:%s) outgoinguser (%s) Not Found" %
                                     (self.iqn, name), 404)
            else:
                conf["outgoinguser_list"].remove(found)

            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf
        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) outgoinguser (%s) is deleted by operator(%s)" %
                   (self.iqn, name, operator))

    # lun operation
    def get_lun_list(self):
        return self.conf["lun_list"]

    def get_lun_by_num(self, lun_num):
        for lun in self.conf["lun_list"]:
            if lun["lun"] == lun_num:
                return lun

        raise StorLeverError("Target (iqn:%s) Lun (%d)Not Found" % (self.iqn, lun_num),
                             404)

    def add_lun(self, lun, path, device_type="disk", bs_type="rdwr", direct_map=False,
                write_cache=True, readonly=False, online=True, scsi_id="",
                scsi_sn="", operator="unkown"):

        if path != "" and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)
        lun_conf = {
            "lun": lun,
            "path": path,
            "device_type": device_type,
            "bs_type": bs_type,
            "direct_map": direct_map,
            "write_cache": write_cache,
            "readonly": readonly,
            "online": online,
            "scsi_id": scsi_id,
            "scsi_sn": scsi_sn
        }
        lun_conf = self.mgr.lun_conf_schema.validate(lun_conf)

        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = None
            for l in conf["lun_list"]:
                if l["lun"] == lun:
                    found = l

            if found is not None:
                raise StorLeverError("tgt target (iqn:%s) Lun (%d) already exists" %
                                     (self.iqn, lun), 400)
            else:
                conf["lun_list"].append(lun_conf)

            self.mgr._set_target_conf(self.iqn, conf)

            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) Lun (%d) is added by operator(%s)" %
                   (self.iqn, lun, operator))



    def set_lun(self, lun, path=None, device_type=None, bs_type=None, direct_map=None,
                write_cache=None, readonly=None, online=None, scsi_id=None,
                scsi_sn=None, operator="unkown"):

        if path != None and not os.path.exists(path):
             raise StorLeverError("path(%s) does not exists" % (path), 400)

        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = None
            for l in conf["lun_list"]:
                if l["lun"] == lun:
                    found = l

            if found is None:
                raise StorLeverError("tgt target (iqn:%s) Lun (%d) Not Found" %
                                     (self.iqn, lun), 404)
            if path is not None:
                found["path"] = path
            if device_type is not None:
                found["device_type"] = device_type
            if bs_type is not None:
                found["bs_type"] = bs_type
            if direct_map is not None:
                found["direct_map"] = direct_map
            if write_cache is not None:
                found["write_cache"] = write_cache
            if readonly is not None:
                found["readonly"] = readonly
            if online is not None:
                found["online"] = online
            if scsi_id is not None:
                found["scsi_id"] = scsi_id
            if scsi_sn is not None:
                found["scsi_sn"] = scsi_sn

            self.mgr._set_target_conf(self.iqn, conf)
            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) Lun (%d) is updated by operator(%s)" %
                   (self.iqn, lun, operator))

    def del_lun(self, lun, operator="unkown"):
        with self.mgr.lock:
            conf = self.mgr._get_target_conf(self.iqn)
            found = None
            for l in conf["lun_list"]:
                if l["lun"] == lun:
                    found = l

            if found is None:
                raise StorLeverError("tgt target (iqn:%s) Lun (%d) Not Found" %
                                     (self.iqn, lun), 404)
            else:
                conf["lun_list"].remove(found)

            self.mgr._set_target_conf(self.iqn, conf)
            self.conf = conf # update the cache target conf

        self._update_target()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "tgt target (iqn:%s) Lun (%d) is deleted by operator(%s)" %
                   (self.iqn, lun, operator))

    # target operation
    def get_state(self):
        return TgtStatus.get_target_state(self.iqn)

    def set_state(self, state, operator="unkown"):
        if state == "offline":
            check_output([TGTADMIN_CMD, "--offline", self.iqn])
        elif state == "ready":
            check_output([TGTADMIN_CMD, "--ready", self.iqn])
        else:
            raise StorLeverError("state (%s) is  not supported" %
                                     (state), 400)

    def get_session_list(self):
        return TgtStatus.get_target_sessions(self.iqn)

