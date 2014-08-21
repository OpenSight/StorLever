def includeme(config):
    # look into following modules' includeme function
    # in order to register routes
    config.include(__name__ + '.index')
    config.include(__name__ + '.login')
    config.include(__name__ + '.menu')
    config.include(__name__ + '.regist_menu')
    config.scan()    # scan to register view callables, must be last statement
