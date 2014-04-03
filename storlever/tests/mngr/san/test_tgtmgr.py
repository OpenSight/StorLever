import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.san.tgt.tgtmgr import tgt_mgr


class TestTgtMgr(unittest.TestCase):

    def test_tgt_conf(self):
        mgr = tgt_mgr()
        conf = mgr.get_tgt_conf()
        self.assertTrue("incomingdiscoveryuser" in conf)
        self.assertTrue("outgoingdiscoveryuser" in conf)
        mgr.set_tgt_conf(incomingdiscoveryuser="test:test")
        conf = mgr.get_tgt_conf()
        self.assertTrue(conf["incomingdiscoveryuser"] == "test:*")
        mgr.set_tgt_conf(incomingdiscoveryuser="")

    def test_target_list(self):
        mgr = tgt_mgr()
        try:
            mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
            mgr.remove_target_by_iqn("iqn.2014-09.com.example:server.test")
        except Exception:
            pass

        mgr.create_target("iqn.2014-09.com.example:server.test")
        iqn_name_list = mgr.get_target_iqn_list()
        self.assertTrue("iqn.2014-09.com.example:server.test" in iqn_name_list)


        target = mgr.get_target_by_iqn("iqn.2014-09.com.example:server.test")
        self.assertEquals(target.iqn, "iqn.2014-09.com.example:server.test")

        mgr.remove_target_by_iqn("iqn.2014-09.com.example:server.test")

        iqn_name_list = mgr.get_target_iqn_list()
        self.assertFalse("iqn.2014-09.com.example:server.test" in iqn_name_list)













