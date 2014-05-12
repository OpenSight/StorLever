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
        manager.register_module("test", ["coreutils"], ["/bin/ls"], "test module")
        module_list = manager.get_modules_name_list()
        self.assertTrue("test" in module_list)
        module_info = manager.get_module_info("test")
        self.assertEquals(module_info["module_name"], "test")
        self.assertEquals(module_info["comment"], "test module")
        found = False
        for requires in module_info["requires"]:
            if requires["name"] == "coreutils":
                found = True
                self.assertEquals(requires["type"], "rpm")
                self.assertTrue(requires["installed"])
        self.assertTrue(found)

        found = False
        for requires in module_info["requires"]:
            if requires["name"] == "/bin/ls":
                found = True
                self.assertEquals(requires["type"], "file")
                self.assertTrue(requires["installed"])
        self.assertTrue(found)

        manager.unregister_module("test")
        module_list = manager.get_modules_name_list()
        self.assertFalse("test" in module_list)









