"""
storlever.mngr.block.lvm.lvm2app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ctypes binding of liblvm2app.so.
Most of codes are copy from project lvm2py https://github.com/xzased/lvm2py

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from ctypes.util import find_library
from ctypes import *
from storlever.lib.exception import StorLeverError


lib = find_library("lvm2app")

if not lib:
    raise Exception("LVM library not found.")

def raise_not_supported(*args, **kwargs):
    raise StorLeverError('function Not supported')

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


class lvm_property_value_union(Union):
    _field_ = [
        ('string', c_char_p),
        ('integer', c_ulonglong),
    ]


class lvm_property_value(Structure):
    #_field_ = [
    #    ('is_settable', c_uint),
        #('is_string', c_uint, 1),
        #('is_integer', c_uint, 1),
        #('is_valid', c_uint, 1),
        #('padding', c_uint, 28),
        #('value', lvm_property_value_union),
    #]
    pass

# Initialize library
try:
    lvm_init = lvmlib.lvm_init
    lvm_init.argtypes = [c_char_p]
    lvm_init.restype = lvm_t
except Exception:
    lvm_init = raise_not_supported

# some stuff
try:
    version = lvmlib.lvm_library_get_version
    version.restype = c_char_p
except Exception:
    version = raise_not_supported
try:
    lvm_quit = lvmlib.lvm_quit
    lvm_quit.argtypes = [lvm_t]
    lvm_quit.restype = None
except Exception:
    lvm_quit = raise_not_supported
try:
    lvm_scan = lvmlib.lvm_scan
    lvm_scan.argtypes = [lvm_t]
except Exception:
    lvm_scan = raise_not_supported
try:
    lvm_list_vg_names = lvmlib.lvm_list_vg_names
    lvm_list_vg_names.argtypes = [lvm_t]
    lvm_list_vg_names.restype = POINTER(dm_list)
except Exception:
    lvm_list_vg_names = raise_not_supported

# error
try:
    lvm_errno = lvmlib.lvm_errno
    lvm_errno.argtypes = [lvm_t]
except Exception:
    lvm_errno = raise_not_supported
try:
    lvm_errmsg = lvmlib.lvm_errmsg
    lvm_errmsg.argtypes = [lvm_t]
    lvm_errmsg.restype = c_char_p
except Exception:
    lvm_errmsg = raise_not_supported

try:
    dm_list_empty = lvmlib.dm_list_empty
    dm_list_empty.argtypes = [POINTER(dm_list)]
except Exception:
    dm_list_empty = raise_not_supported
try:
    dm_list_start = lvmlib.dm_list_start
    dm_list_start.argtypes = [POINTER(dm_list), POINTER(dm_list)]
except Exception:
    dm_list_start = raise_not_supported
try:
    dm_list_end = lvmlib.dm_list_end
    dm_list_end.argtypes = [POINTER(dm_list), POINTER(dm_list)]
except Exception:
    dm_list_end = raise_not_supported
try:
    dm_list_first = lvmlib.dm_list_first
    dm_list_first.argtypes = [POINTER(dm_list)]
    dm_list_first.restype = POINTER(dm_list)
except Exception:
    dm_list_first = raise_not_supported
try:
    dm_list_next = lvmlib.dm_list_next
    dm_list_next.argtypes = [POINTER(dm_list), POINTER(dm_list)]
    dm_list_next.restype = POINTER(dm_list)
except Exception:
    dm_list_next = raise_not_supported

# VG Functions
try:
    lvm_vg_create = lvmlib.lvm_vg_create
    lvm_vg_create.argtypes = [lvm_t, c_char_p]
    lvm_vg_create.restype = vg_t
except Exception:
    lvm_vg_create = raise_not_supported
try:
    lvm_vg_open = lvmlib.lvm_vg_open
    lvm_vg_open.argtypes = [lvm_t, c_char_p, c_char_p]
    lvm_vg_open.restype = vg_t
except Exception:
    lvm_vg_open = raise_not_supported
try:
    lvm_vg_write = lvmlib.lvm_vg_write
    lvm_vg_write.argtypes = [vg_t]
except Exception:
    lvm_vg_write = raise_not_supported
try:
    lvm_vg_remove = lvmlib.lvm_vg_remove
    lvm_vg_remove.argtypes = [vg_t]
except Exception:
    lvm_vg_remove = raise_not_supported
try:
    lvm_vg_close = lvmlib.lvm_vg_close
    lvm_vg_close.argtypes = [vg_t]
except Exception:
    lvm_vg_close = raise_not_supported
try:
    lvm_vg_extend = lvmlib.lvm_vg_extend
    lvm_vg_extend.argtypes = [vg_t, c_char_p]
except Exception:
    lvm_vg_extend = raise_not_supported
try:
    lvm_vg_reduce = lvmlib.lvm_vg_reduce
    lvm_vg_reduce.argtypes = [vg_t, c_char_p]
except Exception:
    lvm_vg_reduce = raise_not_supported
try:
    lvm_vg_get_uuid = lvmlib.lvm_vg_get_uuid
    lvm_vg_get_uuid.argtypes = [vg_t]
    lvm_vg_get_uuid.restype = c_char_p
except Exception:
    lvm_vg_get_uuid = raise_not_supported
try:
    lvm_vg_get_name = lvmlib.lvm_vg_get_name
    lvm_vg_get_name.argtypes = [vg_t]
    lvm_vg_get_name.restype = c_char_p
except Exception:
    lvm_vg_get_name = raise_not_supported
try:
    lvm_vg_get_size = lvmlib.lvm_vg_get_size
    lvm_vg_get_size.argtypes = [vg_t]
    lvm_vg_get_size.restype = c_ulonglong
except Exception:
    lvm_vg_get_size = raise_not_supported
try:
    lvm_vg_get_free_size = lvmlib.lvm_vg_get_free_size
    lvm_vg_get_free_size.argtypes = [vg_t]
    lvm_vg_get_free_size.restype = c_ulonglong
except Exception:
    lvm_vg_get_free_size = raise_not_supported
try:
    lvm_vg_get_extent_size = lvmlib.lvm_vg_get_extent_size
    lvm_vg_get_extent_size.argtypes = [vg_t]
    lvm_vg_get_extent_size.restype = c_ulonglong
except Exception:
    lvm_vg_get_extent_size = raise_not_supported
try:
    lvm_vg_get_extent_count = lvmlib.lvm_vg_get_extent_count
    lvm_vg_get_extent_count.argtypes = [vg_t]
    lvm_vg_get_extent_count.restype = c_ulonglong
except Exception:
    lvm_vg_get_extent_count = raise_not_supported
try:
    lvm_vg_get_free_extent_count = lvmlib.lvm_vg_get_free_extent_count
    lvm_vg_get_free_extent_count.argtypes = [vg_t]
    lvm_vg_get_free_extent_count.restype = c_ulonglong
except Exception:
    lvm_vg_get_free_extent_count = raise_not_supported
try:
    lvm_vg_get_pv_count = lvmlib.lvm_vg_get_pv_count
    lvm_vg_get_pv_count.argtypes = [vg_t]
    lvm_vg_get_pv_count.restype = c_ulonglong
except Exception:
    lvm_vg_get_pv_count = raise_not_supported
try:
    lvm_vg_get_max_pv = lvmlib.lvm_vg_get_max_pv
    lvm_vg_get_max_pv.argtypes = [vg_t]
    lvm_vg_get_max_pv.restype = c_ulonglong
except Exception:
    lvm_vg_get_max_pv = raise_not_supported
try:
    lvm_vg_get_max_lv = lvmlib.lvm_vg_get_max_lv
    lvm_vg_get_max_lv.argtypes = [vg_t]
    lvm_vg_get_max_lv.restype = c_ulonglong
except Exception:
    lvm_vg_get_max_lv = raise_not_supported
try:
    lvm_vgname_from_device = lvmlib.lvm_vgname_from_device
    lvm_vgname_from_device.argtypes = [vg_t, c_char_p]
    lvm_vgname_from_device.restype = c_char_p
except Exception:
    lvm_vgname_from_device = raise_not_supported
try:
    lvm_vg_list_pvs = lvmlib.lvm_vg_list_pvs
    lvm_vg_list_pvs.argtypes = [vg_t]
    lvm_vg_list_pvs.restype = POINTER(dm_list)
except Exception:
    lvm_vg_list_pvs = raise_not_supported
try:
    lvm_vg_list_lvs = lvmlib.lvm_vg_list_lvs
    lvm_vg_list_lvs.argtypes = [vg_t]
    lvm_vg_list_lvs.restype = POINTER(dm_list)
except Exception:
    lvm_vg_list_lvs = raise_not_supported
try:
    lvm_vg_create_lv_linear = lvmlib.lvm_vg_create_lv_linear
    lvm_vg_create_lv_linear.argtypes = [vg_t, c_char_p, c_ulonglong]
    lvm_vg_create_lv_linear.restype = lv_t
except Exception:
    lvm_vg_create_lv_linear = raise_not_supported
try:
    lvm_vg_remove_lv = lvmlib.lvm_vg_remove_lv
    lvm_vg_remove_lv.argtypes = [lv_t]
except Exception:
    lvm_vg_remove_lv = raise_not_supported
try:
    lvm_vg_set_extent_size = lvmlib.lvm_vg_set_extent_size
    lvm_vg_set_extent_size.argtypes = [vg_t, c_ulong]
except Exception:
    lvm_vg_set_extent_size = raise_not_supported
try:
    lvm_vg_is_clustered = lvmlib.lvm_vg_is_clustered
    lvm_vg_is_clustered.argtypes = [vg_t]
except Exception:
    lvm_vg_is_clustered = raise_not_supported
try:
    lvm_vg_is_exported = lvmlib.lvm_vg_is_exported
    lvm_vg_is_exported.argtypes = [vg_t]
except Exception:
    lvm_vg_is_exported = raise_not_supported
try:
    lvm_vg_is_partial = lvmlib.lvm_vg_is_partial
    lvm_vg_is_partial.argtypes = [vg_t]
except Exception:
    lvm_vg_is_partial = raise_not_supported
try:
    lvm_vg_get_seqno = lvmlib.lvm_vg_get_seqno
    lvm_vg_get_seqno.argtypes = [vg_t]
    lvm_vg_get_seqno.restype = c_ulonglong
except Exception:
    lvm_vg_get_seqno = raise_not_supported

# PV Functions
try:
    lvm_pv_create = lvmlib.lvm_pv_create
    lvm_pv_create.argtypes = [lvm_t, c_char_p, c_uint64]
except Exception:
    lvm_pv_create = raise_not_supported
try:
    lvm_pv_get_name = lvmlib.lvm_pv_get_name
    lvm_pv_get_name.argtypes = [pv_t]
    lvm_pv_get_name.restype = c_char_p
except Exception:
    lvm_pv_get_name = raise_not_supported
try:
    lvm_pv_get_uuid = lvmlib.lvm_pv_get_uuid
    lvm_pv_get_uuid.argtypes = [pv_t]
    lvm_pv_get_uuid.restype = c_char_p
except Exception:
    lvm_pv_get_uuid = raise_not_supported
try:
    lvm_pv_get_mda_count = lvmlib.lvm_pv_get_mda_count
    lvm_pv_get_mda_count.argtypes = [pv_t]
    lvm_pv_get_mda_count.restype = c_ulonglong
except Exception:
    lvm_pv_get_mda_count = raise_not_supported
try:
    lvm_pv_get_dev_size = lvmlib.lvm_pv_get_dev_size
    lvm_pv_get_dev_size.argtypes = [pv_t]
    lvm_pv_get_dev_size.restype = c_ulonglong
except Exception:
    lvm_pv_get_dev_size = raise_not_supported
try:
    lvm_pv_get_size = lvmlib.lvm_pv_get_size
    lvm_pv_get_size.argtypes = [pv_t]
    lvm_pv_get_size.restype = c_ulonglong
except Exception:
    lvm_pv_get_size = raise_not_supported
try:
    lvm_pv_get_free = lvmlib.lvm_pv_get_free
    lvm_pv_get_free.argtypes = [pv_t]
    lvm_pv_get_free.restype = c_ulonglong
except Exception:
    lvm_pv_get_free = raise_not_supported
try:
    lvm_pv_from_uuid = lvmlib.lvm_pv_from_uuid
    lvm_pv_from_uuid.argtypes = [vg_t, c_char_p]
    lvm_pv_from_uuid.restype = pv_t
except Exception:
    lvm_pv_from_uuid = raise_not_supported
try:
    lvm_pv_from_name = lvmlib.lvm_pv_from_name
    lvm_pv_from_name.argtypes = [vg_t, c_char_p]
    lvm_pv_from_name.restype = pv_t
except Exception:
    lvm_pv_from_name = raise_not_supported
try:
    lvm_pv_remove = lvmlib.lvm_pv_remove
    lvm_pv_remove.argtypes = [lvm_t, c_char_p]
except Exception:
    lvm_pv_remove = raise_not_supported
try:
    lvm_pv_resize = lvmlib.lvm_pv_resize
    lvm_pv_resize.argtypes = [pv_t, c_uint64]
except Exception:
    lvm_pv_resize = raise_not_supported

# LV Functions
try:
    lvm_lv_get_name = lvmlib.lvm_lv_get_name
    lvm_lv_get_name.argtypes = [lv_t]
    lvm_lv_get_name.restype = c_char_p
except Exception:
    lvm_lv_get_name = raise_not_supported
try:
    lvm_lv_get_uuid = lvmlib.lvm_lv_get_uuid
    lvm_lv_get_uuid.argtypes = [lv_t]
    lvm_lv_get_uuid.restype = c_char_p
except Exception:
    lvm_lv_get_uuid = raise_not_supported
try:
    lvm_lv_get_size = lvmlib.lvm_lv_get_size
    lvm_lv_get_size.argtypes = [lv_t]
    lvm_lv_get_size.restype = c_ulonglong
except Exception:
    lvm_lv_get_size = raise_not_supported
try:
    lvm_lv_get_attr = lvmlib.lvm_lv_get_attr
    lvm_lv_get_attr.argtypes = [lv_t]
    lvm_lv_get_attr.restype = c_char_p
except Exception:
    lvm_lv_get_attr = raise_not_supported
try:
    lvm_lv_get_origin = lvmlib.lvm_lv_get_origin
    lvm_lv_get_origin.argtypes = [lv_t]
    lvm_lv_get_origin.restype = c_char_p
except Exception:
    lvm_lv_get_origin = raise_not_supported
try:
    lvm_lv_snapshot = lvmlib.lvm_lv_snapshot
    lvm_lv_snapshot.argtypes = [lv_t, c_char_p, c_ulonglong]
    lvm_lv_snapshot.restype = lv_t
except Exception:
    lvm_lv_snapshot = raise_not_supported
try:
    lvm_lv_is_active = lvmlib.lvm_lv_is_active
    lvm_lv_is_active.argtypes = [lv_t]
    lvm_lv_is_active.restype = c_ulonglong
except Exception:
    lvm_lv_is_active = raise_not_supported
try:
    lvm_lv_is_suspended = lvmlib.lvm_lv_is_suspended
    lvm_lv_is_suspended.argtypes = [lv_t]
    lvm_lv_is_suspended.restype = c_ulonglong
except Exception:
    lvm_lv_is_suspended = raise_not_supported
try:
    lvm_lv_activate = lvmlib.lvm_lv_activate
    lvm_lv_activate.argtypes = [lv_t]
except Exception:
    lvm_lv_activate = raise_not_supported
try:
    lvm_lv_deactivate = lvmlib.lvm_lv_deactivate
    lvm_lv_deactivate.argtypes = [lv_t]
except Exception:
    lvm_lv_deactivate = raise_not_supported
try:
    lvm_lv_resize = lvmlib.lvm_lv_resize
    lvm_lv_resize.argtypes = [lv_t, c_ulonglong]
except Exception:
    lvm_lv_resize = raise_not_supported
try:
    lvm_lv_from_uuid = lvmlib.lvm_lv_from_uuid
    lvm_lv_from_uuid.argtypes = [vg_t, c_char_p]
    lvm_lv_from_uuid.restype = lv_t
except Exception:
    lvm_lv_from_uuid = raise_not_supported
try:
    lvm_lv_from_name = lvmlib.lvm_lv_from_name
    lvm_lv_from_name.argtypes = [vg_t, c_char_p]
    lvm_lv_from_name.restype = lv_t
except Exception:
    lvm_lv_from_name = raise_not_supported
try:
    lvm_lv_get_property = lvmlib.lvm_lv_get_property
    lvm_lv_get_property.argtypes = [lv_t, c_char_p]
    #lvm_lv_get_property.restype = lvm_property_value
except Exception:
    lvm_lv_get_property = raise_not_supported



