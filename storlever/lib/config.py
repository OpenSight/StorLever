import yaml


class ConfigError(Exception):
    pass


class Config(object):
    def __init__(self, conf_file, conf=None, schema=None):
        self.conf_file = conf_file
        self.conf = conf
        self.schema = schema

    def parse(self):
        if self.conf_file:
            try:
                with open(self.conf_file) as f:
                    self.conf = yaml.load(f)
                if self.schema:
                    # TODO validate
                    pass
                return self.conf
            except Exception:
                raise ConfigError()
        else:
            raise ConfigError()

    def write(self):
        if self.conf:
            yaml.dump(self.conf, default_flow_style=False)
        else:
            raise ConfigError

    @classmethod
    def from_file(cls, conf_file, schema=None):
        conf = cls(conf_file, schema=schema)
        conf.parse()
        return conf

    @classmethod
    def to_file(cls, conf_file, conf):
        conf = cls(conf_file, conf=conf)
        conf.write()
        return conf
