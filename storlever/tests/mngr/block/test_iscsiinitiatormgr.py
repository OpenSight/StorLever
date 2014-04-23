import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.iscsi.initiatormgr import iscsi_initiator_mgr

test_login_node = ""


def get_test_node():
    global test_login_node
    if test_login_node is None or test_login_node == "":
        test_login_node = raw_input("Please input a node(format: IQN Portal) for login test(empty means no test):")

    return test_login_node


class TestIscsiInitiatorMgr(unittest.TestCase):

    def test_global_conf(self):
        mgr = iscsi_initiator_mgr()
        conf = mgr.get_global_conf()
        ori_startup = conf.get("node.startup")
        mgr.update_global_conf({"node.startup": "manual"})
        startup = mgr.get_global_conf()["node.startup"]
        self.assertEquals(startup, "manual")
        mgr.del_global_conf_entry(["node.startup"])
        self.assertFalse("node.startup" in mgr.get_global_conf())
        if ori_startup is not None:
            mgr.update_global_conf({"node.startup": ori_startup})

    def test_initiator_iqn(self):
        mgr = iscsi_initiator_mgr()
        org_iqn = mgr.get_initiator_iqn()
        mgr.set_initiator_iqn("iqn.2014-01.cn.com.opensight:test")
        self.assertEquals(mgr.get_initiator_iqn(), "iqn.2014-01.cn.com.opensight:test")
        mgr.set_initiator_iqn(org_iqn)

    def test_session(self):
        mgr = iscsi_initiator_mgr()
        mgr.get_session_list()

    def test_iface(self):
        mgr = iscsi_initiator_mgr()
        try:
            mgr.get_iface_conf("test_tcp")
            mgr.del_iface("test_tcp")
        except Exception:
            pass

        mgr.create_iface("test_tcp")
        iface_list = mgr.get_iface_list()
        found = False
        for iface_entry in iface_list:
            if iface_entry["iface_name"] == "test_tcp":
                found = True
                self.assertEquals(iface_entry["net_ifacename"], "")
                self.assertEquals(iface_entry["transport_name"], "tcp")
        self.assertTrue(found)

        iface_conf = mgr.get_iface_conf("test_tcp")
        self.assertEquals(iface_conf["iface.transport_name"], "tcp")
        self.assertEquals(iface_conf["iface.net_ifacename"], "")
        self.assertEquals(iface_conf["iface.iscsi_ifacename"], "test_tcp")

        mgr.update_iface_conf("test_tcp", "iface.net_ifacename", "eth0")
        iface_conf = mgr.get_iface_conf("test_tcp")
        self.assertEquals(iface_conf["iface.net_ifacename"], "eth0")
        iface_list = mgr.get_iface_list()
        found = False
        for iface_entry in iface_list:
            if iface_entry["iface_name"] == "test_tcp":
                found = True
                self.assertEquals(iface_entry["net_ifacename"], "eth0")
        self.assertTrue(found)

        mgr.del_iface("test_tcp")
        iface_list = mgr.get_iface_list()
        found = False
        for iface_entry in iface_list:
            if iface_entry["iface_name"] == "test_tcp":
                found = True
        self.assertFalse(found)

    def test_node(self):
        mgr = iscsi_initiator_mgr()
        try:
            mgr.get_node_conf("iqn.2014-01.cn.com.opensight:test_node", "192.168.1.10:3260")
            mgr.delete_node("iqn.2014-01.cn.com.opensight:test_node", "192.168.1.10:3260")
        except Exception:
            pass

        mgr.create_node("iqn.2014-01.cn.com.opensight:test_node", "192.168.1.10:3260")
        node_list = mgr.get_node_list()
        found = False
        for node_entry in node_list:
            if node_entry["target"] == "iqn.2014-01.cn.com.opensight:test_node" \
                and node_entry["portal"] == "192.168.1.10:3260":
                found = True
        self.assertTrue(found)

        node_conf = mgr.get_node_conf("iqn.2014-01.cn.com.opensight:test_node",
                                      "192.168.1.10:3260")
        self.assertEquals(node_conf["node.name"], "iqn.2014-01.cn.com.opensight:test_node")
        self.assertEquals(node_conf["node.conn[0].address"], "192.168.1.10")
        self.assertEquals(node_conf["node.conn[0].port"], "3260")


        mgr.update_node_conf("iqn.2014-01.cn.com.opensight:test_node",
                              "192.168.1.10:3260",
                              "node.startup", "automatic")
        node_conf = mgr.get_node_conf("iqn.2014-01.cn.com.opensight:test_node",
                                      "192.168.1.10:3260")
        self.assertEquals(node_conf["node.startup"], "automatic")
        mgr.update_node_conf("iqn.2014-01.cn.com.opensight:test_node",
                              "192.168.1.10:3260",
                              "node.startup", "manual")
        node_conf = mgr.get_node_conf("iqn.2014-01.cn.com.opensight:test_node",
                                      "192.168.1.10:3260")
        self.assertEquals(node_conf["node.startup"], "manual")


        mgr.delete_node("iqn.2014-01.cn.com.opensight:test_node",
                        "192.168.1.10:3260")
        found = False
        node_list = mgr.get_node_list()
        for node_entry in node_list:
            if node_entry["target"] == "iqn.2014-01.cn.com.opensight:test_node" \
                and node_entry["portal"] == "192.168.1.10:3260":
                found = True
        self.assertFalse(found)

    def test_login(self):
        mgr = iscsi_initiator_mgr()
        test_node_portal = get_test_node()
        if test_node_portal == "":
            return
        test_target, sep, test_portal = test_node_portal.partition(" ")
        node_list = mgr.discovery(test_portal)
        found = False
        for node_entry in node_list:
            if node_entry["target"] == test_target \
                and node_entry["portal"] == test_portal:
                found = True
        self.assertTrue(found)

        node_list = mgr.get_node_list()
        found = False
        for node_entry in node_list:
            if node_entry["target"] == test_target \
                and node_entry["portal"] == test_portal:
                found = True
                self.assertFalse(node_entry["login"])
        self.assertTrue(found)

        mgr.login_node(test_target, test_portal)
        session_list = mgr.get_session_list()
        found = False
        for session_entry in session_list:
            if session_entry["target"] == test_target \
                and session_entry["portal"] == test_portal:
                found = True
                session_id = session_entry["session_id"]
        self.assertTrue(found)

        session_conf = mgr.get_session_conf(session_id)
        self.assertEquals(session_conf["node.name"], test_target)

        mgr.logout_node(test_target, test_portal)
        session_list = mgr.get_session_list()
        found = False
        for session_entry in session_list:
            if session_entry["target"] == test_target \
               and session_entry["portal"] == test_portal:
                found = True
        self.assertFalse(found)

        mgr.delete_node(test_target, test_portal)


















