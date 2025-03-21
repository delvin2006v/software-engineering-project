class LocalConfig :

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.db"
    SECRET_KEY = "THIS-IS-A-SECRET-KEY"
    SECURITY_PASSWORD_SALT = "too-salty"
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_PROTECT_MECHANISM = []
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    SECURITY_REDIRECT_BEHAVIOR = 'spa'

class TestConfig(LocalConfig) :
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/testdb.db'

