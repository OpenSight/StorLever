"""
storlever.mngr.block.lvm.lvm2app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ctypes binding of liblvm2app.so.
Most of codes are copy from project lvm2py https://github.com/xzased/lvm2py

:copyright: (c) 2014 by OpenSight (opensight.com.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from ctypes.util import find_library
from ctypes import *


lib = find_library("lvm2app")

if not lib:
    raise Exception("LVM library not found.")

lvmlib = CDLL(lib)

class lvm(Structure):
    pass

lvm_t = POINTER(lvm)

class volume_group(Structure):
    pass

vg_t = POINTER(volume_group)

class physical_volume(Structure):
    pass

pv_t = POINTER(physical_volume)

class logical_volume(Structure):
    pass

lv_t = POINTER(logical_volume)

class dm_list(Structure):
    pass

dm_list._fields_ = [('p', POINTER(dm_list)), ('n', POINTER(dm_list))]

class lvm_str_list(Structure):
    _fields_ = [
        ('list', dm_list),
        ('str', c_char_p),
        ]

lvm_str_list_t = lvm_str_list

class lvm_pv_list(Structure):
    _fields_ = [
        ('list', dm_list),
        ('pv', pv_t),
        ]

lvm_pv_list_t = lvm_pv_list

class lvm_lv_list(Structure):
    _fields_ = [
        ('list', dm_list),
        ('lv', lv_t),
        ]

lvm_lv_list_t = lvm_lv_list

# Initialize library
lvm_init = lvmlib.lvm_init
lvm_init.argtypes = [c_char_p]
lvm_init.restype = lvm_t

# some stuff
version = lvmlib.lvm_library_get_version
version.restype = c_char_p
lvm_quit = lvmlib.lvm_quit
lvm_quit.argtypes = [lvm_t]
lvm_quit.restype = None
lvm_scan = lvmlib.lvm_scan
lvm_scan.argtypes = [lvm_t]
lvm_list_vg_names = lvmlib.lvm_list_vg_names
lvm_list_vg_names.argtypes = [lvm_t]
lvm_list_vg_names.restype = POINTER(dm_list)

# error
lvm_errno = lvmlib.lvm_errno
lvm_errno.argtypes = [lvm_t]
lvm_errmsg = lvmlib.lvm_errmsg
lvm_errmsg.argtypes = [lvm_t]
lvm_errmsg.restype = c_char_p

dm_list_empty = lvmlib.dm_list_empty
dm_list_empty.argtypes = [POINTER(dm_list)]
dm_list_start = lvmlib.dm_list_start
dm_list_start.argtypes = [POINTER(dm_list), POINTER(dm_list)]
dm_list_end = lvmlib.dm_list_end
dm_list_end.argtypes = [POINTER(dm_list), POINTER(dm_list)]
dm_list_first = lvmlib.dm_list_first
dm_list_first.argtypes = [POINTER(dm_list)]
dm_list_first.restype = POINTER(dm_list)
dm_list_next = lvmlib.dm_list_next
dm_list_next.argtypes = [POINTER(dm_list), POINTER(dm_list)]
dm_list_next.restype = POINTER(dm_list)

# VG Functions
lvm_vg_create = lvmlib.lvm_vg_create
lvm_vg_create.argtypes = [lvm_t, c_char_p]
lvm_vg_create.restype = vg_t
lvm_vg_open = lvmlib.lvm_vg_open
lvm_vg_open.argtypes = [lvm_t, c_char_p, c_char_p]
lvm_vg_open.restype = vg_t
lvm_vg_write = lvmlib.lvm_vg_write
lvm_vg_write.argtypes = [vg_t]
lvm_vg_remove = lvmlib.lvm_vg_remove
lvm_vg_remove.argtypes = [vg_t]
lvm_vg_close = lvmlib.lvm_vg_close
lvm_vg_close.argtypes = [vg_t]
lvm_vg_extend = lvmlib.lvm_vg_extend
lvm_vg_extend.argtypes = [vg_t, c_char_p]
lvm_vg_reduce = lvmlib.lvm_vg_reduce
lvm_vg_reduce.argtypes = [vg_t, c_char_p]
lvm_vg_get_uuid = lvmlib.lvm_vg_get_uuid
lvm_vg_get_uuid.argtypes = [vg_t]
lvm_vg_get_uuid.restype = c_char_p
lvm_vg_get_name = lvmlib.lvm_vg_get_name
lvm_vg_get_name.argtypes = [vg_t]
lvm_vg_get_name.restype = c_char_p
lvm_vg_get_size = lvmlib.lvm_vg_get_size
lvm_vg_get_size.argtypes = [vg_t]
lvm_vg_get_size.restype = c_ulonglong
lvm_vg_get_free_size = lvmlib.lvm_vg_get_free_size
lvm_vg_get_free_size.argtypes = [vg_t]
lvm_vg_get_free_size.restype = c_ulonglong
lvm_vg_get_extent_size = lvmlib.lvm_vg_get_extent_size
lvm_vg_get_extent_size.argtypes = [vg_t]
lvm_vg_get_extent_size.restype = c_ulonglong
lvm_vg_get_extent_count = lvmlib.lvm_vg_get_extent_count
lvm_vg_get_extent_count.argtypes = [vg_t]
lvm_vg_get_extent_count.restype = c_ulonglong
lvm_vg_get_free_extent_count = lvmlib.lvm_vg_get_free_extent_count
lvm_vg_get_free_extent_count.argtypes = [vg_t]
lvm_vg_get_free_extent_count.restype = c_ulonglong
lvm_vg_get_pv_count = lvmlib.lvm_vg_get_pv_count
lvm_vg_get_pv_count.argtypes = [vg_t]
lvm_vg_get_pv_count.restype = c_ulonglong
lvm_vg_get_max_pv = lvmlib.lvm_vg_get_max_pv
lvm_vg_get_max_pv.argtypes = [vg_t]
lvm_vg_get_max_pv.restype = c_ulonglong
lvm_vg_get_max_lv = lvmlib.lvm_vg_get_max_lv
lvm_vg_get_max_lv.argtypes = [vg_t]
lvm_vg_get_max_lv.restype = c_ulonglong
lvm_vgname_from_device = lvmlib.lvm_vgname_from_device
lvm_vgname_from_device.argtypes = [vg_t, c_char_p]
lvm_vgname_from_device.restype = c_char_p
lvm_vg_list_pvs = lvmlib.lvm_vg_list_pvs
lvm_vg_list_pvs.argtypes = [vg_t]
lvm_vg_list_pvs.restype = POINTER(dm_list)
lvm_vg_list_lvs = lvmlib.lvm_vg_list_lvs
lvm_vg_list_lvs.argtypes = [vg_t]
lvm_vg_list_lvs.restype = POINTER(dm_list)
lvm_vg_create_lv_linear = lvmlib.lvm_vg_create_lv_linear
lvm_vg_create_lv_linear.argtypes = [vg_t, c_char_p, c_ulonglong]
lvm_vg_create_lv_linear.restype = lv_t
lvm_vg_remove_lv = lvmlib.lvm_vg_remove_lv
lvm_vg_remove_lv.argtypes = [lv_t]
lvm_vg_set_extent_size = lvmlib.lvm_vg_set_extent_size
lvm_vg_set_extent_size.argtypes = [vg_t, c_ulong]
lvm_vg_is_clustered = lvmlib.lvm_vg_is_clustered
lvm_vg_is_clustered.argtypes = [vg_t]
lvm_vg_is_exported = lvmlib.lvm_vg_is_exported
lvm_vg_is_exported.argtypes = [vg_t]
lvm_vg_is_partial = lvmlib.lvm_vg_is_partial
lvm_vg_is_partial.argtypes = [vg_t]
lvm_vg_get_seqno = lvmlib.lvm_vg_get_seqno
lvm_vg_get_seqno.argtypes = [vg_t]
lvm_vg_get_seqno.restype = c_ulonglong

# PV Functions
lvm_pv_create = lvmlib.lvm_pv_create
lvm_pv_create.argtypes = [lvm_t, c_char_p, c_uint64]
lvm_pv_get_name = lvmlib.lvm_pv_get_name
lvm_pv_get_name.argtypes = [pv_t]
lvm_pv_get_name.restype = c_char_p
lvm_pv_get_uuid = lvmlib.lvm_pv_get_uuid
lvm_pv_get_uuid.argtypes = [pv_t]
lvm_pv_get_uuid.restype = c_char_p
lvm_pv_get_mda_count = lvmlib.lvm_pv_get_mda_count
lvm_pv_get_mda_count.argtypes = [pv_t]
lvm_pv_get_mda_count.restype = c_ulonglong
lvm_pv_get_dev_size = lvmlib.lvm_pv_get_dev_size
lvm_pv_get_dev_size.argtypes = [pv_t]
lvm_pv_get_dev_size.restype = c_ulonglong
lvm_pv_get_size = lvmlib.lvm_pv_get_size
lvm_pv_get_size.argtypes = [pv_t]
lvm_pv_get_size.restype = c_ulonglong
lvm_pv_get_free = lvmlib.lvm_pv_get_free
lvm_pv_get_free.argtypes = [pv_t]
lvm_pv_get_free.restype = c_ulonglong
lvm_pv_from_uuid = lvmlib.lvm_pv_from_uuid
lvm_pv_from_uuid.argtypes = [vg_t, c_char_p]
lvm_pv_from_uuid.restype = pv_t
lvm_pv_from_name = lvmlib.lvm_pv_from_name
lvm_pv_from_name.argtypes = [vg_t, c_char_p]
lvm_pv_from_name.restype = pv_t

# LV Functions
lvm_lv_get_name = lvmlib.lvm_lv_get_name
lvm_lv_get_name.argtypes = [lv_t]
lvm_lv_get_name.restype = c_char_p
lvm_lv_get_uuid = lvmlib.lvm_lv_get_uuid
lvm_lv_get_uuid.argtypes = [lv_t]
lvm_lv_get_uuid.restype = c_char_p
lvm_lv_get_size = lvmlib.lvm_lv_get_size
lvm_lv_get_size.argtypes = [lv_t]
lvm_lv_get_size.restype = c_ulonglong
lvm_lv_is_active = lvmlib.lvm_lv_is_active
lvm_lv_is_active.argtypes = [lv_t]
lvm_lv_is_active.restype = c_ulonglong
lvm_lv_is_suspended = lvmlib.lvm_lv_is_suspended
lvm_lv_is_suspended.argtypes = [lv_t]
lvm_lv_is_suspended.restype = c_ulonglong
lvm_lv_activate = lvmlib.lvm_lv_activate
lvm_lv_activate.argtypes = [lv_t]
lvm_lv_deactivate = lvmlib.lvm_lv_deactivate
lvm_lv_deactivate.argtypes = [lv_t]
lvm_lv_resize = lvmlib.lvm_lv_resize
lvm_lv_resize.argtypes = [lv_t, c_ulonglong]
lvm_lv_from_uuid = lvmlib.lvm_lv_from_uuid
lvm_lv_from_uuid.argtypes = [vg_t, c_char_p]
lvm_lv_from_uuid.restype = lv_t
lvm_lv_from_name = lvmlib.lvm_lv_from_name
lvm_lv_from_name.argtypes = [vg_t, c_char_p]
lvm_lv_from_name.restype = lv_t




