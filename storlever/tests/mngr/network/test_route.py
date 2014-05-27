import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.network.route import route_mgr


class TestRouteMgr(unittest.TestCase):

    def test_ipv4_route_list(self):
        manager = route_mgr()
        route_list = manager.get_ipv4_route_list()
        self.assertTrue(len(route_list) > 0)
        self.assertTrue("destination" in route_list[0])
        self.assertTrue("genmask" in route_list[0])

    def test_ipv6_route_list(self):
        manager = route_mgr()
        route_list = manager.get_ipv6_route_list()
        self.assertTrue(len(route_list) > 0)
        self.assertTrue("destination" in route_list[0])
        self.assertTrue("next_hop" in route_list[0])







