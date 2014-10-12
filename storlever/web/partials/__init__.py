def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.statistics')
    config.include(__name__ + '.system-info')
