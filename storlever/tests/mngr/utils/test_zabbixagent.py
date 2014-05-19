import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.utils.zabbixagent import zabbix_agent_mgr


class TestZabbixAgent(unittest.TestCase):

    def test_agent_conf(self):
        mgr = zabbix_agent_mgr()
        conf = mgr.get_agent_conf()
        org_hostname = conf["hostname"]
        mgr.set_agent_conf(hostname="testhost");
        conf = mgr.get_agent_conf()
        self.assertEquals(conf["hostname"], "testhost")
        mgr.set_agent_conf(hostname=org_hostname)

    def test_passive_server_list(self):
        mgr = zabbix_agent_mgr()
        org_server_list = mgr.get_passive_check_server_list()
        mgr.set_passive_check_server_list(["192.168.1.1", "192.168.1.2"])
        server_list = mgr.get_passive_check_server_list()
        self.assertEquals(server_list, ["192.168.1.1", "192.168.1.2"])
        mgr.set_passive_check_server_list(org_server_list)

    def test_active_server_list(self):
        mgr = zabbix_agent_mgr()
        org_server_list = mgr.get_active_check_server_list()
        mgr.set_active_check_server_list(["192.168.1.1", "192.168.1.2"])
        server_list = mgr.get_active_check_server_list()
        self.assertEquals(server_list, ["192.168.1.1", "192.168.1.2"])
        mgr.set_active_check_server_list(org_server_list)









