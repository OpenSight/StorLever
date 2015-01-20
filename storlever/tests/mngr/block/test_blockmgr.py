import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.blockmgr import  block_mgr
from storlever.tests.mngr.block.utils import get_block_dev

class TestBlockMgr(unittest.TestCase):

    def test_block_mgr(self):
        mgr = block_mgr()
        block_list = mgr.get_block_dev_list()
        block_dev = None
        for block_entry in block_list:
            # if block_entry.name.startswith("sd"):
            block_dev = block_entry
            break

        self.assertTrue(block_dev is not None)
        block_dev.flush_block_buf()

    def test_block_dev(self):

        mgr = block_mgr()
        device = get_block_dev()
        if device == "":
            return  # no test
        block_name = os.path.basename(device)
        block = mgr.get_block_dev_by_name(block_name)
        self.assertEquals(block.name, block_name)
        self.assertEquals(block.dev_file, device)
        block.refresh_property()
        block.flush_block_buf()
        block.clean_meta()















