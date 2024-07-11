class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "key"
    PERMANENT_SESSION_LIFETIME = 1800
    
class ProductionConfig(Config):
    DEBUG= False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
