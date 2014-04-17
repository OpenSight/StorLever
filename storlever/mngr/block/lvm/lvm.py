import os.path
from functools import wraps
from lvm2app import *
from storlever.lib.exception import StorLeverError


class DeferAndCache(object):
    """
    Used as a decorator to defer the calculation of object attribute's value
    util the first time it is accessed,
    and also cache the calculated value, so it will not be calculated again, once calculated
    """
    def __init__(self, calc_func):
        self._calc_func = calc_func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self._calc_func(instance)
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
    def get_lv_by_name(self, name):
        return _LV(self, name=name)

    def get_lv_by_uuid(self, uuid):
        return _LV(self, uuid=uuid)

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

    def get_name(self):
        return lvm_pv_get_name(self._hdlr)

    def get_uuid(self):
        return lvm_pv_get_uuid(self._hdlr)

    def get_size(self):
        return lvm_pv_get_size(self._hdlr)


class LVM(object):
    def __init__(self):
        self.vgs = {}
        with _LVM() as _lvm:
            for vg_name in _lvm.list_vg_names():
                self.vgs[vg_name] = None

    def get_vg(self, vg_name):
        if vg_name not in self.vgs:
            raise StorLeverError('No such VG', 404)

        if self.vgs[vg_name] is None:
            self.vgs[vg_name] = VG(vg_name)


class VG(object):
    def __init__(self, name):
        with _LVM() as _lvm:
            _vg = _VG(_lvm, name)
            self.name = _vg.name
            self.uuid = _vg.uuid
            self.size = _vg.size
        self._pvs = None
        self._lvs = None

    @property
    def pvs(self):
        if self._pvs is None:
            self._pvs = {}
            with _LVM() as _lvm:
                with _VG(_lvm, self.name) as _vg:
                    for _pv in _vg.iter_pv():
                        self._pvs[_pv.name] = PV(_pv.name)
        return self._pvs

    @property
    def lvs(self):
        if self._lvs is None:
            self._lvs = {}
            with _LVM() as _lvm:
                with _VG(_lvm, self.name) as _vg:
                    for _lv in _vg.iter_lv():
                        self._lvs[_lv.name] = LV(_lv.name)
        return self._lvs

    def check_detail(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._hdlr is None:
                raise StorLeverError('Empty VG handler, unable to process')
            return func(self, *args, **kwargs)
        return wrapper

    def delete(self):
        pass

    def create_lv(self):
        pass

    def delete_lv(self):
        pass

    def grow(self):
        pass

    def shrink(self):
        pass

    def replace_pv(self):
        pass


class PV(object):
    def __init__(self, name):
        self.name = name
        pass


class LV(object):
    def __init__(self, name):
        self.name = name
        pass


