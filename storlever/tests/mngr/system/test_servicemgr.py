import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.system.servicemgr import service_mgr


class TestServiceMgr(unittest.TestCase):

    def test_service_list(self):
        manager = service_mgr()
        service_list = manager.service_list()
        hasSshd = False
        for ser in service_list:
            if "sshd" in ser["name"]:
                hasSshd = True

        self.assertEquals(True, hasSshd)

    def test_service_op(self):
        manager = service_mgr()
        ser = manager.get_service_by_name("sshd")
        org_state = ser.get_state()
        org_auto_start = ser.get_auto_start()
        ser.start()
        ser.enable_auto_start()
        self.assertEquals(True, ser.get_state())
        self.assertEquals(True, ser.get_auto_start())
        service_list = manager.service_list()
        for entry in service_list:
            if "sshd" == entry["name"]:
                self.assertEquals("True", entry["state"])
                self.assertEquals("True", entry["auto_start"])
        ser.stop()
        ser.disable_auto_start()
        self.assertEquals(False, ser.get_state())
        self.assertEquals(False, ser.get_auto_start())
        if org_state:
            ser.start()
        if org_auto_start:
            ser.enable_auto_start()






