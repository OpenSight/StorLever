import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.nas.smbmgr import smb_mgr


class TestSmbMgr(unittest.TestCase):

    def test_smb_conf(self):
        mgr = smb_mgr()
        conf = mgr.get_smb_conf()
        self.assertTrue("server_string" in conf)
        orig_server_string = conf["server_string"]
        mgr.set_smb_conf(server_string="test samba")
        conf = mgr.get_smb_conf()
        self.assertTrue(conf["server_string"] == "test samba")
        mgr.set_smb_conf(server_string=orig_server_string)


    def test_smb_share(self):
        mgr = smb_mgr()
        try:
            mgr.get_share_conf("test_share")
            mgr.del_share_conf("test_share")
        except Exception:
            pass

        mgr.add_share_conf("test_share", "/home", "test")
        share_conf_list = mgr.get_share_conf_list()
        found = False
        for share_conf in share_conf_list:
            if share_conf["share_name"] == "test_share":
                found = True
                self.assertEquals(share_conf["path"], "/home")
                self.assertEquals(share_conf["comment"], "test")
        self.assertTrue(found)

        share_conf = mgr.get_share_conf("test_share")
        self.assertEquals(share_conf["share_name"], "test_share")
        self.assertEquals(share_conf["path"], "/home")
        self.assertEquals(share_conf["comment"], "test")

        mgr.set_share_conf("test_share", comment="test1")
        share_conf = mgr.get_share_conf("test_share")
        self.assertEquals(share_conf["comment"], "test1")

        mgr.del_share_conf("test_share")

        share_conf_list = mgr.get_share_conf_list()
        found = False
        for share_conf in share_conf_list:
            if share_conf["share_name"] == "test_share":
                found = True
        self.assertFalse(found)

    def test_smb_connection(self):
        mgr = smb_mgr()
        mgr.get_connection_list()

    def test_smb_user(self):
        mgr = smb_mgr()
        mgr.add_smb_account("root", "123456")
        smb_account_list = mgr.get_smb_account_list()
        found = False
        for smb_account in smb_account_list:
            if smb_account["username"] == "root":
                found = True
        self.assertTrue(found)

        mgr.set_smb_account_passwd("root", "123456")

        mgr.del_smb_account("root")

        smb_account_list = mgr.get_smb_account_list()
        found = False
        for smb_account in smb_account_list:
            if smb_account["username"] == "root":
                found = True
        self.assertFalse(found)










