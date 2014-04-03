import sys
import os
from storlever.lib.exception import StorLeverError

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.san.tgt.tgtmgr import tgt_mgr


class TestTgtTarget(unittest.TestCase):

    def setUp(self):
        mgr = tgt_mgr()
        try:
            mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
            mgr.remove_target_by_iqn("iqn.2014-09.com.example:server.test")
        except Exception:
            pass
        mgr.create_target("iqn.2014-09.com.example:server.test")

    def tearDown(self):
        mgr = tgt_mgr()
        mgr.remove_target_by_iqn("iqn.2014-09.com.example:server.test")

    def test_initiator_addr_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue(target.get_initiator_addr_list() == [])
        target.set_initiator_addr_list(["192.168.1.0/24", "192.168.2.0/24"])

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        addr_list = target.get_initiator_addr_list()
        self.assertTrue(addr_list == ["192.168.1.0/24", "192.168.2.0/24"])



    def test_initiator_name_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue(target.get_initiator_name_list() == [])
        target.set_initiator_name_list(["iqn.2014-09.com.example:initiator1",
                                        "iqn.2014-09.com.example:initiator2"])
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        name_list = target.get_initiator_name_list()
        self.assertTrue(name_list ==["iqn.2014-09.com.example:initiator1",
                                     "iqn.2014-09.com.example:initiator2"])

    def test_incominguser_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue(target.get_incominguser_list() == [])
        target.set_incominguser("test", "123456")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue("test" in target.get_incominguser_list())
        target.set_incominguser("test", "12345678")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue("test" in target.get_incominguser_list())
        target.del_incominguser("test")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")

        self.assertFalse("test" in target.get_incominguser_list())

    def test_outgoinguser_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue(target.get_outgoinguser_list() == [])
        target.set_outgoinguser("test", "123456")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue("test" in target.get_outgoinguser_list())
        target.set_outgoinguser("test", "12345678")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertTrue("test" in target.get_outgoinguser_list())
        target.del_outgoinguser("test")

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertFalse("test" in target.get_outgoinguser_list())

    def test_lun_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        target.add_lun(3, "/dev/loop0");

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        lun_conf_list = target.get_lun_list()
        found = False
        for lun_conf in lun_conf_list:
            if lun_conf["lun"] == 3:
                found = True
                self.assertEquals(lun_conf["write_cache"], True)
                self.assertEquals(lun_conf["readonly"], False)
                self.assertEquals(lun_conf["online"], True)
                self.assertEquals(lun_conf["device_type"], "disk")
                self.assertEquals(lun_conf["bs_type"], "rdwr")
        self.assertTrue(found)


        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        lun_conf = target.get_lun_by_num(3);
        self.assertEquals(lun_conf["write_cache"], True)
        self.assertEquals(lun_conf["readonly"], False)
        self.assertEquals(lun_conf["online"], True)
        self.assertEquals(lun_conf["device_type"], "disk")
        self.assertEquals(lun_conf["bs_type"], "rdwr")

        target.set_lun(3, online=False, write_cache=False)
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        lun_conf = target.get_lun_by_num(3);
        self.assertEquals(lun_conf["write_cache"], False)
        self.assertEquals(lun_conf["online"], False)

        target.del_lun(3)

        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        lun_conf_list = target.get_lun_list()
        found = False
        for lun_conf in lun_conf_list:
            if lun_conf["lun"] == 3:
                found = True
        self.assertFalse(found)

    def test_target_state(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        state = target.get_state()
        if state == "error":
         with self.assertRaises(StorLeverError):
            target.set_state("ready")
        else:
            target.set_state("ready")

    def test_target_session_list(self):
        mgr = tgt_mgr()
        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        target.get_session_list()










