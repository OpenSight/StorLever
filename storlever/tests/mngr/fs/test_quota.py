import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.fs.fsmgr import fs_mgr
from storlever.mngr.fs import ext4
from utils import get_block_dev




class TestFsQuota(unittest.TestCase):

    def setUp(self):
        mgr = fs_mgr()
        dev_file = get_block_dev()
        mgr.mkfs_on_dev("ext4", get_block_dev())
        mgr.add_fs("test_quota", "ext4", dev_file, "usrquota,grpquota", comment="test")


    def tearDown(self):
        mgr = fs_mgr()
        mgr.del_fs("test_quota")


    def test_quota_operation(self):
        mgr = fs_mgr()
        f = mgr.get_fs_by_name("test_quota")

        f.quota_check()
        ureport = f.quota_user_report()
        found = False
        for uquota in ureport:
            if uquota["name"] == "root":
                found = True
                self.assertEquals(uquota["block_softlimit"], 0)
                self.assertEquals(uquota["block_hardlimit"], 0)
                self.assertEquals(uquota["inode_softlimit"], 0)
                self.assertEquals(uquota["inode_hardlimit"], 0)
        self.assertTrue(found)


        greport = f.quota_group_report()
        found = False
        for gquota in greport:
            if gquota["name"] == "root":
                found = True
                self.assertEquals(gquota["block_softlimit"], 0)
                self.assertEquals(gquota["block_hardlimit"], 0)
                self.assertEquals(gquota["inode_softlimit"], 0)
                self.assertEquals(gquota["inode_hardlimit"], 0)
        self.assertTrue(found)

        f.quota_user_set("root", 1000, 1500, 2000, 2500)
        f.quota_group_set("root", 3000, 3500, 4000, 4500)


        f.quota_check()
        ureport = f.quota_user_report()
        found = False
        for uquota in ureport:
            if uquota["name"] == "root":
                found = True
                self.assertEquals(uquota["block_softlimit"], 1000)
                self.assertEquals(uquota["block_hardlimit"], 1500)
                self.assertEquals(uquota["inode_softlimit"], 2000)
                self.assertEquals(uquota["inode_hardlimit"], 2500)
        self.assertTrue(found)

        greport = f.quota_group_report()
        found = False
        for gquota in greport:
            if gquota["name"] == "root":
                found = True
                self.assertEquals(gquota["block_softlimit"], 3000)
                self.assertEquals(gquota["block_hardlimit"], 3500)
                self.assertEquals(gquota["inode_softlimit"], 4000)
                self.assertEquals(gquota["inode_hardlimit"], 4500)
        self.assertTrue(found)








