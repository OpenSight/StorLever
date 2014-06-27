import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.utils.smartdmgr import smartd_mgr


class TestSnmpAgentMgr(unittest.TestCase):

    def test_monitor(self):
        mgr = smartd_mgr()
        old_monitor_list = mgr.get_monitor_list()
        try:
            new_monitor_list = [
                {
                    "dev": "/dev/sda",
                    "mail_to": "test@163.com",
                    "mail_test": True,
                    "mail_exec": "/bin/sh",
                    "schedule_regexp": "S/../.././01"
                }
            ]
            mgr.set_monitor_list(new_monitor_list)
            check_monitor_list = mgr.get_monitor_list()
            self.assertEquals(len(check_monitor_list), 1)
            monitor_conf = check_monitor_list[0]
            self.assertEquals(monitor_conf["dev"], "/dev/sda")
            self.assertEquals(monitor_conf["mail_to"], "test@163.com")
            self.assertEquals(monitor_conf["mail_test"], True)
            self.assertEquals(monitor_conf["mail_exec"], "/bin/sh")
            self.assertEquals(monitor_conf["schedule_regexp"], "S/../.././01")


            new_monitor_list = [
                {
                    "dev": "/dev/sda",
                    "mail_to": "test@sina.com",
                    "mail_test": False,
                    "mail_exec": "/bin/mail",
                    "schedule_regexp": ""
                }
            ]
            mgr.set_monitor_list(new_monitor_list)
            check_monitor_list = mgr.get_monitor_list()
            self.assertEquals(len(check_monitor_list), 1)
            monitor_conf = check_monitor_list[0]
            self.assertEquals(monitor_conf["dev"], "/dev/sda")
            self.assertEquals(monitor_conf["mail_to"], "test@sina.com")
            self.assertEquals(monitor_conf["mail_test"], False)
            self.assertEquals(monitor_conf["mail_exec"], "/bin/mail")
            self.assertEquals(monitor_conf["schedule_regexp"], "")

        finally:
            mgr.set_monitor_list(old_monitor_list)






