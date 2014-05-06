import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from storlever.mngr.system.modulemgr import module_mgr


class TestModuleMgr(unittest.TestCase):

    def test_module_register(self):
        manager = module_mgr()
        module_list = manager.get_modules_name_list()
        self.assertFalse("test" in module_list)
        manager.register_module("test", ["coreutils"], "test module")
        module_list = manager.get_modules_name_list()
        self.assertTrue("test" in module_list)
        module_info = manager.get_module_info("test")
        self.assertEquals(module_info["module_name"], "test")
        self.assertEquals(module_info["comment"], "test module")
        found = False
        for rpm_info in module_info["rpms"]:
            found = True
            self.assertEquals(rpm_info["package_name"], "coreutils")
            self.assertTrue(rpm_info["installed"])
        self.assertTrue(found)
        manager.unregister_module("test")
        module_list = manager.get_modules_name_list()
        self.assertFalse("test" in module_list)









