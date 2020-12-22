import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from department_app import create_app, db
from department_app.config import TestingConfig


def create_database_for_testing(func):
    def wrapper(*args):
        engine = create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
        if not database_exists(engine.url):
            create_database(engine.url)

        yield func()

        drop_database(engine.url)
    return wrapper


def decorate_if(condition, decorator):
    return decorator if condition else lambda x: x


@pytest.fixture(scope='session')
@decorate_if(os.getenv('GITLAB_CI'), create_database_for_testing)
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        return app


@pytest.fixture(scope='module')
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
            db.drop_all()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
