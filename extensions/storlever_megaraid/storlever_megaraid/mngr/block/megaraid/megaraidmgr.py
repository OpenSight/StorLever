"""
storlever_megaraid.mngr.block.megaraid.megaraidmgr
~~~~~~~~~~~~~~~~

This module provide the support for megaraid to storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import os.path

from storlever.lib.command import check_output
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "megaraid",
    "comment": "Provides the support for Megaraid controller, which can manage "
               "the the logical disk output by megaraid driver"
}



class MegaraidManager(object):

    def get_pd_manager(self):
        return PhysicalDriveManager()

    def get_vd_manager(self):
        return VirtualDriveManager()


class PhysicalDriveManager(object):
    """
    physical drive
    Megaraid SAS Software User Guide 7.18

    """

    def __init__(self):
        pass

    def list_pd(self):
        # list all PD
        # MegaCli -PDList -aN|-a0,1..|-aAll|
        pass

    def pd_info(self, pd):
        # MegaCli -PDInfo -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL|
        pass

    def online(self, pd):
        # MegaCli -PDOnline -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def offline(self, pd):
        # MegaCli -PDOffline -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def make_good(self, pd, force=False):
        # MegaCli -PDMakeGood -PhysDrv[E0:S0,E1:S1....] | [-Force] -aN|-a0,1,2|-aALL
        pass

    def start_init(self, pd):
        # MegaCli -PDClear -Start |-Stop|-ShowProg |-ProgDsply -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def stop_init(self, pd):
        # MegaCli -PDClear -Start |-Stop|-ShowProg |-ProgDsply -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def init_progress(self, pd):
        # MegaCli -PDClear -Start |-Stop|-ShowProg |-ProgDsply -PhysDrv[E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def start_rebuild(self, pd):
        # MegaCli -PDRbld -Start |-Stop|-Suspend|-Resume|-ShowProg |-ProgDsply -PhysDrv [E0:S0,E1:S1....] -aN|-a0,1,2|-aALL
        pass

    def stop_rebuild(self, pd):
        pass

    def rebuild_progress(self, pd):
        pass


class VirtualDriveManager(object):
    """
    virtual drive
    Megaraid SAS Software User Guide 7.16 and 7.17
    """

    def __init__(self):
        pass

    def vd_list(self):
        # MegaCli -LDInfo -Lx|-L0,1,2|-Lall -aN|-a0,1,2|-aALL
        pass

    def vd_info(self, vd):
        # MegaCli -LDInfo -Lx|-L0,1,2|-Lall -aN|-a0,1,2|-aALL
        pass

    def create_vd(self, ):
        # to create raid 0 1 5 6
        # MegaCli -CfgLDAdd
        pass

    def create_vd_ext(self):
        # to create raid 10 50 60
        # MegaCli -CfgSpanAdd
        pass

    def delete_vd(self, vd):
        # MegaCli -CfgLDDel -Lx|-L0,1,2|-Lall -aN|-a0,1,2|-aALL
        pass

    def set_cache_policy(self, write_back=True, read_ahead=True, cached=True):
        # MegaCli -LDSetProp {-Name LdNamestring} | -RW|RO|Blocked|RemoveBlocked |
        # WT|WB|ForcedWB [-Immediate] |RA|NORA| Cached|Direct | -EnDskCache|DisDskCache
        # | CachedBadBBU|NoCachedBadBBU | ExclusiveAccess|Shared |-L0,1,2|-Lall -aN|-a0,1,2|-aALL
        pass

    def start_init(self, vd):
        pass

    def abort_init(self, vd):
        pass

    def list_foreign(self):
        # MegaCli -CfgForeign
        pass

    def delete_foreign(self):
        pass

    def import_foreign(self):
        pass


MegaraidManager = MegaraidManager()
ModuleManager.register_module(**MODULE_INFO)

def megaraid_mgr():
    """return the global block manager instance"""
    return MegaraidManager








