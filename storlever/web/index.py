"""
storlever.web.index
~~~~~~~~~~~~~~~~

This module implements index web page of storlever

:copyright: (c) 2014 by OpenSight (opensight.com.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import platform




from storlever.rest.common import get_view, post_view, put_view, delete_view

from storlever.lib.exception import StorLeverError


def includeme(config):
    config.add_route('root', '/')


@get_view(route_name='root', permission="web", renderer='storlever:templates/index.pt')
def index_get(request):
    session = request.session
    print session.new
    if session.new:
        session["login"] = "admin"

    return {"project": "storlever"}

