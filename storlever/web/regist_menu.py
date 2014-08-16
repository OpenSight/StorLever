"""
storlever.web.menu
~~~~~~~~~~~~~~~~

This module implements web menu system

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""
import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.lib.exception import StorLeverError
from storlever.web.menu import web_menu_mgr
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('storlever')

def includeme(config):
    mgr = web_menu_mgr()
    regist_system(mgr)

def regist_system(mgr):
    root_text = _("System")
    mgr.add_root_node("ROOT_NODE_System", root_text, "")
    inter_text = _("System")
    mgr.add_intermediate_node("INTER_NODE_System", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("System Infomation")
    mgr.add_leaf_node("LEAF_NODE_SystemInfo", "INTER_NODE_System", leaf_text, "")
    leaf_text = _("System Statistics")
    mgr.add_leaf_node("LEAF_NODE_Statistics", "INTER_NODE_System", leaf_text, "")
    leaf_text = _("Service Information")
    mgr.add_leaf_node("LEAF_NODE_ServiceInfo", "INTER_NODE_System", leaf_text, "")
    leaf_text = _("User Management")
    mgr.add_leaf_node("LEAF_NODE_UserManagement", "INTER_NODE_System", leaf_text, "")
    leaf_text = _("Module Management")
    mgr.add_leaf_node("LEAF_NODE_ModuleManagement", "INTER_NODE_System", leaf_text, "")

    inter_text = _("Network")
    mgr.add_intermediate_node("INTER_NODE_Network", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("Interface Management")
    mgr.add_leaf_node("LEAF_NODE_InterfaceManagement", "INTER_NODE_Network", leaf_text, "")
    leaf_text = _("Bond Management")
    mgr.add_leaf_node("LEAF_NODE_BondManagement", "INTER_NODE_Network", leaf_text, "")
    leaf_text = _("Network Settings")
    mgr.add_leaf_node("LEAF_NODE_NetworkSettings", "INTER_NODE_Network", leaf_text, "")

    inter_text = _("Tools")
    mgr.add_intermediate_node("INTER_NODE_Tools", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("NTP")
    mgr.add_leaf_node("LEAF_NODE_NTP", "INTER_NODE_Tools", leaf_text, "")
    leaf_text = _("SNMP")
    mgr.add_leaf_node("LEAF_NODE_SNMP", "INTER_NODE_Tools", leaf_text, "")
    leaf_text = _("Zabbix")
    mgr.add_leaf_node("LEAF_NODE_Zabbix", "INTER_NODE_Tools", leaf_text, "")
    