class config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "8865 secret key"

class productionConfig(config):
    pass

class developmentConfig(config):
    DEBUG = True

class testingConfig(config):
    TESTING = True