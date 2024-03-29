import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'


class Config:
    """Base configuration class, from what all configuration classes
    inherit from."""

    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # DB
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    SQLALCHEMY_DATABASE_URI = URI.format(user=POSTGRES_USER,
                                         password=POSTGRES_PASSWORD,
                                         host=POSTGRES_HOST,
                                         port=POSTGRES_PORT, db=POSTGRES_DB)


class ProductionConfig(Config):
    """Configuration class for production only."""
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration class for development only."""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Configuration class for testing only."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    if os.getenv('GITLAB_CI'):
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres'\
                                  '@db:5432/test'
