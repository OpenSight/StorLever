import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.md.md import md_mgr
from storlever.lib.exception import StorLeverError
from storlever.tests.mngr.block.utils import get_block_dev_simple


class TestMD(unittest.TestCase):

    def tearDown(self):
        pass

    def test_md(self):
        md = md_mgr()
        mds = md.get_all_md()
        dev1 = get_block_dev_simple()
        dev2 = get_block_dev_simple()
        if not dev1:
            return
        mds.create('/dev/md0', 1, (dev1, dev2))
        self.assertIn('md0', mds.raid_list)
        md0 = mds.get_md('/dev/md0')
        self.assertIn(dev1, (member['device'] for _, member in md0.members.iteritems()))
        self.assertIn(dev2, (member['device'] for _, member in md0.members.iteritems()))
        self.assertEqual(2, md0.raid_devices)
        mds.delete('/dev/md0')
        self.assertRaises(StorLeverError, mds.get_md, '/dev/md0')


