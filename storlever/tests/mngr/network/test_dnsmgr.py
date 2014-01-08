import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.network.dnsmgr import dns_mgr


class TestDnsMgr(unittest.TestCase):

    def test_name_servers(self):
        manager = dns_mgr()
        org_server_list = manager.get_name_servers()
        manager.set_name_servers(["8.8.8.8"])
        self.assertEqual(["8.8.8.8"], manager.get_name_servers())
        manager.set_name_servers(org_server_list)








