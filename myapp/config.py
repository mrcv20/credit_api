from os import environ, path
import os

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    """Base config, uses staging database server."""

    SECRET_KEY = 'senhasecreta'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wasionbr@localhost/teste'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = 'localhost'

class DevelopmentConfig(Config):
    'sqlite:///' + os.path.join(basedir, 'db-test.sqlite')

class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}