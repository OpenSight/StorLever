import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.fs.fsmgr import fs_mgr
from storlever.mngr.fs import ext4
from utils import get_block_dev


class TestMkfs(unittest.TestCase):

    def test_mkfs_no_option(self):
        mgr = fs_mgr()
        mgr.mkfs_on_dev("ext4", get_block_dev())


class TestFsMgr(unittest.TestCase):

    def test_type_list(self):
        mgr = fs_mgr()
        self.assertTrue("ext4" in mgr.fs_type_list())

    def test_add_fs(self):
        mgr = fs_mgr()
        dev_file = get_block_dev()
        mgr.mkfs_on_dev("ext4", get_block_dev())
        mgr.add_fs("test_ext4", "ext4", dev_file, comment="test")
        self.assertTrue("test_ext4" in mgr.fs_name_list())
        f = mgr.get_fs_by_name("test_ext4")
        self.assertEquals(f.fs_conf["dev_file"], dev_file)
        self.assertEquals(f.fs_conf["comment"], "test")
        self.assertTrue(f.is_available())
        self.assertTrue(f.usage_info()["percent"] < 10)
        self.assertTrue(len(f.fs_meta_dump()) != 0)
        f.grow_size()
        with open("/etc/fstab", "r") as fstab:
            self.assertTrue("/mnt/test_ext4" in fstab.read())

        mgr.del_fs("test_ext4")








