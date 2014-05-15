import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.network.ifmgr import if_mgr
from storlever.mngr.network.bond import bond_mgr
from utils import get_net_if

class TestBondMgr(unittest.TestCase):

    def test_bond(self):
        manager = if_mgr()
        ifs_list = manager.interface_name_list()
        test_ifs_name = get_net_if()
        if test_ifs_name == "":
            return
        self.assertTrue(test_ifs_name in ifs_list)
        ifs = manager.get_interface_by_name(test_ifs_name)  # last interface to test
        ip, mask, gateway = ifs.get_ip_config()
        bond_manager = bond_mgr()
        bond_name = bond_manager.add_group(80, 1, [test_ifs_name],
                                           ip, mask, gateway)
        bond_list = bond_manager.group_name_list()

        self.assertTrue(True, isinstance(bond_list, list))
        self.assertGreater(len(bond_list), 0)
        self.assertEqual(bond_name, bond_list[0])

        bond_ifs = bond_manager.get_group_by_name(bond_name)
        self.assertEqual(bond_ifs.miimon, 80)
        self.assertEqual(bond_ifs.mode, 1)
        self.assertEqual((ip, mask, gateway), bond_ifs.get_ip_config())

        bond_manager.del_group(bond_name)
        ifs = manager.get_interface_by_name(test_ifs_name)
        self.assertEqual((ip, mask, gateway), ifs.get_ip_config())




