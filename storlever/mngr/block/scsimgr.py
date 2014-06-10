"""
storlever.mngr.block.scsimgr
~~~~~~~~~~~~~~~~

This module implements scsi device manager

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path
import re
from stat import *

from storlever.lib.command import check_output, write_file_entry, read_file_entry
from storlever.lib.exception import StorLeverError
from storlever.mngr.block.blockmgr import BLOCKDEV_CMD
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "scsi",
    "rpms": [
        "lsscsi",
        "sg3_utils"
        "smartmontools"
    ],
    "comment": "Provides the management functions for scsi device"
}

LSSCSI_CMD = "/usr/bin/lsscsi"
SCSI_RESCAN_CMD = "/usr/bin/rescan-scsi-bus.sh"
SMARTCTL_CMD = "/usr/sbin/smartctl"

class ScsiDev(object):
    def __init__(self, scsi_id, scsi_type, dev_file, sg_file):
        self.scsi_id = scsi_id
        self.scsi_type = scsi_type
        self.dev_file = dev_file
        self.sg_file = sg_file
        mode = os.stat(dev_file)[ST_MODE]
        if S_ISBLK(mode):
            self.block_name = os.path.basename(dev_file)
        else:
            self.block_name = ""

    @property
    def vendor(self):
        return read_file_entry(
            os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/vendor"),
            "unkown").strip()


    @property
    def model(self):
        return read_file_entry(
            os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/model"),
            "unkown").strip()

    @property
    def rev(self):
        return read_file_entry(
            os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/rev"),
            "1.0").strip()

    @property
    def state(self):
        return read_file_entry(
            os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/state"),
            "running").strip()

    def safe_delete(self):
        # flush dev's buf first
        try:
            if self.dev_file != "":
                check_output([BLOCKDEV_CMD, "--flushbufs", self.dev_file])
        except Exception:
            pass
        delete_path = os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/delete")
        write_file_entry(delete_path, "1\n")

    def rescan_dev(self):
        '''rescan the device can update the device's state(including size) in host system'''
        state_path = os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/rescan")
        write_file_entry(state_path, "1\n")

    def offline_dev(self, scsi_id):
        state_path = os.path.join("/sys/class/scsi_device/", self.scsi_id, "device/state")
        write_file_entry(state_path, "offline\n")

    def get_smart_info(self):
        if self.dev_file == "":
            raise StorLeverError("scsi_id (%s) has not be recognized" % self.scsi_id, 400)
        output = check_output([SMARTCTL_CMD, "-i", "-T", "verypermissive", self.dev_file])
        smart_enabled = False
        auto_offline_enabled = False
        if "SMART support is: Enabled" in output:
            smart_enabled = True
            output = check_output([SMARTCTL_CMD, "-a", "-T", "verypermissive", self.dev_file])

            if "Auto Offline Data Collection: Enabled" in output:
                auto_offline_enabled = True

        # filter the copyright
        lines = output.splitlines()
        for index, line in enumerate(lines):
            if line == "":
                break
        else:
            index = 0
        detail = "\n".join(lines[index + 1:])

        info = {
            "smart_enabled": smart_enabled,
            "auto_offline_enabled": auto_offline_enabled,
            "detail": detail
        }
        return info

    def set_smart_config(self, smart_enabled=None, auto_offline_enabled=None):

        if self.dev_file == "":
            raise StorLeverError("scsi_id (%s) has not be recognized" % self.scsi_id, 400)

        if smart_enabled is not None:
            if smart_enabled:
                param = "on"
            else:
                param = "off"
            out = check_output([SMARTCTL_CMD, "-s", param, "-T", "verypermissive", self.dev_file])

        if auto_offline_enabled is not None:
            if auto_offline_enabled:
                param = "on"
            else:
                param = "off"
            out = check_output([SMARTCTL_CMD, "-o", param, "-T", "verypermissive", self.dev_file])

    def smart_test(self, scsi_id, test_type):
        if test_type not in ("offline", "short", "long", "conveyance"):
            raise StorLeverError("test_type (%s) Not Support" % test_type, 400)

        if self.dev_file == "":
            raise StorLeverError("scsi_id (%s) has not be recognized" % self.scsi_id, 400)

        out = check_output([SMARTCTL_CMD, "-t", test_type, "-T", "verypermissive", self.dev_file])



class ScsiManager(object):

    """contains all methods to manage scsi device in linux system"""
    def get_scsi_dev_list(self):
        dev_list = []
        lines = check_output([LSSCSI_CMD, "-g"]).splitlines()
        for line in lines:
            line_list = line.split()
            scsi_id = line_list[0].strip(" []")
            scsi_type = line_list[1]

            dev_file = ""
            sg_file = ""
            for entry in line_list:
                if entry.startswith("/dev/sg"):
                    sg_file = entry
                elif entry.startswith("/dev/"):
                    dev_file = entry
            scsi_dev = ScsiDev(scsi_id, scsi_type, dev_file, sg_file)
            dev_list.append(scsi_dev)

        return dev_list

    def get_scsi_dev_by_id(self, scsi_id):
        lines = check_output([LSSCSI_CMD, "-g", scsi_id]).splitlines()
        if not lines:
            raise StorLeverError("scsi_id (%s) Not Found" % scsi_id, 404)

        line_list = lines[0].split()
        scsi_id = line_list[0].strip(" []")
        scsi_type = line_list[1]

        dev_file = ""
        sg_file = ""
        for entry in line_list:
            if entry.startswith("/dev/sg"):
                sg_file = entry
            elif entry.startswith("/dev/"):
                dev_file = entry

        return ScsiDev(scsi_id, scsi_type, dev_file, sg_file)

    def get_scsi_host_list(self):
        host_list = []
        lines = check_output([LSSCSI_CMD, "-H"]).splitlines()
        for line in lines:
            line_list = line.split()
            host_list.append({
                "host_number": line_list[0].strip(" []"),
                "type": line_list[1],
            })
        return host_list

    def rescan_bus(self, host=[], channels=[], targets=[], luns=[],
                 remove=False, force_rescan=False, force_remove=False):
        cmd_list = [SCSI_RESCAN_CMD]
        if remove:
            cmd_list.append("-r")
        if force_remove:
            cmd_list.append("--forceremove")
        if force_rescan:
            cmd_list.append("--forcerescan")

        if len(host) != 0:
            cmd_list.append("--hosts=" + (",".join(host)))
        if len(channels) != 0:
            cmd_list.append("--channels=" + (",".join(channels)))
        if len(targets) != 0:
            cmd_list.append("--ids=" + (",".join(targets)))
        if len(luns) != 0:
            cmd_list.append("--luns=" + (",".join(luns)))

        out = check_output(cmd_list)

ScsiManager = ScsiManager()
ModuleManager.register_module(**MODULE_INFO)

def scsi_mgr():
    """return the global block manager instance"""
    return ScsiManager








