import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.blockmgr import  block_mgr


class TestBlockMgr(unittest.TestCase):

    def test_block_mgr(self):
        mgr = block_mgr()
        block_list = mgr.get_block_dev_list()
        block_dev = None
        for block_entry in block_list:
            if block_entry["name"].startswith("sd"):
                block_dev = block_entry
        self.assertTrue(block_dev is not None)
        mgr.flush_block_buf(block_dev["name"])














