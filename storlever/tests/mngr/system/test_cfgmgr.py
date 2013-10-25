import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.system.cfgmgr import cfg_mgr


class TestCfgMgr(unittest.TestCase):

    def test_backup(self):

        file_content = ""

        # make test file
        with open("/etc/storlever_test", "w") as f:
            f.write("test")

        mgr = cfg_mgr()

        # backup config
        mgr.backup_to_file("/tmp/storlever_conf_test.tar.gz")

        with open("/etc/storlever_test", "r") as f:
            file_content = f.read()
        self.assertEquals("test", file_content)

        # change test file
        with open("/etc/storlever_test", "w") as f:
            f.write("test2")

        with open("/etc/storlever_test", "r") as f:
            file_content = f.read()
        self.assertEquals("test2", file_content)

        # restore config
        mgr.restore_from_file("/tmp/storlever_conf_test.tar.gz")

        # check test file
        with open("/etc/storlever_test", "r") as f:
            file_content = f.read()
        self.assertEquals("test", file_content)

        # clear backup config file
        os.remove("/tmp/storlever_conf_test.tar.gz")







