"""
storlever.mngr.block.iscsi.node
~~~~~~~~~~~~~~~~

This module implements Node class of iscsi initiator

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""



from storlever.lib.command import check_output
from storlever.lib import logger
import logging


ISCSIADM_CMD = "/sbin/iscsiadm"
class Node(object):
    def __init__(self, mgr, target, portal):
        self.mgr = mgr
        self.target = str(target)
        self.portal = str(portal)

    def get_conf(self):
        outlines = check_output([ISCSIADM_CMD, "-m", "node",
                                 "-T", self.target, "-p", self.portal],
                                input_ret=[2, 6, 7, 21, 22]).splitlines()
        return self.mgr.lines_to_property_dict(outlines)

    def set_conf(self, name, value, operator="unkown"):
        check_output([ISCSIADM_CMD, "-m", "node", "-T", self.target, "-p", self.portal,
                      "-o", "update", "-n", str(name), "-v", str(value)], input_ret=[2, 6, 7, 21, 22])
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) conf (%s:%s) is updated by operator(%s)" %
                   (self.target, self.portal, name, value, operator))

    def login(self, operator="unkown"):
        cmd = [ISCSIADM_CMD, "-m", "node","--login", "-T", self.target, "-p", self.portal]

        outlines = check_output(cmd, input_ret=[2, 6, 7, 21, 22]).splitlines()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) is login by operator(%s)" %
                   (self.target, self.portal, operator))

    def logout(self, operator="unkown"):
        cmd = [ISCSIADM_CMD, "-m", "node","--logout", "-T", self.target, "-p", self.portal]

        outlines = check_output(cmd, input_ret=[2, 6, 7, 21, 22]).splitlines()
        logger.log(logging.INFO, logger.LOG_TYPE_CONFIG,
                   "iscsi initiator node (%s, %s) is logout by operator(%s)" %
                   (self.target, self.portal, operator))
