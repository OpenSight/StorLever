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

from storlever.lib.command import check_output, write_file_entry, read_file_entry
from storlever.lib.exception import StorLeverError
from storlever.mngr.block.blockmgr import BLOCKDEV_CMD
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "scsi",
    "rpms": [
        "lsscsi",
        "sg3_utils"
    ],
    "comment": "Provides the management functions for scsi device"
}

LSSCSI_CMD = "/usr/bin/lsscsi"
SCSI_RESCAN_CMD = "/usr/bin/rescan-scsi-bus.sh"

class ScsiManager(object):

    """contains all methods to manage scsi device in linux system"""

    def get_scsi_dev_list(self):
        dev_list = []
        lines = check_output([LSSCSI_CMD]).splitlines()
        for line in lines:
            line_list = line.split()
            scsi_id  = line_list[0].strip(" []")
            type = line_list[1]
            vendor = read_file_entry(os.path.join("/sys/class/scsi_device/", scsi_id, "device/vendor"),
                                     "unkown").strip()
            model = read_file_entry(os.path.join("/sys/class/scsi_device/", scsi_id, "device/model"),
                                     "unkown").strip()
            rev = read_file_entry(os.path.join("/sys/class/scsi_device/", scsi_id, "device/rev"),
                                     "1.0").strip()
            state = read_file_entry(os.path.join("/sys/class/scsi_device/", scsi_id, "device/state"),
                                     "running").strip()
            dev_file = ""
            for entry in line_list:
                if entry.startswith("/dev/"):
                    dev_file = entry
            dev_list.append({
                "scsi_id": scsi_id,
                "type": type,
                "vendor":vendor,
                "model": model,
                "state": state,
                "rev": rev,
                "dev_file": dev_file,
                "block_name":os.path.basename(dev_file)
            })
        return dev_list

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

    def safe_delete_dev(self, scsi_id):

        dev_list = self.get_scsi_dev_list()
        delete_scsi = None
        for dev_entry in dev_list:
            if dev_entry["scsi_id"] == scsi_id:
                delete_scsi = dev_entry
        if delete_scsi is None:
            raise StorLeverError("scsi_id (%s) Not Found" % scsi_id, 404)

        # flush dev's buf first
        try:
            dev_file = delete_scsi["dev_file"]
            if dev_file != "":
                check_output([BLOCKDEV_CMD, "--flushbufs", dev_file])
        except Exception:
            pass

        delete_path = os.path.join("/sys/class/scsi_device/", scsi_id, "device/delete")
        write_file_entry(delete_path, "1\n")

    def rescan_dev(self, scsi_id):
        '''rescan the device can update the device's state(including size) in host system'''

        # dev_list = self.get_scsi_dev_list()
        # seleted_scsi = None
        # for dev_entry in dev_list:
        #    if dev_entry["scsi_id"] == scsi_id:
        #        seleted_scsi = dev_entry
        #if seleted_scsi is None:
        #    raise StorLeverError("scsi_id (%s) Not Found" % scsi_id, 404)

        state_path = os.path.join("/sys/class/scsi_device/", scsi_id, "device/rescan")
        write_file_entry(state_path, "1\n")

    def remote_offline_dev(self, scsi_id):
        # dev_list = self.get_scsi_dev_list()
        # seleted_scsi = None
        #for dev_entry in dev_list:
        #    if dev_entry["scsi_id"] == scsi_id:
        #        seleted_scsi = dev_entry
        #if seleted_scsi is None:
        #    raise StorLeverError("scsi_id (%s) Not Found" % scsi_id, 404)

        state_path = os.path.join("/sys/class/scsi_device/", scsi_id, "device/state")
        write_file_entry(state_path, "offline\n")

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








