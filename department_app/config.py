import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # DB
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    _POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    _POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
    _POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    _POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + _POSTGRES_USER \
        + ':' + _POSTGRES_PASSWORD + '@' + _POSTGRES_HOST + ':' \
        + _POSTGRES_PORT + '/' + _POSTGRES_DB


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
