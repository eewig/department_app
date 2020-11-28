import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP_SETTINGS = 'department_app.' + os.getenv('APP_SETTINGS',
    'config.ProductionConfig')

db = SQLAlchemy()


def create_app(test_object=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_object is None:
        app.config.from_object(APP_SETTINGS)
    else:
        app.config.from_object(test_object)

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    @app.route('/')
    def hello():
        return 'Hello'


    # app.register_blueprint(employee.bp)

    # DB

    db.init_app(app)

    with app.app_context():
        from .views import department

        db.create_all()


        return app
