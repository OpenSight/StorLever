import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.nas.ftpmgr import ftp_mgr


class TestFtpMgr(unittest.TestCase):

    def test_ftp_conf(self):
        mgr = ftp_mgr()
        conf = mgr.get_ftp_conf()
        self.assertTrue("listen" in conf)
        orig_listen = conf["listen"]
        mgr.set_ftp_conf(listen=True)
        conf = mgr.get_ftp_conf()
        self.assertTrue(conf["listen"])
        mgr.set_ftp_conf(listen=False)
        conf = mgr.get_ftp_conf()
        self.assertFalse(conf["listen"])
        mgr.set_ftp_conf(listen=orig_listen)


    def test_ftp_user(self):
        mgr = ftp_mgr()
        try:
            mgr.get_user_conf("root")
            mgr.del_user_conf("root")
        except Exception:
            pass

        mgr.add_user_conf("root", True, True)
        user_conf_list = mgr.get_user_conf_list()
        found = False
        for user_conf in user_conf_list:
            if user_conf["user_name"] == "root":
                found = True
                self.assertEquals(user_conf["login_enable"], True)
                self.assertEquals(user_conf["chroot_enable"], True)
        self.assertTrue(found)

        user_conf = mgr.get_user_conf("root")
        self.assertEquals(user_conf["login_enable"], True)
        self.assertEquals(user_conf["chroot_enable"], True)
        self.assertEquals(user_conf["user_name"], "root")

        mgr.set_user_conf("root", chroot_enable=False)
        user_conf = mgr.get_user_conf("root")
        self.assertEquals(user_conf["chroot_enable"], False)

        mgr.del_user_conf("root")

        user_conf_list = mgr.get_user_conf_list()
        found = False
        for user_conf in user_conf_list:
            if user_conf["user_name"] == "root":
                found = True
        self.assertFalse(found)









