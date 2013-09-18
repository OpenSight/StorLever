"""
storlever.common
~~~~~~~~~~~~~~~~

This module implements some common API for REST.

:copyright: (c) 2013 by Yiting Huang.
:license: GPLv3, see LICENSE for more details.

"""
import sys
import traceback

import pyramid.exceptions
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.events import subscriber, NewResponse

from storlever.lib.schema import SchemaError as ValidationFailure
from storlever.lib.exception import StorLeverError


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


@view_config(context=ValidationFailure)
def failed_validation(exc, request):
    response = Response('Failed validation: %s' % exc.code)
    response.status_int = 400
    return {'info': str(exc), 'traceback': []}


@view_config(context=StorLeverError)
def storlever_error_view(exc, request):
    response = request.response
    response.status_int = exc.http_status_code
    tb_list = traceback.format_list(traceback.extract_tb(sys.exc_traceback)[-5:])
    return {'info': str(exc), 'traceback': tb_list}


@view_config(context=Exception)
def error_view(exc, request):
    response = request.response
    response.status_int = exc.http_status_code
    tb_list = traceback.format_list(traceback.extract_tb(sys.exc_traceback)[-5:])
    return {'info': str(exc), 'traceback': tb_list}


@view_config(context=pyramid.exceptions.NotFound)
def not_found_view(exc, request):
    response = request.response
    response.status_int = exc.status_code
    return {'info': 'Resource {} not found or method {} not supported'.format(request.path, request.method),
            'traceback': []}


@subscriber(NewResponse)
def add_response_header(event):
    """
    add all custom header here
    """
    response = event.response
    response.headers['X-Powered-By'] = 'Pyramid framework'
