import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.scsimgr import scsi_mgr


test_block = None

def get_block_dev():
    global test_block
    if test_block is None:
        test_block = raw_input("Please input a free scsi dev(dev file path) for scsi test:")
        test_block = test_block.strip()

    return test_block

class TestScsiMgr(unittest.TestCase):

    def test_scsi_list(self):
        mgr = scsi_mgr()
        dev_list = mgr.get_scsi_dev_list()
        self.assertTrue(len(dev_list) != 0)
        host_list = mgr.get_scsi_host_list()
        self.assertTrue(len(host_list) != 0)

    def test_scsi_op(self):
        mgr = scsi_mgr()
        test_dev_file = get_block_dev()
        if test_dev_file == "":
            return
        dev_list = mgr.get_scsi_dev_list()
        test_scsi_dev = None
        for scsi_dev in dev_list:
            if scsi_dev.dev_file == test_dev_file:
                test_scsi_dev = scsi_dev
                break;
        self.assertTrue(test_scsi_dev is not None)
        self.assertEquals(test_scsi_dev.state, "running")

        smart_info = test_scsi_dev.get_smart_info()

        test_scsi_dev.rescan_dev()
        test_scsi_dev.safe_delete()

        dev_list = mgr.get_scsi_dev_list()
        found = False
        for scsi_dev in dev_list:
            if scsi_dev.dev_file == test_dev_file:
                found = True
        self.assertFalse(found)

        mgr.rescan_bus()

        dev_list = mgr.get_scsi_dev_list()
        found = False
        for scsi_dev in dev_list:
            if scsi_dev.dev_file == test_dev_file:
                found = True
        self.assertTrue(found)











