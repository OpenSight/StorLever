import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.fs.fsmgr import fs_mgr
from storlever.mngr.fs import ext4
from utils import get_block_dev




class TestFsDir(unittest.TestCase):

    def setUp(self):
        mgr = fs_mgr()
        dev_file = get_block_dev()
        mgr.mkfs_on_dev("ext4", get_block_dev())
        mgr.add_fs("test_dir", "ext4", dev_file, comment="test")

    def tearDown(self):
        mgr = fs_mgr()
        mgr.del_fs("test_dir")


    def test_dir_operation(self):
        mgr = fs_mgr()
        f = mgr.get_fs_by_name("test_dir")

        f.create_dir("test")
        dir_list = f.ls_dir()
        found = False
        for each_dir in dir_list:
            if each_dir["name"] == "test":
                found = True
                self.assertEquals(each_dir["mode"], 0777)
                self.assertEquals(each_dir["abspath"], "/mnt/test_dir/test")
                self.assertEquals(each_dir["relpath"], "test")
                self.assertEquals(each_dir["user"], "root")
                self.assertEquals(each_dir["group"], "root")
        self.assertTrue(found)
        f.mod_dir_mode("test", 0666)
        dir_list = f.ls_dir()
        for each_dir in dir_list:
            if each_dir["name"] == "test":
                self.assertEquals(each_dir["mode"], 0666)

        f.mod_dir_owner("test", "root", "root")

        usage_list = f.dir_usage_stat("test")
        found = False
        for each_usage in usage_list:
            if each_usage["abspath"] == "/mnt/test_dir/test":
                found = True
        self.assertTrue(found)

        f.delete_dir("test")











