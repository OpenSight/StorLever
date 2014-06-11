import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.network.ifmgr import if_mgr
from utils import get_net_if


class TestEthInterfaceMgr(unittest.TestCase):

    def test_interface_list(self):
        manager = if_mgr()
        ifs_list = manager.get_interface_list()
        self.assertTrue(isinstance(ifs_list, list))
        self.assertGreater(len(ifs_list), 0)

    def test_interface_updown(self):
        manager = if_mgr()
        ifs_list = manager.interface_name_list()
        test_ifs_name = get_net_if()
        if test_ifs_name == "":
            return
        self.assertTrue(test_ifs_name in ifs_list)
        ifs = manager.get_interface_by_name(test_ifs_name)  # last interface to test
        org_up = ifs.property_info["up"]

        if org_up:
            ifs.down()
            self.assertEqual(False, ifs.property_info["up"])
            ifs.up()
            self.assertEqual(True, ifs.property_info["up"])
        else:
            ifs.up()
            self.assertEqual(True, ifs.property_info["up"])
            ifs.down()
            self.assertEqual(False, ifs.property_info["up"])

    def test_interface_ip(self):
        manager = if_mgr()
        ifs_list = manager.interface_name_list()
        test_ifs_name = get_net_if()
        if test_ifs_name == "":
            return
        self.assertTrue(test_ifs_name in ifs_list)
        ifs = manager.get_interface_by_name(test_ifs_name)  # last interface to test
        ip, mask, gateway = ifs.get_ip_config()
        ifs.set_ip_config("", "", "")
        new_ip, new_mask, new_gateway = ifs.get_ip_config()
        self.assertEqual("", new_ip)
        self.assertEqual("", new_mask)
        self.assertEqual("", new_gateway)
        ifs.set_ip_config(ip, mask, gateway)







