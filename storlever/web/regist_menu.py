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
    regist_store(mgr)

def regist_system(mgr):
    root_text = _("System")
    mgr.add_root_node("ROOT_NODE_System", root_text, "")
    inter_text = _("System")
    mgr.add_intermediate_node("INTER_NODE_System", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("System Infomation")
    mgr.add_leaf_node("system-info", "INTER_NODE_System", leaf_text, "partials/system-info")
    leaf_text = _("System Statistics")
    mgr.add_leaf_node("statistics", "INTER_NODE_System", leaf_text, "partials/statistics")
    leaf_text = _("Service Information")
    mgr.add_leaf_node("service", "INTER_NODE_System", leaf_text, "partials/service")
    leaf_text = _("User Management")
    mgr.add_leaf_node("user", "INTER_NODE_System", leaf_text, "partials/user")
    leaf_text = _("Module Management")
    mgr.add_leaf_node("module", "INTER_NODE_System", leaf_text, "partials/module")

    inter_text = _("Network")
    mgr.add_intermediate_node("INTER_NODE_Network", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("Interface Management")
    mgr.add_leaf_node("interface", "INTER_NODE_Network", leaf_text, "partials/interface")
    leaf_text = _("Bond Management")
    mgr.add_leaf_node("bond", "INTER_NODE_Network", leaf_text, "partials/bond")
    leaf_text = _("Network Settings")
    mgr.add_leaf_node("net-settings", "INTER_NODE_Network", leaf_text, "partials/net")

    inter_text = _("Tools")
    mgr.add_intermediate_node("INTER_NODE_Tools", "ROOT_NODE_System", inter_text, "")
    leaf_text = _("NTP")
    mgr.add_leaf_node("NTP", "INTER_NODE_Tools", leaf_text, "partials/ntp")
    leaf_text = _("SNMP")
    mgr.add_leaf_node("SNMP", "INTER_NODE_Tools", leaf_text, "partials/snmp")
    leaf_text = _("Zabbix")
    mgr.add_leaf_node("Zabbix", "INTER_NODE_Tools", leaf_text, "partials/zabbix")
    

def regist_store(mgr):
    root_text = _("Store")
    mgr.add_root_node("ROOT_NODE_Store", root_text, "")
    inter_text = _("Store")
    mgr.add_intermediate_node("INTER_NODE_Store", "ROOT_NODE_Store", inter_text, "")
    leaf_text = _("Store")
    mgr.add_leaf_node("store", "INTER_NODE_Store", leaf_text, "partials/store")
    