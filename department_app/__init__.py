import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow


APP_SETTINGS = 'department_app.' + os.getenv('APP_SETTINGS',
    'config.DevelopmentConfig')

db = SQLAlchemy()
api = Api()
ma = Marshmallow()
migrate = Migrate()

logging.basicConfig(filename='app.log', level=logging.DEBUG)


def create_app(test_object=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_object is None:
        app.config.from_object(APP_SETTINGS)
    else:
        app.config.from_object(test_object)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models.models import Department, Employee
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    register_api(app)

    register_blueprints(app)

    from .models import db_utils
    db_utils.register_db_commands(app)

    register_routes(app)


    return app


def register_api(app):
    from .rest import api_bp
    from .rest.department import DepartmentList, Department
    from .rest.employee import EmployeeList, Employee

    api.init_app(api_bp)
    api.add_resource(DepartmentList, '/department')
    api.add_resource(Department, '/department/<int:id>')
    api.add_resource(EmployeeList, '/employee')
    api.add_resource(Employee, '/employee/<int:id>')


def register_blueprints(app):
    from .rest import api_bp

    app.register_blueprint(api_bp)


def register_routes(app):
    with app.app_context():
        from .views import department
        from .views import employee
