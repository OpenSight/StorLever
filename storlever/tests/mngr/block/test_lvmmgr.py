import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.lvm.lvm import lvm_mgr
from storlever.lib.exception import StorLeverError
from storlever.tests.mngr.block.utils import get_block_dev, get_extra_block_dev


class TestLVM(unittest.TestCase):

    def tearDown(self):
        pass

    def test_lvm(self):
        lvm = lvm_mgr()
        # create VG
        device = get_block_dev()
        if device == "":
            return  # no test
        lvm.new_vg('test_vg', [device])
        vg = lvm.get_vg('test_vg')
        self.assertIn(os.path.basename(device), vg.pvs)
        pv = vg.get_pv(device)
        self.assertEqual(pv.dev_file, device)
        # create LV
        vg.create_lv('test_lv1', 64*1024*1024*10)
        self.assertIn('test_lv1', vg.lvs)
        lv = vg.get_lv('test_lv1')
        self.assertEqual(lv.name, 'test_lv1')
        # resize LV
        lv.resize(64*1024*1024*15)
        self.assertEqual(lv.size, 64*1024*1024*15)
        # remove LV
        lv.delete()
        self.assertNotIn('test_lv1', vg.lvs)
        # grow VG
        device_extra = get_extra_block_dev()
        if device_extra != "":
            vg.grow(device_extra)
            vg = lvm.get_vg('test_vg')
            self.assertEqual(len(vg.pvs), 2)
            self.assertIn(os.path.basename(device), vg.pvs)
            self.assertIn(os.path.basename(device_extra), vg.pvs)
            # shrink VG
            vg.shrink(device)
            vg = lvm.get_vg('test_vg')
            self.assertIn(os.path.basename(device_extra), vg.pvs)
            self.assertNotIn(os.path.basename(device), vg.pvs)
        # delete VG
        vg.delete()
        self.assertRaises(StorLeverError, lvm.get_vg, 'test_vg')



