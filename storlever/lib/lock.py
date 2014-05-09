"""
storlever.lib.lock
~~~~~~~~~~~~~~~~

This module implements lock mechanism for storlever.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

from threading import Lock as threading_Lock


storlever_lock_factory = threading_Lock   # default is threading.Lock


def set_lock_factory(lock_factory):
    """set lock factory for storlever

    This lock should has a context interface(support "with")


    """
    global storlever_lock_factory
    storlever_lock_factory = lock_factory


def set_lock_factory_from_name(module_path_name, factory_func_name):
    """another version of set_lock_factory

    use the module name the function name instead of the function object
    """
    global storlever_lock_factory
    storlever_lock_factory = \
        getattr(__import__(module_path_name, fromlist=[factory_func_name]),
                factory_func_name)


def lock():
    """return a lock object support context for storlever"""
    return storlever_lock_factory()