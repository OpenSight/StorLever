import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.nas.nfsmgr import nfs_mgr


class TestNfsMgr(unittest.TestCase):

    def test_nfs_export(self):
        mgr = nfs_mgr()
        try:
            mgr.get_export_conf("test_export")
            mgr.del_export_conf("test_export")
        except Exception:
            pass

        mgr.append_export_conf("test_export", "/home", [{"host": "*", "options":"rw"}])
        export_list = mgr.get_export_list()
        found = False
        for export_point in export_list:
            if export_point["name"] == "test_export":
                found = True
                self.assertEquals(export_point["path"], "/home")
                self.assertEquals(export_point["clients"], [{"host": "*", "options":"rw"}])
        self.assertTrue(found)

        export_point = mgr.get_export_conf("test_export")
        self.assertEquals(export_point["path"], "/home")
        self.assertEquals(export_point["clients"], [{"host": "*", "options":"rw"}])

        mgr.set_export_conf("test_export", "/etc", [])
        export_point = mgr.get_export_conf("test_export")
        self.assertEquals(export_point["path"], "/etc")
        self.assertEquals(export_point["clients"], [])

        mgr.del_export_conf("test_export")

        export_list = mgr.get_export_list()
        found = False
        for export_point in export_list:
            if export_point["name"] == "test_export":
                found = True
        self.assertFalse(found)









