"""
storlever.lib.exception
~~~~~~~~~~~~~~~~~~~~~~~

This module defines the exception class which should be
sub-classed from by all other Exception used in StorLever project.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""


class StorLeverError(Exception):
    def __init__(self, info, http_status_code=500):
        super(StorLeverError, self).__init__(info)
        self.http_status_code = http_status_code

class StorLeverCmdError(StorLeverError):
    def __init__(self, return_code, info, http_status_code=500):
        super(StorLeverCmdError, self).__init__(info, http_status_code)
        self.return_code = return_code