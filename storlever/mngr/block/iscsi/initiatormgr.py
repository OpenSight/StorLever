"""
storlever.mngr.block.iscsi.iscsimgr
~~~~~~~~~~~~~~~~

This module implements iscsi initiator manager

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""

import os
import os.path
import shutil

from storlever.lib.command import check_output, write_file_entry, read_file_entry
from storlever.lib.exception import StorLeverError, StorLeverCmdError
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR, cfg_mgr
from storlever.mngr.system.servicemgr import service_mgr
from storlever.lib.confparse import properties
from storlever.lib.lock import lock
from storlever.lib import logger
import logging

import subprocess

ISCSIADM_CMD = "/sbin/iscsiadm"
ISCSI_INITIATOR_ETC_CONF_DIR = "/etc/iscsi"
ISCSI_INITIATOR_ETC_GLOBAL_FILE = "iscsid.conf"
ISCSI_INITIATOR_ETC_NAME_FILE = "initiatorname.iscsi"
ISCSI_INITIATOR_DB_PATH = "/var/lib/iscsi"

class IscsiInitiatorManager(object):

    """contains all methods to manage iscsi initiator in linux system"""
    def __init__(self):
        self.lock = lock()

    def _lines_to_property_dict(self, lines):
        property_dict = {}
        for line in lines:
            if line.strip().startswith("#"):
                continue
            key, sep, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if value == "<empty>":
                value = ""
            property_dict[key] = value
        return property_dict

    # global property
    def get_initiator_iqn(self):
        with self.lock:
            if not os.path.exists(ISCSI_INITIATOR_ETC_CONF_DIR):
                os.makedirs(ISCSI_INITIATOR_ETC_CONF_DIR)
            name_file = os.path.join(ISCSI_INITIATOR_ETC_CONF_DIR, ISCSI_INITIATOR_ETC_NAME_FILE)
            if os.path.exists(name_file):
                conf = properties(name_file)
            else:
                conf = properties()

        return conf.get("InitiatorName", "iqn.2014-01.cn.com.opensight:default")

    def set_initiator_iqn(self, iqn, operator="unkown"):
        with self.lock:
            if not os.path.exists(ISCSI_INITIATOR_ETC_CONF_DIR):
                os.makedirs(ISCSI_INITIATOR_ETC_CONF_DIR)
            name_file = os.path.join(ISCSI_INITIATOR_ETC_CONF_DIR, ISCSI_INITIATOR_ETC_NAME_FILE)
            conf = properties(InitiatorName=iqn)
            conf.set_sep(True)
            conf.apply_to(name_file)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iqn is updated to %s by operator(%s)" %
                   (iqn, operator))

    def get_global_conf(self):
        with self.lock:
            if not os.path.exists(ISCSI_INITIATOR_ETC_CONF_DIR):
                os.makedirs(ISCSI_INITIATOR_ETC_CONF_DIR)
            conf_file = os.path.join(ISCSI_INITIATOR_ETC_CONF_DIR, ISCSI_INITIATOR_ETC_GLOBAL_FILE)
            if os.path.exists(conf_file):
                conf = properties(conf_file)
            else:
                conf = properties()
        return dict(conf)

    def update_global_conf(self, new_conf={}, operator="unkown"):
        """update the global conf dict with the given conf

        if the entry does not exists in the conf, it would be created
        """
        conf = properties(new_conf)
        conf.set_sep(True)
        with self.lock:
            if not os.path.exists(ISCSI_INITIATOR_ETC_CONF_DIR):
                os.makedirs(ISCSI_INITIATOR_ETC_CONF_DIR)
            conf_file = os.path.join(ISCSI_INITIATOR_ETC_CONF_DIR, ISCSI_INITIATOR_ETC_GLOBAL_FILE)
            conf.apply_to(conf_file)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator global conf is updated by operator(%s)" %
                   (operator))

    def del_global_conf_entry(self, keys=[], operator="unkown"):
        conf = properties()
        conf.set_sep(True)
        if isinstance(keys, list):
            for key in keys:
                conf.delete(key)
        else:
            conf.delete(keys)

        with self.lock:
            if not os.path.exists(ISCSI_INITIATOR_ETC_CONF_DIR):
                os.makedirs(ISCSI_INITIATOR_ETC_CONF_DIR)
            conf_file = os.path.join(ISCSI_INITIATOR_ETC_CONF_DIR, ISCSI_INITIATOR_ETC_GLOBAL_FILE)
            conf.apply_to(conf_file)

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator global conf is updated by operator(%s)" %
                   (operator))


    # iface property
    def get_iface_list(self):
        iface_list = []
        try:
           outlines = check_output([ISCSIADM_CMD, "-m", "iface"], input_ret=[2, 7, 22]).splitlines()
        except StorLeverCmdError as e:
            if e.return_code == 21:
                outlines = []
            else:
                raise
        for line in outlines:
            iface_name, sep, params = line.partition(" ")
            params = params.strip().split(",")
            if len(params) < 5:
                continue # we don't recognize this output format
            for index, value in enumerate(params):
                if value == "<empty>":
                    params[index] = ""

            iface_list.append({
                "iface_name": iface_name,
                "transport_name": params[0],
                "hwaddress": params[1],
                "ipaddress": params[2],
                "net_ifacename": params[3],
                "initiatorname": params[4],
            })
        return iface_list

    def get_iface_conf(self, iface_name):
        outlines = check_output([ISCSIADM_CMD, "-m", "iface", "-I", iface_name],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        return self._lines_to_property_dict(outlines)

    def create_iface(self, iface_name, operator="unkown"):
        iface_list = self.get_iface_list()
        for iface in iface_list:
            if iface["iface_name"] == iface_name:
                raise StorLeverError("iface (%s) already exists" % iface_name, 400)
        check_output([ISCSIADM_CMD, "-m", "iface", "-I", iface_name, "-o", "new"],
                                input_ret=[2, 6, 7, 21, 22])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iface (%s) is created by operator(%s)" %
                   (iface_name, operator))

    def update_iface_conf(self, iface_name, name, value, operator="unkown"):
        check_output([ISCSIADM_CMD, "-m", "iface", "-I", iface_name, "-o", "update",
                      "-n", str(name), "-v", str(value)], input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iface (%s) conf (%s:%s) is updated by operator(%s)" %
                   (iface_name, name, value, operator))


    def del_iface(self, iface_name, operator="unkown"):
        if iface_name in ("default", "iser"):
            raise StorLeverError("iface (default, iser) cannot be deleted", 400)
        iface_list = self.get_iface_list()
        for iface in iface_list:
            if iface["iface_name"] == iface_name:
                break;
        else:
            raise StorLeverError("iface (%s) Not Found" % iface_name, 404)


        check_output([ISCSIADM_CMD, "-m", "iface", "-I", iface_name, "-o", "delete"],
                                input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iface (%s) is deleted by operator(%s)" %
                   (iface_name, operator))

    # node property
    def get_node_list(self):
        node_list = []
        session_list = self.get_session_list()
        try:
           outlines = check_output([ISCSIADM_CMD, "-m", "node"], input_ret=[2, 7, 22]).splitlines()
        except StorLeverCmdError as e:
            if e.return_code == 21:
                outlines = []
            else:
                raise
        for line in outlines:
            params = line.split()
            if len(params) < 2:
                continue # we don't recognize this output format
            target = params[1]
            portal, sep, tag = params[0].partition(",")

            login = False
            for session in session_list:
                if session["target"] == target \
                    and session["portal"] == portal:
                    login = True
            node_list.append({
                "target": target,
                "portal": portal,
                "login": login,
            })

        return node_list

    def create_node(self, target, portal, iface=None, operator="unkown"):
        cmd = [ISCSIADM_CMD, "-m", "node", "-o", "new", "-T", target, "-p", portal]
        if iface is not None:
            cmd.append("-I")
            cmd.append(iface)

        check_output(cmd, input_ret=[2, 6, 7, 21, 22])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) is created by operator(%s)" %
                   (target, portal, operator))

    def delete_node(self, target, portal, operator="unkown"):
        node_list = self.get_node_list()

        login = False
        for node in node_list:
            if node["target"] == target and node["portal"] == portal:
                login = node["login"]
                break
        else:
            raise StorLeverError("Node (%s, %s) Not Found" % (target, portal), 404)

        if login:
            self.logout_node(target, portal, operator)

        check_output([ISCSIADM_CMD, "-m", "node","-o", "delete",
                      "-T", target, "-p", portal], input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) is deleted by operator(%s)" %
                   (target, portal, operator))

    def get_node_conf(self, target, portal):
        outlines = check_output([ISCSIADM_CMD, "-m", "node",
                                 "-T", target, "-p", portal],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        return self._lines_to_property_dict(outlines)

    def update_node_conf(self, target, portal, name, value, operator="unkown"):
        check_output([ISCSIADM_CMD, "-m", "node", "-T", target, "-p", portal,
                      "-o", "update", "-n", str(name), "-v", str(value)], input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) conf (%s:%s) is updated by operator(%s)" %
                   (target, portal, name, value, operator))

    def login_node(self, target, portal=None, operator="unkown"):
        cmd = [ISCSIADM_CMD, "-m", "node","--login", "-T", target]
        if portal is not None:
            cmd.append("-p")
            cmd.append(portal)

        outlines = check_output(cmd, input_ret=[2, 6, 7, 21, 22]).splitlines()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s) is login by operator(%s)" %
                   (target, operator))

    def logout_node(self, target, portal=None, operator="unkown"):
        cmd = [ISCSIADM_CMD, "-m", "node","--logout", "-T", target]
        if portal is not None:
            cmd.append("-p")
            cmd.append(portal)

        outlines = check_output(cmd, input_ret=[2, 6, 7, 21, 22]).splitlines()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s) is logout by operator(%s)" %
                   (target, operator))

    # session property
    def get_session_list(self):
        session_list = []
        try:
           outlines = check_output([ISCSIADM_CMD, "-m", "session"], input_ret=[2, 7, 22]).splitlines()
        except StorLeverCmdError as e:
            if e.return_code == 21:
                outlines = []
            else:
                raise
        for line in outlines:
            transport, sep, info = line.partition(":")
            transport = transport.strip()
            info_list = info.split()
            target = info_list[2]
            portal, sep, tag = info_list[1].partition(",")
            session_id = info_list[0].strip("[] ")
            session_list.append({
                "session_id": int(session_id),
                "transport_name": transport,
                "portal": portal,
                "target": target
            })
        return session_list


    def get_session_conf(self, session_id):

        outlines = check_output([ISCSIADM_CMD, "-m", "session", "-r", str(session_id)],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        return self._lines_to_property_dict(outlines)

    def get_session_stat(self, session_id):
        stat = {}
        outlines = check_output([ISCSIADM_CMD, "-m", "session", "-s", "-r", str(session_id)],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        for line in outlines[1:]:
            if line.count(":") != 1:
                continue
            key, sep, value = line.partition(":")
            if value.strip() == "":
                continue
            stat[key.strip()] = value.strip()

        return stat

    def logout_session(self, session_id, operator="unkown"):
        outlines = check_output([ISCSIADM_CMD, "-m", "session", "-u", "-r", str(session_id)],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator session (%s) is logout by operator(%s)" %
                   (str(session_id), operator))

    # discovery
    def discovery(self, portal, iface_name=None):
        # delete the config for this dicovery
        try:
            check_output([ISCSIADM_CMD, "-m", "discoverydb", "-t", "st",
                          "-p", portal, "-o", "delete"])
        except StorLeverError:
            pass

        # discovery process
        cmd = [ISCSIADM_CMD, "-m", "discovery", "-t", "st", "-p", portal]
        if iface_name is not None:
            cmd.append("-I")
            cmd.append(iface_name)

        outlines = check_output(cmd, input_ret=[2, 6, 7, 21, 22]).splitlines()

        result = []
        for line in outlines:
            line_list = line.split()
            target = line_list[1]
            portal, sep, tag = line_list[0].partition(",")
            result.append({
                "portal": portal,
                "target": target
            })

        return result

    def system_restore_cb(self):
        check_output("rm -rf " + os.path.join(ISCSI_INITIATOR_DB_PATH, "nodes/*"), True)
        check_output("rm -rf " + os.path.join(ISCSI_INITIATOR_DB_PATH, "ifaces/*"), True)


IscsiInitiatorManager = IscsiInitiatorManager()

# register ftp manager callback functions to basic manager
cfg_mgr().register_system_restore_cb(IscsiInitiatorManager.system_restore_cb)
cfg_mgr().register_config_file(os.path.join(ISCSI_INITIATOR_DB_PATH, "ifaces/"))
cfg_mgr().register_config_file(os.path.join(ISCSI_INITIATOR_DB_PATH, "nodes/"))
service_mgr().register_service("iscsid", "iscsid", "iscsid", "iSCSI Initiator daemon")
service_mgr().register_service("iscsi", "iscsi", "", "iSCSI Initiator login Script")



def iscsi_initiator_mgr():
    """return the global block manager instance"""
    return IscsiInitiatorManager

