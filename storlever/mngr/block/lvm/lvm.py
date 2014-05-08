"""
storlever.mngr.block.lvm.lvm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lvm manager of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os.path
from functools import wraps
from lvm2app import *
from storlever.lib.exception import StorLeverError
from storlever.mngr.system.modulemgr import ModuleManager

MODULE_INFO = {
    "module_name": "lvm",
    "rpms": [],
    "comment": "Provides the management functions for lvm subsystem(lvm2)"
}



class DeferAndCache(object):
    """
    Used as a decorator to defer the calculation of object attribute value
    until the first time it is accessed,
    and also cache the calculated value, so it will not be calculated again, once calculated
    """
    def __init__(self, calc_func):
        self._calc_func = calc_func
        self._attr_name = calc_func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self._calc_func(instance)
        instance.__dict__[self._attr_name] = value
        return value


class _LVM(object):

    def __init__(self):
        self._hdlr = lvm_init('')

    def close(self):
        if self._hdlr:
            lvm_quit(self._hdlr)
            self._hdlr = None

    def __enter__(self):
        if self._hdlr is None:
            self._hdlr = lvm_init('')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._hdlr:
            lvm_quit(self._hdlr)
            self._hdlr = None

    def check_hdlr(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._hdlr is None:
                raise StorLeverError('Empty LVM handler, unable to process')
            return func(self, *args, **kwargs)
        return wrapper

    @property
    def hdlr(self):
        return self._hdlr

    def raise_from_error(self, info=''):
        if self._hdlr is None:
            raise StorLeverError(info)
        elif info:
            raise StorLeverError(info + '\n' + lvm_errmsg(self._hdlr))
        else:
            raise StorLeverError(lvm_errmsg(self._hdlr))

    @check_hdlr
    def _create_pv(self, device):
        if lvm_pv_create(self._hdlr, device, 0) != 0:
            self.raise_from_error(info='Can not create PV on {0}'.format(device))

    @check_hdlr
    def remove_pv(self, device):
        if lvm_pv_remove(self._hdlr, device) != 0:
            self.raise_from_error(info='Failed to remove PV {0}'.format(device))

    @check_hdlr
    def create_vg(self, vg_name, devices=None, pe_size=64):
        """
        :param vg_name: string of volume group name
        :param devices: list of block names
        :param pe_size: integer in MB
        :return: None
        """
        # TODO maybe we need to check if block device in "devices" is already used
        with _VG(self, vg_name, mode=_VG.MODE_NEW) as vg:
            vg.set_extent_size(pe_size)
            for device in devices:
                vg.add_pv(device)

    @check_hdlr
    def delete_vg(self, vg_name):
        with _VG(self, vg_name, mode=_VG.MODE_WRITE) as vg:
            vg.delete()

    @check_hdlr
    def list_vg_names(self):
        vg_list = []
        names = lvm_list_vg_names(self._hdlr)
        if not bool(names):
            return vg_list
        vg = dm_list_first(names)
        while vg:
            c = cast(vg, POINTER(lvm_str_list))
            vg_list.append(c.contents.str)
            if dm_list_end(names, vg):
                # end of linked list
                break
            vg = dm_list_next(names, vg)
        return vg_list

    @check_hdlr
    def get_vg(self, name, mode=None):
        if mode is None:
            mode = _VG.MODE_READ
        return _VG(self, name, mode=mode)


class _VG(object):
    """
    Used _VG object ONLY in with context, for example:
    with _VG(lvm, 'new_vg') as vg:
        vg.set_extent_size()
        vg.add_pv()
    """

    MODE_READ = 0
    MODE_WRITE = 1
    MODE_NEW = 2

    def __init__(self, lvm, name, mode=MODE_READ):
        self._lvm = lvm
        if not lvm or not lvm.hdlr:
            raise StorLeverError('')
        self.name = name
        self._mode = mode
        if mode == self.MODE_READ:
            self._hdlr = lvm_vg_open(self._lvm.hdlr, self.name, 'r', 0)
        elif mode == self.MODE_WRITE:
            self._hdlr = lvm_vg_open(self._lvm.hdlr, self.name, 'w', 0)
        elif mode == self.MODE_NEW:
            self._hdlr = lvm_vg_create(self._lvm.hdlr, self.name)
        else:
            raise StorLeverError('Unknown VG operation mode')
        if not bool(self._hdlr):
            self.raise_from_error(info='Failed to open VG handler')

    def check_hdlr(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._hdlr is None:
                raise StorLeverError('Empty VG handler, unable to process')
            return func(self, *args, **kwargs)
        return wrapper

    def raise_from_error(self, info=''):
        if not self._lvm or not self._lvm.hdlr:
            raise StorLeverError('')
        self._lvm.raise_from_error(info)

    def __enter__(self):
        if not self._hdlr:
            self._hdlr = lvm_vg_create(self._lvm_hdlr, self.name)
            if not bool(self._hdlr):
                self.raise_from_error()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._hdlr and exc_type is None:
            # no error happened, let's try to commit the new VG to disk
            if self._mode in (self.MODE_NEW, self.MODE_WRITE):
                if lvm_vg_write(self._hdlr) != 0:
                    self._close()
                    raise self.raise_from_error('Failed commit VG creation')
            self._close()
        elif self._hdlr and exc_type:
            # failed in during creation, just close
            self._close()
        else:
            pass

    def _close(self):
        hdlr, self._hdlr = self._hdlr, None
        if hdlr:
            if lvm_vg_close(hdlr) != 0:
                raise self.raise_from_error('Failed to close VG handler')

    @check_hdlr
    def set_extent_size(self, size=64):
        """
        set physical extent size
        :param size: in MB, max 4096
        :return: None
        """
        if size > 4096:
            raise StorLeverError('PE too large')
        if lvm_vg_set_extent_size(self._hdlr, size*1024*1024) != 0:
            self.raise_from_error(info='Set physical extent size failed')

    @check_hdlr
    def add_pv(self, device):
        if not os.path.exists(device):
            raise StorLeverError('Not valid device {0}'.format(device))
            #self._create_pv(device)
        rc = lvm_vg_extend(self._hdlr, device)
        if rc != 0:
            raise self.raise_from_error()

    @check_hdlr
    def remove_pv(self, device):
        rc = lvm_vg_reduce(self._hdlr, device)
        if rc != 0:
            raise self.raise_from_error()

    @check_hdlr
    def delete(self):
        if lvm_vg_remove(self._hdlr) != 0:
            self.raise_from_error('Failed to delete VG {0}'.format(self.name))

    @check_hdlr
    def get_uuid(self):
        return lvm_vg_get_uuid(self._hdlr)

    @check_hdlr
    def get_name(self):
        return lvm_vg_get_name(self._hdlr)

    @check_hdlr
    def get_size(self):
        return lvm_vg_get_size(self._hdlr)

    @check_hdlr
    def get_free_size(self):
        return lvm_vg_get_free_size(self._hdlr)

    @check_hdlr
    def get_extent_size(self):
        return lvm_vg_get_extent_size(self._hdlr)

    @check_hdlr
    def get_extent_count(self):
        return lvm_vg_get_extent_count(self._hdlr)

    @check_hdlr
    def get_free_extent_count(self):
        return lvm_vg_get_free_extent_count(self._hdlr)

    @check_hdlr
    def iter_lv(self):
        lv_hdlr_list = lvm_vg_list_lvs(self._hdlr)
        if not bool(lv_hdlr_list):
            return
        lv = dm_list_first(lv_hdlr_list)
        while lv:
            c = cast(lv, POINTER(lvm_lv_list))
            yield _LV(self, hdlr=c.contents.lv)
            if dm_list_end(lv_hdlr_list, lv):
                # end of linked list
                break
            lv = dm_list_next(lv_hdlr_list, lv)

    @check_hdlr
    def get_max_lv(self):
        return lvm_vg_get_max_lv(self._hdlr)

    @check_hdlr
    def get_lv_by_name(self, name):
        return _LV(self, name=name)

    @check_hdlr
    def get_lv_by_uuid(self, uuid):
        return _LV(self, uuid=uuid)

    @check_hdlr
    def create_lv(self, name, size):
        lv_hdlr = lvm_vg_create_lv_linear(self._hdlr, name, size)
        if not bool(lv_hdlr):
            self.raise_from_error(info='Failed to create LV {0} in VG {1}'.format(name, self.name))
        return _LV(self, hdlr=lv_hdlr)

    @check_hdlr
    def iter_pv(self):
        pv_hdlr_list = lvm_vg_list_pvs(self._hdlr)
        if not bool(pv_hdlr_list):
            return
        pv = dm_list_first(pv_hdlr_list)
        while pv:
            c = cast(pv, POINTER(lvm_pv_list))
            yield _PV(self, hdlr=c.contents.pv)
            if dm_list_end(pv_hdlr_list, pv):
                # end of linked list
                break
            pv = dm_list_next(pv_hdlr_list, pv)

    @check_hdlr
    def get_pv_by_name(self, name):
        return _PV(self, name=name)

    @check_hdlr
    def get_pv_count(self):
        return lvm_vg_get_pv_count(self._hdlr)

    @check_hdlr
    def get_max_pv(self):
        return lvm_vg_get_max_pv(self._hdlr)

    @property
    def hdlr(self):
        return self._hdlr


class _LV(object):
    """
    Always use this inside VG's with context
    since LV's handler is inside VG's handler
    """
    def __init__(self, vg, hdlr=None, name=None, uuid=None):
        self._vg = vg
        if not vg or not vg.hdlr:
            raise StorLeverError('No valid VG handler')
        if hdlr:
            self._hdlr = hdlr
        elif name:
            self._hdlr = lvm_lv_from_name(vg.hdlr, name)
            if not bool(self._hdlr):
                raise StorLeverError('No LV {0} under VG {1}'.format(name, vg.name))
        elif uuid:
            self._hdlr = lvm_lv_from_uuid(vg.hdlr, uuid)
            if not bool(self._hdlr):
                raise StorLeverError('No LV {0} under VG {1}'.format(uuid, vg.name))
        else:
            raise StorLeverError('No valid parameter given to get a LV handler')
        self.name = self.get_name()
        self.uuid = self.get_uuid()
        self.size = self.get_size()

    def get_name(self):
        return lvm_lv_get_name(self._hdlr)

    def get_uuid(self):
        return lvm_lv_get_uuid(self._hdlr)

    def get_size(self):
        return lvm_lv_get_size(self._hdlr)

    def resize(self, size):
        if lvm_lv_resize(self._hdlr, size) != 0:
            self._vg.raise_from_error('Failed to resize LV {0}'.format(self.name))

    def delete(self):
        if lvm_vg_remove_lv(self._hdlr) != 0:
            self._vg.raise_from_error('Failed to remove LV {0}'.format(self.name))


class _PV(object):
    """
    Always use this inside VG's with context
    """
    def __init__(self, vg, hdlr=None, name=None, uuid=None):
        self._vg = vg
        if not vg or not vg.hdlr:
            raise StorLeverError('No valid VG handler')
        if hdlr:
            self._hdlr = hdlr
        elif name:
            self._hdlr = lvm_pv_from_name(vg.hdlr, name)
            if not bool(self._hdlr):
                raise StorLeverError('No LV {0} under VG {1}'.format(name, vg.name))
        elif uuid:
            self._hdlr = lvm_pv_from_uuid(vg.hdlr, uuid)
            if not bool(self._hdlr):
                raise StorLeverError('No LV {0} under VG {1}'.format(uuid, vg.name))
        else:
            raise StorLeverError('No valid parameter given to get a LV handler')
        self.name = self.get_name()
        self.uuid = self.get_uuid()
        self.size = self.get_size()
        self.free = self.get_free_size()

    def get_name(self):
        return lvm_pv_get_name(self._hdlr)

    def get_uuid(self):
        return lvm_pv_get_uuid(self._hdlr)

    def get_size(self):
        return lvm_pv_get_size(self._hdlr)

    def get_free_size(self):
        return lvm_pv_get_free(self._hdlr)

    def delete(self):
        self._vg.remove_pv(self.name)


class LVM(object):
    def __init__(self):
        self.vgs = {}
        with _LVM() as _lvm:
            for vg_name in _lvm.list_vg_names():
                self.vgs[vg_name] = VG(self, vg_name)

    def new_vg(self, vg_name, devices, pe_size=64):
        if vg_name in self.vgs:
            raise StorLeverError('VG {0} already exists'.format(vg_name))
        # TODO more check
        with _LVM() as _lvm:
            _lvm.create_vg(vg_name, devices, pe_size=pe_size)
        self.vgs[vg_name] = VG(self, vg_name)
        return self.vgs[vg_name]

    def refresh(self):
        with _LVM() as _lvm:
            for vg_name in _lvm.list_vg_names():
                self.vgs[vg_name] = VG(self, vg_name)


class VG(object):
    def __init__(self, lvm, name):
        self.lvm = lvm
        with _LVM() as _lvm:
            with _VG(_lvm, name) as _vg:
                self.name = _vg.name
                self.uuid = _vg.get_uuid()
                self.size = _vg.get_size()
                self.free_size = _vg.get_free_size()

    @DeferAndCache
    def pvs(self):
        pvs = {}
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                for _pv in _vg.iter_pv():
                    pvs[_pv.name] = PV(self, _pv.name, _pv.uuid, _pv.size)
        return pvs

    @DeferAndCache
    def lvs(self):
        lvs = {}
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                for _lv in _vg.iter_lv():
                    lvs[_lv.name] = LV(self, _lv.name, _lv.uuid, _lv.size)
        return lvs

    def _get_detail(self):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                self.__dict__['extent_size'] = _vg.get_extent_size()
                self.__dict__['extent_count'] = _vg.get_extent_count()
                self.__dict__['free_extent_count'] = _vg.get_free_extent_count()
                self.__dict__['pv_count'] = _vg.get_pv_count()
                self.__dict__['max_pv'] = _vg.get_max_pv()
                self.__dict__['max_lv'] = _vg.get_max_lv()

    @DeferAndCache
    def extent_size(self):
        self._get_detail()
        return self.extent_size

    @DeferAndCache
    def extent_count(self):
        self._get_detail()
        return self.extent_count

    @DeferAndCache
    def free_extent_count(self):
        self._get_detail()
        return self.free_extent_count

    @DeferAndCache
    def pv_count(self):
        self._get_detail()
        return self.pv_count

    @DeferAndCache
    def max_pv(self):
        self._get_detail()
        return self.max_pv

    @DeferAndCache
    def max_lv(self):
        self._get_detail()
        return self.max_lv

    def get_pv(self, pv_name):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                return _vg.get_pv_by_name(pv_name)

    def delete(self):
        pvs = self.pvs
        with _LVM() as _lvm:
            _lvm.delete_vg(self.name)
        self.lvm.vgs.pop(self.name, None)
        for pv in self.pvs.itervalues():
            pv.delete()

    def create_lv(self, lv_name, size):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name, mode=_VG.MODE_WRITE) as _vg:
                _lv = _vg.create_lv(lv_name, size)
                lv = LV(self, _lv.name, _lv.uuid, _lv.size)
        self.lvs[lv_name] = lv
        return lv

    def grow(self, device):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name, mode=_VG.MODE_WRITE) as _vg:
                _vg.add_pv(device)
                pv = _vg.get_pv_by_name(device)
        self.pvs[device] = pv

    def shrink(self, device):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name, mode=_VG.MODE_WRITE) as _vg:
                _vg.remove_pv(device)
        self.pvs.pop(device, None)

    def replace_pv(self):
        pass

    def get_lv(self, lv_name):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                _lv = _vg.get_lv_by_name(lv_name)
                return LV(self, _lv.name, _lv.uuid, _lv.size)

    def get_pv(self, pv_name):
        with _LVM() as _lvm:
            with _VG(_lvm, self.name) as _vg:
                _pv = _vg.get_pv_by_name(pv_name)
                return PV(self, _pv.name, _pv.uuid, _pv.size)


class PV(object):
    def __init__(self, vg, name, uuid, size):
        self.vg = vg
        self.name = name
        self.uuid = uuid
        self.size = size

    def delete(self):
        with _LVM() as _lvm:
            _lvm.remove_pv(self.name)


class LV(object):
    def __init__(self, vg, name, uuid, size):
        self.vg = vg
        self.name = name
        self.uuid = uuid
        self.size = size
        pass

    def resize(self, size):
        with _LVM() as _lvm:
            with _VG(_lvm, self.vg.name) as _vg:
                _vg.get_lv_by_name(self.name).resize(size)
                size = _vg.get_lv_by_name(self.name).get_size()
        self.size = size

    def delete(self):
        with _LVM() as _lvm:
            with _VG(_lvm, self.vg.name, mode=_VG.MODE_WRITE) as _vg:
                _vg.get_lv_by_name(self.name).delete()
        self.vg.lvs.pop(self.name, None)


ModuleManager.register_module(**MODULE_INFO)