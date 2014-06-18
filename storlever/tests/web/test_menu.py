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


class TestMenuMgr(unittest.TestCase):


    def setUp(self):
        # register menu node
        mgr = web_menu_mgr()
        root_text = _("root text")
        mgr.add_root_node("test_root", root_text, "http://localhost:6543/")
        intermediate_text = _("intermediate text")
        mgr.add_intermediate_node("test_inter", "test_root", intermediate_text, "http://localhost:6543/")
        leaf_text = _("leaf text")
        mgr.add_leaf_node("test_leaf", "test_inter", leaf_text, "http://localhost:6543/")

    def tearDown(self):
        mgr = web_menu_mgr()
        mgr.del_node_by_id("test_leaf")
        mgr.del_node_by_id("test_inter")
        mgr.del_node_by_id("test_root")

    def test_node_del(self):
        mgr = web_menu_mgr()
        leaf2_text = _("leaf2 text")
        mgr.add_leaf_node("test_leaf2", "test_inter", leaf2_text, "http://localhost:6543/")
        leaf2_node = mgr.get_node_by_id("test_leaf2")

        mgr.del_node_by_id("test_leaf2")

        with self.assertRaises(StorLeverError):
            leaf2_node = mgr.get_node_by_id("test_leaf2")

        inter_node = mgr.get_node_by_id("test_inter")
        self.assertFalse(leaf2_node in inter_node.get_sub_nodes())


    def test_node_op(self):
        mgr = web_menu_mgr()

        # test root list
        root_list = mgr.get_root_node_list()
        for root_node in root_list:
            if root_node.node_id == "test_root":
                break
        else:
            raise Exception("No test_root node in the root node list")

        # get the menu node
        root_node = mgr.get_node_by_id("test_root")
        self.assertEquals(root_node.node_id, "test_root")
        self.assertEquals(root_node.parent_id, "")
        self.assertEquals(root_node.node_type, "root")
        self.assertEquals(root_node.text, "root text")
        self.assertEquals(root_node.uri, "http://localhost:6543/")
        sub_nodes = root_node.get_sub_nodes()
        for node in sub_nodes:
            if node.node_id == "test_inter":
                break
        else:
            raise Exception("No test_inter node in the root's sub node list")

        inter_node = mgr.get_node_by_id("test_inter")
        self.assertEquals(inter_node.node_id, "test_inter")
        self.assertEquals(inter_node.parent_id, "test_root")
        self.assertEquals(inter_node.node_type, "intermediate")
        self.assertEquals(inter_node.text, "intermediate text")
        self.assertEquals(inter_node.uri, "http://localhost:6543/")
        sub_nodes = inter_node.get_sub_nodes()
        for node in sub_nodes:
            if node.node_id == "test_leaf":
                break
        else:
            raise Exception("No test_leaf node in the inter_test's sub node list")

        leaf_text = mgr.get_node_by_id("test_leaf")
        self.assertEquals(leaf_text.node_id, "test_leaf")
        self.assertEquals(leaf_text.parent_id, "test_inter")
        self.assertEquals(leaf_text.node_type, "leaf")
        self.assertEquals(leaf_text.text, "leaf text")
        self.assertEquals(leaf_text.uri, "http://localhost:6543/")
        sub_nodes = leaf_text.get_sub_nodes()
        self.assertFalse(sub_nodes)

    def test_node_dict(self):
        mgr = web_menu_mgr()
        root_node = mgr.get_node_by_id("test_root")
        root_dict = root_node.to_dict()
        self.assertEquals(root_dict["node_id"], "test_root")
        self.assertEquals(root_dict["parent_id"], "")
        self.assertEquals(root_dict["node_type"], "root")
        self.assertEquals(root_dict["text"], "root text")
        self.assertEquals(root_dict["uri"], "http://localhost:6543/")
        inter_dict = root_dict["sub_nodes"][0]
        self.assertEquals(inter_dict["node_id"], "test_inter")
        self.assertEquals(inter_dict["parent_id"], "test_root")
        self.assertEquals(inter_dict["node_type"], "intermediate")
        self.assertEquals(inter_dict["text"], "intermediate text")
        self.assertEquals(inter_dict["uri"], "http://localhost:6543/")
        leaf_dict = inter_dict["sub_nodes"][0]
        self.assertEquals(leaf_dict["node_id"], "test_leaf")
        self.assertEquals(leaf_dict["parent_id"], "test_inter")
        self.assertEquals(leaf_dict["node_type"], "leaf")
        self.assertEquals(leaf_dict["text"], "leaf text")
        self.assertEquals(leaf_dict["uri"], "http://localhost:6543/")
        self.assertFalse(leaf_dict["sub_nodes"])







