import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.system.usermgr import user_mgr


class TestUserMgr(unittest.TestCase):

    def test_user_list(self):
        manager = user_mgr()
        user_list = manager.user_list()
        self.assertEquals("root", user_list[0]["name"])
        self.assertEquals("root", user_list[0]["primary_group"])
        self.assertEquals(0, user_list[0]["uid"])

        root_user = manager.get_user_info_by_name("root")
        self.assertEquals("root", root_user["name"])
        self.assertEquals("root", root_user["primary_group"])
        self.assertEquals(0, root_user["uid"])

    def test_group_list(self):
        manager = user_mgr()
        group_list = manager.group_list()
        self.assertEquals("root", group_list[0]["name"])
        self.assertEquals(0, group_list[0]["gid"])

        root_group = manager.get_group_by_name("root")
        self.assertEquals("root", root_group["name"])
        self.assertEquals(0, root_group["gid"])

    def test_user_add_del(self):
        manager = user_mgr()
        manager.user_add("storlever_test", groups="root", home_dir="/home")
        user = manager.get_user_info_by_name("storlever_test")
        self.assertEquals("storlever_test", user["name"])
        self.assertEquals("root", user["groups"])
        manager.user_mod("storlever_test", groups="")
        user = manager.get_user_info_by_name("storlever_test")
        self.assertEquals("", user["groups"])
        manager.user_del_by_name("storlever_test")

    def test_group_add_del(self):
        manager = user_mgr()
        manager.group_add("storlever_test")
        group = manager.get_group_by_name("storlever_test")
        self.assertEquals("storlever_test", group["name"])
        manager.group_del_by_name("storlever_test")


