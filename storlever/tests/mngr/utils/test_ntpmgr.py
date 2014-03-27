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
        server_list = mgr.get_server_conf_list()
        for server_conf in server_list:
            if server_conf["server_addr"] == "0.asia.pool.ntp.org":
                index = server_list.index(server_conf)
                mgr.del_server_conf(index)

        index = mgr.append_server_conf("0.asia.pool.ntp.org", prefer=True)
        server_list = mgr.get_server_conf_list()
        found = False
        for server_conf in server_list:
            if server_conf["server_addr"] == "0.asia.pool.ntp.org":
                found = True
                self.assertTrue(server_conf["prefer"])
        self.assertTrue(found)

        server_conf = mgr.get_server_conf(index)
        self.assertEquals(server_conf["server_addr"], "0.asia.pool.ntp.org")
        self.assertEquals(server_conf["prefer"], True)

        mgr.set_server_conf(index, server_addr="1.asia.pool.ntp.org")
        server_conf = mgr.get_server_conf(index)
        self.assertEquals(server_conf["server_addr"], "1.asia.pool.ntp.org")

        mgr.del_server_conf(index)

        server_list = mgr.get_server_conf_list()
        found = False
        for server_conf in server_list:
            if server_conf["server_addr"] == "0.asia.pool.ntp.org":
                found = True
        self.assertFalse(found)

    def test_restrict(self):

        mgr = ntp_mgr()
        restrict_list = mgr.get_restrict_list()
        for restrict_conf in restrict_list:
            if restrict_conf["restrict_addr"] == "192.168.222.1":
                index = restrict_list.index(restrict_conf)
                mgr.del_restrict(index)

        index = mgr.append_restrict("192.168.222.1", mask="255.255.255.0")
        restrict_list = mgr.get_restrict_list()
        found = False
        for restrict_conf in restrict_list:
            if restrict_conf["restrict_addr"] == "192.168.222.1":
                found = True
                self.assertEquals(restrict_conf["mask"], "255.255.255.0")
        self.assertTrue(found)

        restrict_conf = mgr.get_restrict(index)
        self.assertEquals(restrict_conf["restrict_addr"], "192.168.222.1")
        self.assertEquals(restrict_conf["mask"], "255.255.255.0")

        mgr.set_restrict(index, restrict_addr="192.168.223.1")
        restrict_conf = mgr.get_restrict(index)
        self.assertEquals(restrict_conf["restrict_addr"], "192.168.223.1")

        mgr.del_restrict(index)

        restrict_list = mgr.get_restrict_list()
        found = False
        for restrict_conf in restrict_list:
            if restrict_conf["restrict_addr"] == "192.168.223.1":
                found = True
        self.assertFalse(found)










