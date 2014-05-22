import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.utils.ntpmgr import ntp_mgr


class TestNtpMgr(unittest.TestCase):

    def test_server(self):
        mgr = ntp_mgr()
        old_server_list = mgr.get_server_conf_list()
        try:

            new_server_list = [
                {
                    "server_addr": "0.asia.pool.ntp.org",
                    "prefer": True
                }
            ]
            mgr.set_server_conf_list(new_server_list)
            server_list = mgr.get_server_conf_list()
            self.assertEquals(len(server_list), 1)
            server_conf = server_list[0]
            self.assertEquals(server_conf["server_addr"], "0.asia.pool.ntp.org")
            self.assertTrue(server_conf["prefer"])

            new_server_list = [
                {
                    "server_addr": "1.asia.pool.ntp.org",
                    "prefer": False
                }
            ]
            mgr.set_server_conf_list(new_server_list)
            server_list = mgr.get_server_conf_list()
            self.assertEquals(len(server_list), 1)
            server_conf = server_list[0]
            self.assertEquals(server_conf["server_addr"], "1.asia.pool.ntp.org")
            self.assertFalse(server_conf["prefer"])

        finally:
            mgr.set_server_conf_list(old_server_list)


    def test_restrict(self):
        mgr = ntp_mgr()
        old_restrict_list = mgr.get_restrict_list()
        try:
            new_restrict_list = [
                {
                    "restrict_addr": "192.168.222.1",
                    "mask": "255.255.255.0"
                }
            ]
            mgr.set_restrict_list(new_restrict_list)
            restrict_list = mgr.get_restrict_list()
            self.assertEquals(len(restrict_list), 1)
            restrict_conf = restrict_list[0]
            self.assertEquals(restrict_conf["restrict_addr"], "192.168.222.1")
            self.assertEquals(restrict_conf["mask"], "255.255.255.0")

            new_restrict_list = [
                {
                    "restrict_addr": "192.168.223.1",
                    "mask": "255.255.0.0"
                }
            ]
            mgr.set_restrict_list(new_restrict_list)
            restrict_list = mgr.get_restrict_list()
            self.assertEquals(len(restrict_list), 1)
            restrict_conf = restrict_list[0]
            self.assertEquals(restrict_conf["restrict_addr"], "192.168.223.1")
            self.assertEquals(restrict_conf["mask"], "255.255.0.0")

        finally:
            mgr.set_restrict_list(old_restrict_list)











