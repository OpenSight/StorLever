def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.megaraid')
    config.scan()             # scan to register view callables, must be last statement