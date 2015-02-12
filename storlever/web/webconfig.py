"""
storlever.web.webconfig
~~~~~~~~~~~~~~~~

This module implements index web page of storlever

:copyright: (c) 2014 by OpenSight (www.opensight.cn).
:license: AGPLv3, see LICENSE for more details.

"""

import os
import errno
import hashlib
from storlever.mngr.system.cfgmgr import STORLEVER_CONF_DIR
from storlever.lib.config import Config, yaml, ConfigError
from storlever.lib.schema import Schema, Use


class WebConfig(Config):
    """
    default password is opensight2013,
    fc91f9f874d2ef4d48fdde151271716f268977c1f77241d5321b61fda137ac3c is sha256 hash of result of PBKDF2 to opensight2013
    """
    CONF_FILE = os.path.join(STORLEVER_CONF_DIR, 'web.yaml')
    DEFAULT_CONF = {'password': 'fc91f9f874d2ef4d48fdde151271716f268977c1f77241d5321b61fda137ac3c',
                    'language': 'chinese'}
    SCHEMA = Schema({
        'password': Use(str),     # filesystem type
        'language': Use(str),     # dev file
    })

    def __init__(self, conf=None):
        self.conf_file = self.CONF_FILE
        self.conf = conf
        self.schema = self.SCHEMA

    def parse(self):
        if self.conf_file is not None and self.conf_file != "":
            try:
                with open(self.conf_file, "r") as f:
                    self.conf = yaml.load(f)
                if self.schema:
                    self.conf = self.schema.validate(self.conf)
                return self.conf
            except IOError as e:
                if e.errno == errno.ENOENT:
                    self.conf = self.DEFAULT_CONF
                    self.write()
                    return self.conf
                else:
                    raise ConfigError(str(e))
            except Exception:
                raise ConfigError(str(Exception))
        else:
            raise ConfigError("conf file absent")

    @classmethod
    def from_file(cls):
        conf = cls()
        conf.parse()
        return conf

    @classmethod
    def to_file(cls, conf):
        conf = cls(conf=conf)
        conf.write()
        return conf


class WebPassword(object):
    def __init__(self):
        self._web_conf = WebConfig.from_file()
        self._saved_password = self._web_conf.conf['password']

    def check_passwd(self, login, passwd):
        if login == 'admin' and self._saved_password == hashlib.sha256(passwd).hexdigest():
            return True
        return False

    def change_passwd(self, login, passwd):
        if login != 'admin':
            return False
        self._web_conf['password'] = hashlib.sha256(passwd).hexdigest()
        self._web_conf.write()
        return True

