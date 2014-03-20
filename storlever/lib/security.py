"""
storlever.lib.secucrity
~~~~~~~~~~~~~~~~

This module implements some security configuration for storlever.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""


from pyramid.security import Allow, Everyone, Authenticated, DENY_ALL


class AclRootFactory(object):
    __acl__ = [ (Allow, Everyone, 'api'),
                (Allow, Authenticated, 'web'),
                DENY_ALL]
    def __init__(self, request):
        pass