"""
storlever.mngr.block.iscsi.iface
~~~~~~~~~~~~~~~~

This module implements Iface class of iscsi initiator

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.lib.command import check_output
from storlever.lib import logger
import logging


ISCSIADM_CMD = "/sbin/iscsiadm"

class Iface(object):
    def __init__(self, mgr,
                 iscsi_ifacename, transport_name, hwaddress,
                 ipaddress, net_ifacename, initiatorname):
        self.mgr = mgr
        self.iscsi_ifacename = iscsi_ifacename
        self.transport_name = transport_name
        self.hwaddress = hwaddress
        self.ipaddress = ipaddress
        self.net_ifacename = net_ifacename
        self.initiatorname = initiatorname

    def get_conf(self):
        outlines = check_output([ISCSIADM_CMD, "-m", "iface", "-I", self.iscsi_ifacename],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        return self.mgr.lines_to_property_dict(outlines)

    def _refresh_property(self):
        conf = self.get_conf()
        self.iscsi_ifacename = conf["iface.iscsi_ifacename"]
        self.transport_name = conf["iface.transport_name"]
        self.hwaddress = conf["iface.hwaddress"]
        self.ipaddress = conf["iface.ipaddress"]
        self.net_ifacename = conf["iface.net_ifacename"]
        self.initiatorname = conf["iface.initiatorname"]

    def set_conf(self, name, value, operator="unkown"):
        name = str(name).strip()
        value = str(value).strip()
        check_output([ISCSIADM_CMD, "-m", "iface", "-I", self.iscsi_ifacename, "-o", "update",
                      "-n", name, "-v", value], input_ret=[2, 6, 7, 21, 22])

        self._refresh_property()

        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator iface (%s) conf (%s:%s) is updated by operator(%s)" %
                   (self.iscsi_ifacename, name, value, operator))


