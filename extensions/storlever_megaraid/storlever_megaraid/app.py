"""
storlever_megaraid.app
~~~~~~~~~~~~~~~~

storlever_megaraid's main file to extend the rest api of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

def main(config):

    # route and view configuration of REST API version 1 can be found in module storlever_megaraid.rest
    # check storlever_megaraid.rest.__init__.py for more detail
    config.include('storlever_megaraid.rest', route_prefix='storlever/api/v1')



