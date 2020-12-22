import os
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from .models import db              # SQLAlchemy instance
from .models.schemas import ma      # Marshmallow instance


APP_SETTINGS = 'department_app.' + os.getenv('APP_SETTINGS',
    'config.ProductionConfig')

api = Api()
migrate = Migrate()

if os.getenv('APP_SETTINGS') == 'config.ProductionConfig':
    logging.basicConfig(filename='app.log', level=logging.DEBUG)


def create_app(test_object=None):
    """Application factory. Create app instance.

    :param test_object: Configuration object for testing purposes.

    :returns: App instance
    :rtype: Flask
    """

    app = Flask(__name__, instance_relative_config=True)

    if test_object is None:
        app.config.from_object(APP_SETTINGS)
    else:
        app.config.from_object(test_object)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # from .models.models import Department, Employee
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    register_api()

    register_blueprints(app)

    from .models.db_utils import register_db_commands
    register_db_commands(app)

    register_routes(app)
    return app


def register_api():
    """Import and initialize api.
    Adds all resources to the api.
    """

    from .rest import api_bp
    from .rest.department import DepartmentList, Department
    from .rest.employee import EmployeeList, Employee

    api.init_app(api_bp)
    api.add_resource(DepartmentList, '/department')
    api.add_resource(Department, '/department/<int:department_id>')
    api.add_resource(EmployeeList, '/employee')
    api.add_resource(Employee, '/employee/<int:employee_id>')


def register_blueprints(app):
    """Import and register all blueprints on the application."""
    from .rest import api_bp

    app.register_blueprint(api_bp)


def register_routes(app):
    """Import all views so that they are available in the application."""
    with app.app_context():
        from .views import department
        from .views import employee
