"""
storlever.web.index
~~~~~~~~~~~~~~~~

This module implements index web page of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import hashlib
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from storlever.web.webconfig import WebPassword


from storlever.rest.common import get_view, post_view, put_view, delete_view

from storlever.lib.exception import StorLeverError


def includeme(config):
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


@view_config(route_name='login', renderer='storlever:templates/login.pt')
@forbidden_view_config(renderer='storlever:templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if WebPassword().check_passwd(login, password) is False:
            message = 'Failed login (username or password is wrong)'
        else:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        salt = 'OpenSight2013',
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.application_url,
                     headers = headers)

