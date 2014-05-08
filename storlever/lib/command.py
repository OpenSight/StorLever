"""
storlever.lib.command
~~~~~~~~~~~~~~~~

This module implements command call for storlever.

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""
import subprocess
import os
import exception

# backport check_output to python 2.6
if "check_output" not in dir( subprocess ):
    def backport_check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.

        Backported from Python 2.7 as it's implemented as pure python on stdlib.

        >>> check_output(['/usr/bin/python', '--version'])
        Python 2.6.2
        """
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            error = subprocess.CalledProcessError(retcode, cmd)
            error.output = output
            raise error
        return output
    subprocess.check_output = backport_check_output;


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
        raise exception.StorLeverCmdError(e.returncode, info, http_status)


def read_file_entry(path, default_value = None):
    if os.path.isfile(path):
        with open(path, "r") as file_entry:
            value = file_entry.read()
    else:
        if default_value is None:
            raise exception.StorLeverError(path + " does not exist", 500)
        else:
            value = default_value
    return value


def write_file_entry(path, value):
    if os.path.isfile(path):
        with open(path, "w") as file_entry:
            file_entry.write(value)
    else:
        raise exception.StorLeverError(path + " does not exist", 500)

    return value

SELINUXENABLED_BIN = "/usr/sbin/selinuxenabled"
GETENFORCE_BIN = "/usr/sbin/getenforce"
SETENFORCE_BIN = "/usr/sbin/setenforce"

def set_selinux_permissive():
    """check selinux and put it in permissive mode
    """
    if os.path.exists(SELINUXENABLED_BIN) and \
                    subprocess.call([SELINUXENABLED_BIN]) == 0:
        if os.path.exists(GETENFORCE_BIN) and \
                "Enforcing" in check_output([GETENFORCE_BIN]) :
            if os.path.exists(SETENFORCE_BIN):
                check_output([SETENFORCE_BIN, "0"])


