def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.network')
    config.include(__name__ + '.system')
    config.include(__name__ + '.lvm')
    config.include(__name__ + '.block')
    config.include(__name__ + '.md')
    config.include(__name__ + '.fs')
    config.include(__name__ + '.utils')
    config.include(__name__ + '.nas')
    config.include(__name__ + '.san')
    config.scan()             # scan to register view callables, must be last statement