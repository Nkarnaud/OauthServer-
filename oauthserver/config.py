import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = 'p9Bv<3Eid9%$ju452i01'
    SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/oauth_db'
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/oauth_db'


class TestingConfig(BaseConfig):
    """
    Development environment configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/oauth_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig
}
