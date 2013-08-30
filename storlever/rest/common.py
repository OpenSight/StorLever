"""
storlever.common
~~~~~~~~~~~~~~~~

This module implements some common API for REST.

:copyright: (c) 2013 by Yiting Huang.
:license: GPLv3, see LICENSE for more details.

"""

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.events import subscriber, NewResponse

from storlever.lib.schema import SchemaError as ValidationFailure


class _rest_view(view_config):
    def __init__(self, **settings):
        method = self.__class__.__name__.split('_')[0].upper()
        super(_rest_view, self).__init__(request_method=method,
                                         **settings)


class get_view(_rest_view):
    pass


class post_view(_rest_view):
    pass


class put_view(_rest_view):
    pass


class delete_view(_rest_view):
    pass


class RestError(Exception):
    """ Exception for REST related error other than request validation Error
    Raise this error in REST request handling will cause pyramid to return JSON encoded error message like:
    {
        "message": "something failed",
        "code": 500
    }
    code in JSON is same as the returned HTTP status code, which can be given as status_code when raising error
    """
    def __init__(self, msg='REST request failed', status_code=500):
        self.msg = msg
        self.status_code = status_code


@view_config(context=ValidationFailure)
def failed_validation(exc, request):
    response = Response('Failed validation: %s' % exc.code)
    response.status_int = 400
    return response


@view_config(context=RestError)
def failed_rest(exc, request):
    response = request.response
    response.status_int = exc.status_code
    return {'code': exc.status_code, 'message': exc.msg}


@subscriber(NewResponse)
def add_response_header(event):
    """
    add all custom header here
    """
    response = event.response
    response.headers['X-Powered-By'] = 'Pyramid framework'
