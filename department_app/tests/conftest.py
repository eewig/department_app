import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from department_app import create_app, db
from department_app.config import TestingConfig
# from department_app.models.db_utils import init_db, drop_db


@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)
    if os.getenv('GITLAB_CI'):
        engine = create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
        if not database_exists(engine.url):
            create_database(engine.url)
    with app.app_context():
        yield app
    if os.getenv('GITLAB_CI'):
        drop_database(engine.url)


@pytest.fixture(scope='module')
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
            db.drop_all()


def create_test_db(func):
    def wrapper(*args):
        engine = create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
        if not database_exists(engine.url):
            create_database(engine.url)
        func()
        drop_database(engine.url)
    return wrapper

def decorate_if_gitlab(decorator):
    if os.getenv('GITLAB_CI'):
        return decorator


# @pytest.fixture(scope='module')
# def client():
#     app = create_app(TestingConfig)
#
#     with app.test_client() as testing_client:
#         with app.app_context():
#             yield testing_client



# @pytest.fixture
# def app():
#     def _app(config_class):
#         app = create_app(config_class)
#         app.test_request_context().push()
#
#         if config_class is TestingConfig:
#             db.drop_all()
#             from ..models.models import Department, Employee
#             db.create_all()
#
#         return app
#
#     yield _app
#     db.session.remove()
#     if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
#         db.drop_all()
#
#
# def init_database():
#     db.create_all()
#
#     yield db
#
#     db.drop_all()
