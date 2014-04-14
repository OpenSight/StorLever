import os.path
from lvm2app import *
from storlever.lib.exception import StorLeverError

class LVM(object):

    def __init__(self):
        self._hdlr = None

    def open(self):
        if self._hdlr is None:
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

    def raise_from_error(self, info=''):
        if self._hdlr is None:
            raise StorLeverError('')
        else:
            raise StorLeverError(info + '\n' + lvm_errmsg(self._hdlr))

    def _create_pv(self, device):
        if lvm_pv_create(self._hdlr, device, 0) != 0:
            self.raise_from_error(info='Can not create PV on {0}'.format(device))

    def create_vg(self, vg_name, devices=None, pe_size=None):
        """
        :param vg_name: string of volume group name
        :param devices: list of block names
        :param pe_size: integer in MB
        :return: None
        """
        # TODO maybe we need to check if block device in "devices" is already used
        if self._hdlr is None:
            raise Exception()
        vg_hdlr = lvm_vg_create(self._hdlr, vg_name)
        if not bool(vg_hdlr):
            self.raise_from_error()
        if pe_size:
            if pe_size > 4096:
                StorLeverError('PE too large')
            if lvm_vg_set_extent_size(vg_hdlr, pe_size*1024*1024) != 0:
                self.raise_from_error(info='Set physical extent size failed')
        for device in devices:
            if not os.path.exists(device):
                rc = lvm_vg_close(vg_hdlr)
                if rc != 0:
                    raise StorLeverError('close vg handler failed')
                raise StorLeverError('Not valid device {0}'.format(device))
            #self._create_pv(device)
            rc = lvm_vg_extend(vg_hdlr, device)
            if rc != 0:
                rc = lvm_vg_close(vg_hdlr)
                if rc != 0:
                    raise self.raise_from_error()
                raise self.raise_from_error()
            if lvm_vg_write(vg_hdlr) != 0:
                if lvm_vg_close(vg_hdlr) != 0:
                    raise self.raise_from_error('Failed to close VG handler')
                raise self.raise_from_error('Failed commit VG creation')
        if lvm_vg_close(vg_hdlr) != 0:
            raise self.raise_from_error('Failed to close VG handler')


class VGNew(object):
    def __init__(self, lvm_hdlr, name):
        self._lvm_hdlr = lvm_hdlr
        self._name = name

    def __enter__(self):
        hdlr = lvm_vg_create(self._lvm_hdlr, self._name)
        if not bool(hdlr):
            self.raise_from_error()
        return hdlr


class VG(object):
    def __init__(self, lvm_hdlr, name, new=False):
        self._lvm_hdlr = lvm_hdlr
        self._name = name
        self._hdlr = None
        self.name = ''
        self.pvs = []
        self.lvs = []
        self.size = 0
        self._new = new

    def __enter__(self):
        if self._new:
            self._hdlr = lvm_vg_create(self._lvm_hdlr, self._name)
            if not bool(self._hdlr):
                self.raise_from_error()
        else:
            self._hdlr = lvm_vg_open(self._lvm_hdlr, self._name, 'r', 0)
            if not bool(self._hdlr):
                self.raise_from_error()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if lvm_vg_close(self._hdlr) != 0:
            raise self.raise_from_error('Failed to close VG handler')

    @classmethod
    def new(cls, lvm_hdlr, name):
        return cls(lvm_hdlr, name, new=True)

    @property
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


