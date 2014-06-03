import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.utils.snmpagent import snmp_agent_mgr


class TestSnmpAgentMgr(unittest.TestCase):

    def test_basic_conf(self):
        mgr = snmp_agent_mgr()
        old_conf = mgr.get_basic_conf()

        mgr.set_basic_conf(sys_name="test_snmp")
        new_conf = mgr.get_basic_conf()
        self.assertEquals(new_conf["sys_name"], "test_snmp")
        mgr.set_basic_conf(config=old_conf)

    def test_community(self):
        mgr = snmp_agent_mgr()
        try:
            mgr.get_community_conf("test_community")
            mgr.del_community_conf("test_community")
        except Exception:
            pass

        mgr.add_community_conf("test_community", oid=".1", read_only=False)
        community_list = mgr.get_community_list()
        found = False
        for community_conf in community_list:
            if community_conf["community_name"] == "test_community":
                found = True
                self.assertEquals(community_conf["read_only"], False)
                self.assertEquals(community_conf["oid"], ".1")
        self.assertTrue(found)

        community_conf = mgr.get_community_conf("test_community")
        self.assertEquals(community_conf["read_only"], False)
        self.assertEquals(community_conf["oid"], ".1")
        self.assertEquals(community_conf["ipv6"], False)

        mgr.update_community_conf("test_community", read_only=True)
        community_conf = mgr.get_community_conf("test_community")
        self.assertEquals(community_conf["read_only"], True)

        mgr.del_community_conf("test_community")

        community_list = mgr.get_community_list()
        found = False
        for community_conf in community_list:
            if community_conf["community_name"] == "test_community":
                found = True
        self.assertFalse(found)

    def test_trap_sink_list(self):
        mgr = snmp_agent_mgr()
        old_sink_list = mgr.get_trap_sink_list()
        try:
            new_sink_list = [
                {
                    "host": "192.168.1.1",
                    "type": "trap2",
                    "community": "test_community"
                }
            ]
            mgr.set_trap_sink_list(new_sink_list)
            sink_list = mgr.get_trap_sink_list()
            self.assertEquals(len(sink_list), 1)
            sink_conf = sink_list[0]
            self.assertEquals(sink_conf["host"], "192.168.1.1")
            self.assertEquals(sink_conf["type"], "trap2")
            self.assertEquals(sink_conf["community"], "test_community")

            new_sink_list = [
                {
                    "host": "192.168.1.2",
                    "type": "trap",
                    "community": "test_community1"
                }
            ]
            mgr.set_trap_sink_list(new_sink_list)
            sink_list = mgr.get_trap_sink_list()
            self.assertEquals(len(sink_list), 1)
            sink_conf = sink_list[0]
            self.assertEquals(sink_conf["host"], "192.168.1.2")
            self.assertEquals(sink_conf["type"], "trap")
            self.assertEquals(sink_conf["community"], "test_community1")

        finally:
            mgr.set_trap_sink_list(old_sink_list)

    def test_monitor(self):
        mgr = snmp_agent_mgr()
        try:
            mgr.get_monitor_conf("test_monitor")
            mgr.del_monitor_conf("test_monitor")
        except Exception:
            pass

        mgr.add_monitor_conf("test_monitor", "sysContact.0", option="-r 60")
        monitor_list = mgr.get_monitor_list()
        found = False
        for monitor_conf in monitor_list:
            if monitor_conf["monitor_name"] == "test_monitor":
                found = True
                self.assertEquals(monitor_conf["expression"], "sysContact.0")
                self.assertEquals(monitor_conf["option"], "-r 60")
        self.assertTrue(found)

        monitor_conf = mgr.get_monitor_conf("test_monitor")
        self.assertEquals(monitor_conf["expression"], "sysContact.0")
        self.assertEquals(monitor_conf["option"], "-r 60")

        mgr.update_monitor_conf("test_monitor", expression="! sysContact.0")
        monitor_conf = mgr.get_monitor_conf("test_monitor")
        self.assertEquals(monitor_conf["expression"], "! sysContact.0")

        mgr.del_monitor_conf("test_monitor")

        monitor_list = mgr.get_monitor_list()
        found = False
        for monitor_conf in monitor_list:
            if monitor_conf["monitor_name"] == "test_monitor":
                found = True
        self.assertFalse(found)







