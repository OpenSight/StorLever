"""
storlever.mngr.block.iscsi.iscsimgr
~~~~~~~~~~~~~~~~

This module implements iscsi initiator manager

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

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
from storlever.mngr.system.modulemgr import ModuleManager
from iface import Iface
from node import Node

MODULE_INFO = {
    "module_name": "iscsi_initiator",
    "rpms": [
        "iscsi-initiator-utils",
    ],
    "comment": "Provides the management functions for iscsi initiator(open-iscsi)"
}


ISCSIADM_CMD = "/sbin/iscsiadm"
ISCSI_INITIATOR_ETC_CONF_DIR = "/etc/iscsi"
ISCSI_INITIATOR_ETC_GLOBAL_FILE = "iscsid.conf"
ISCSI_INITIATOR_ETC_NAME_FILE = "initiatorname.iscsi"
ISCSI_INITIATOR_DB_PATH = "/var/lib/iscsi"



class IscsiInitiatorManager(object):

    """contains all methods to manage iscsi initiator in linux system"""
    def __init__(self):
        self.lock = lock()

    @staticmethod
    def lines_to_property_dict(lines):
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

            iface_obj = Iface(
                self, iface_name,
                params[0], params[1], params[2], params[3], params[4]
            )
            iface_list.append(iface_obj)

        return iface_list

    def get_iface_by_name(self, iface_name):
        try:
           outlines = check_output([ISCSIADM_CMD, "-m", "iface"], input_ret=[2, 7, 22]).splitlines()
        except StorLeverCmdError as e:
            if e.return_code == 21:
                outlines = []
            else:
                raise
        for line in outlines:
            entry_iface_name, sep, params = line.partition(" ")
            params = params.strip().split(",")
            if len(params) < 5:
                continue # we don't recognize this output format

            if entry_iface_name == iface_name:
                for index, value in enumerate(params):
                    if value == "<empty>":
                        params[index] = ""
                iface_obj = Iface(
                    self, entry_iface_name,
                    params[0], params[1], params[2], params[3], params[4]
                )
                return iface_obj
        else:
            raise StorLeverError("iface (%s) Not Found" % iface_name, 404)

    def create_iface(self, iface_name, operator="unkown"):
        iface_list = self.get_iface_list()
        for iface in iface_list:
            if iface.iscsi_ifacename == iface_name:
                raise StorLeverError("iface (%s) already exists" % iface_name, 400)
        check_output([ISCSIADM_CMD, "-m", "iface", "-I", iface_name, "-o", "new"],
                                input_ret=[2, 6, 7, 21, 22])

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iface (%s) is created by operator(%s)" %
                   (iface_name, operator))

    def del_iface(self, iface_name, operator="unkown"):
        if iface_name in ("default", "iser"):
            raise StorLeverError("iface (default, iser) cannot be deleted", 400)
        iface_list = self.get_iface_list()
        for iface in iface_list:
            if iface.iscsi_ifacename == iface_name:
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

            node_list.append(Node(self, target, portal))

        return node_list

    def get_node(self, target, portal):
        #check exist
        node_list = []
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
            entry_target = params[1]
            entry_portal, sep, tag = params[0].partition(",")
            if entry_portal == portal and entry_target == target:
                break;
        else:
            raise StorLeverError("Node (%s, %s) Not Found" % (target, portal), 404)

        return Node(self, target, portal)

    def create_node(self, target, portal, iface=None, operator="unkown"):

        node_list = self.get_node_list()
        for node in node_list:
            if node.target == target and node.portal == portal:
                raise StorLeverError("Node (%s, %s) already exists" % (target, portal), 400)

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

        for node in node_list:
            if node.target == target and node.portal == portal:
                break
        else:
            raise StorLeverError("Node (%s, %s) Not Found" % (target, portal), 404)

        session_list = self.get_session_list()
        for session in session_list:
            if session["portal"] == portal and session["target"] == target:
                node.logout(operator)

        check_output([ISCSIADM_CMD, "-m", "node","-o", "delete",
                      "-T", target, "-p", portal], input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) is deleted by operator(%s)" %
                   (target, portal, operator))

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
        return self.lines_to_property_dict(outlines)

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
ModuleManager.register_module(**MODULE_INFO)


def iscsi_initiator_mgr():
    """return the global block manager instance"""
    return IscsiInitiatorManager

