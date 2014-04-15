import os.path
from functools import wraps
from lvm2app import *
from storlever.lib.exception import StorLeverError


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

    def _create_pv(self, device):
        if lvm_pv_create(self._hdlr, device, 0) != 0:
            self.raise_from_error(info='Can not create PV on {0}'.format(device))

    def create_vg(self, vg_name, devices=None, pe_size=64):
        """
        :param vg_name: string of volume group name
        :param devices: list of block names
        :param pe_size: integer in MB
        :return: None
        """
        # TODO maybe we need to check if block device in "devices" is already used
        if self._hdlr is None:
            raise StorLeverError('')

        with _VG(self, vg_name, mode=_VG.MODE_NEW) as vg:
            vg.set_extent_size(pe_size)
            for device in devices:
                vg.add_pv(device)

    def delete_vg(self, vg_name):
        with _VG(self, vg_name, mode=_VG.MODE_WRITE) as vg:
            vg.delete()

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

    def get_vg(self, name, mode=_VG.MODE_READ):
        return _VG(self, name, mode=mode)


class _VG(object):
    """
    For VG creation
    Used ONLY in with context, for example:
    with _VGNew(lvm, 'new_vg') as vg:
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
        self._name = name
        self._mode = mode
        if mode == self.MODE_READ:
            self._hdlr = lvm_vg_open(self._lvm.hdlr, self._name, 'r', 0)
        elif mode == self.MODE_WRITE:
            self._hdlr = lvm_vg_open(self._lvm.hdlr, self._name, 'w', 0)
        elif mode == self.MODE_NEW:
            self._hdlr = lvm_vg_create(self._lvm.hdlr, self._name)
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
            self._hdlr = lvm_vg_create(self._lvm_hdlr, self._name)
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
            self.raise_from_error('Failed to delete VG {0}'.format(self._name))


class VG(object):
    def __init__(self, lvm, name):
        self._lvm = lvm
        if not lvm or not lvm.hdlr:
            raise StorLeverError('')
        self._name = name
        self._hdlr = lvm_vg_open(self._lvm.hdlr, self._name, 'r', 0)
        if not bool(self._hdlr):
            self.raise_from_error()

    def raise_from_error(self, info=''):
        if not self._lvm or not self._lvm.hdlr:
            raise StorLeverError('')
        self._lvm.raise_from_error(info)

    def __enter__(self):
        if not self._hdlr:
            self._hdlr = lvm_vg_open(self._lvm.hdlr, self._name, 'r', 0)
            if not bool(self._hdlr):
                self.raise_from_error()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        hdlr, self._hdlr = self._hdlr, None
        if hdlr:
            if lvm_vg_close(hdlr) != 0:
                raise self.raise_from_error('Failed to close VG handler')

    def available_size(self):
        pass

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


class LV(object):
    def __init__(self):
        self.name = ''
        self.size = 0
        self.vg = None
        self.type = 'linear'
        self.stripe_size = 0
        self.stripe_number = 0
        self.mirror_number = 0

    def delete(self):
        pass

    def grow(self):
        pass

    def shrink(self):
        pass


