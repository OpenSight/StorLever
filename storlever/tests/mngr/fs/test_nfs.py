import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.fs.fsmgr import fs_mgr
from storlever.mngr.fs import nfs

test_nfs_src = None


def get_nfs_src():
    global test_nfs_src
    if test_nfs_src is None:
        test_nfs_src = raw_input("Please input a nfs source(format: IP:PATH)(empty means no test):")

    return test_nfs_src

class TestMkfs(unittest.TestCase):

    def test_mkfs_no_option(self):
        mgr = fs_mgr()
        nfs_source = get_nfs_src()
        if nfs_source == "":
            return
        mgr.mkfs_on_dev("nfs", nfs_source)


class TestFsMgr(unittest.TestCase):

    def test_type_list(self):
        mgr = fs_mgr()
        self.assertTrue("nfs" in mgr.fs_type_list())

    def test_add_fs(self):
        mgr = fs_mgr()
        dev_file = get_nfs_src()
        if dev_file == "":
            return
        mgr.mkfs_on_dev("nfs", dev_file)
        mgr.add_fs("test_nfs", "nfs", dev_file, comment="test")
        self.assertTrue("test_nfs" in mgr.fs_name_list())
        f = mgr.get_fs_by_name("test_nfs")
        self.assertEquals(f.fs_conf["dev_file"], dev_file)
        self.assertEquals(f.fs_conf["comment"], "test")
        self.assertTrue(f.is_available())
        self.assertTrue(f.usage_info()["total"] > 0)
        self.assertTrue(len(f.fs_meta_dump()) != 0)
        with open("/etc/fstab", "r") as fstab:
            self.assertTrue("/mnt/test_nfs" in fstab.read())
        mgr.del_fs("test_nfs")








