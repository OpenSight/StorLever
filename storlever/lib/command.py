"""
storlever.lib.command
~~~~~~~~~~~~~~~~

This module implements command call for storlever.

:copyright: (c) 2013 by jk.
:license: GPLv3, see LICENSE for more details.

"""
import subprocess

import exception


def check_output(cmd, shell=False, input_ret=[]):
    """call the cmd and return output

     it's similar with subprocess.check_output except it would raise a
     StorLeverError instead of subprocess.CalledProcessError.

     StorLeverError's http_status_code is 400 for the specified
     cmd return codes(input_ret), otherwise it's 500

     StorLeverError's str is the stdout/stderr of the cmd

    """
    try:
        return subprocess.check_output(cmd,
                                       stderr=subprocess.STDOUT,
                                       shell=shell)
    except subprocess.CalledProcessError as e:
        if e.returncode in input_ret:
            http_status = 400
        else:
            http_status = 500
        info = e.output

        # re-raise the storlever's error
        raise exception.StorLeverError(info, http_status)







