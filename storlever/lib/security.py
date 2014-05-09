"""
storlever.lib.secucrity
~~~~~~~~~~~~~~~~

This module implements some security configuration for storlever.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""


from pyramid.security import Allow, Everyone, Authenticated, DENY_ALL


class AclRootFactory(object):
    __acl__ = [ (Allow, Everyone, 'api'),
                (Allow, Authenticated, 'web'),
                DENY_ALL]
    def __init__(self, request):
        pass