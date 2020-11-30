import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow


APP_SETTINGS = 'department_app.' + os.getenv('APP_SETTINGS',
    'config.DevelopmentConfig')

db = SQLAlchemy()
api = Api()
ma = Marshmallow()

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
    from .rest.api import Departments, api_bp
    api.init_app(api_bp)
    api.add_resource(Departments, '/departments')

    app.register_blueprint(api_bp)



    # DB

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from .views import department

        db.create_all()



    return app
