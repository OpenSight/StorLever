def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.statistics')
    config.include(__name__ + '.system-info')
    config.include(__name__ + '.user')
    config.include(__name__ + '.interface')
    config.include(__name__ + '.bond')
    config.include(__name__ + '.net-settings')
    config.include(__name__ + '.ntp')
    config.include(__name__ + '.snmp')
    config.include(__name__ + '.mail')
    config.include(__name__ + '.smart')
    config.include(__name__ + '.zabbix')
    config.include(__name__ + '.block-set')
    config.include(__name__ + '.scsi-set')
    config.include(__name__ + '.md-set')
