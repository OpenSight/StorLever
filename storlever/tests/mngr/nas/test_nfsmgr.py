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
        export_list = mgr.get_export_list()
        for export_point in export_list:
            if export_point["path"] == "/home":
                index = export_list.index(export_point)
                mgr.del_export_conf(index)

        index = mgr.append_export_conf("/home")
        export_list = mgr.get_export_list()
        found = False
        for export_point in export_list:
            if export_point["path"] == "/home":
                found = True
                self.assertEquals(export_point["clients"], [])
        self.assertTrue(found)

        export_point = mgr.get_export_conf(index)
        self.assertEquals(export_point["path"], "/home")
        self.assertEquals(export_point["clients"], [])

        mgr.set_export_conf(index, "/etc")
        export_point = mgr.get_export_conf(index)
        self.assertEquals(export_point["path"], "/etc")

        mgr.del_export_conf(index)

        export_list = mgr.get_export_list()
        found = False
        for export_point in export_list:
            if export_point["path"] == "/home":
                found = True
        self.assertFalse(found)

    def test_nfs_client(self):

        mgr = nfs_mgr()
        export_index = -1
        export_list = mgr.get_export_list()
        for export_point in export_list:
            if export_point["path"] == "/home":
                export_index = export_list.index(export_point)
                break
        if export_index == -1:  # not found
            export_index = mgr.append_export_conf("/home")

        client_index = mgr.add_client(export_index,"*", "rw")

        client_list = mgr.get_export_conf(export_index)["clients"]
        found = False
        for nfs_client in client_list:
            if nfs_client["host"] == "*":
                found = True
                self.assertEquals(nfs_client["options"], "rw")
        self.assertTrue(found)

        mgr.update_client(export_index, client_index, "*", "ro")
        client_conf =  mgr.get_export_conf(export_index)["clients"][client_index]
        self.assertEquals(client_conf["options"], "ro")

        mgr.del_client(export_index, client_index)

        client_list = mgr.get_export_conf(export_index)["clients"]
        found = False
        for nfs_client in client_list:
            if nfs_client["host"] == "*":
                found = True
        self.assertFalse(found)

        mgr.del_export_conf(export_index)

        export_list = mgr.get_export_list()
        found = False
        for export_point in export_list:
            if export_point["path"] == "/home":
                found = True
        self.assertFalse(found)










