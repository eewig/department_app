import pytest

from department_app import create_app, db
from department_app.config import TestingConfig
from department_app.models.db import init_db, drop_db


@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        # init_db()
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()
        # drop_db()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

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
