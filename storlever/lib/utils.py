
"""
storlever.lib.utils
~~~~~~~~~~~~~~~~

This module provide some utils function for storlever lib

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import json


def filter_dict(d, keys, invert=False):
    """ Filters a dict by only permitting certain keys. """
    if invert:
        key_set = set(d.keys()) - set(keys)
    else:
        key_set = set(keys) & set(d.keys())
    return dict([ (k, d[k]) for k in key_set ])


class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        # dirty hack to keep 'default' method intact
        kwargs.pop('default', None)
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            if isinstance(o, set):
                return list(o)
            elif hasattr(o, '__json__'):
                return o.__json__()
            elif hasattr(o, '__dict__'):
                obj_dict = {}
                for k, v in o.__dict__.iteritems():
                    if not k.startswith('_'):
                        obj_dict[k] = v
                return obj_dict


def encode_json(o):
    return json.dumps(o, check_circular=True, cls=CustomJSONEncoder)




