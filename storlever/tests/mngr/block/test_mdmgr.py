import sys
import os

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.block.md.md import md_mgr
from storlever.lib.exception import StorLeverError
from storlever.tests.mngr.block.utils import get_block_dev, get_extra_block_dev


class TestMD(unittest.TestCase):

    def tearDown(self):
        pass

    def test_md(self):

        md = md_mgr()

