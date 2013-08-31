def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.network')
    config.include(__name__ + '.system')
    config.include(__name__ + '.lvm')
    config.include(__name__ + '.block')