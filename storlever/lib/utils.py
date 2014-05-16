
"""
storlever.lib.utils
~~~~~~~~~~~~~~~~

This module provide some utils function for storlever lib

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

def filter_dict(d, keys, invert=False):
    """ Filters a dict by only permitting certain keys. """
    if invert:
        key_set = set(d.keys()) - set(keys)
    else:
        key_set = set(keys) & set(d.keys())
    return dict([ (k, d[k]) for k in key_set ])