from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse

from .. import db
from ..models.models import Department, DepartmentSchema


api_bp = Blueprint('api', __name__, url_prefix='/api')


class Departments(Resource):
    def get(self):
        departments = Department.query.all()
        if departments is None:
            return jsonify({'message': 'There is no departments.'}, 204)

        department_schema = DepartmentSchema(many=True)
        response = department_schema.dump(departments)
        print(type(response), response)
        return jsonify({response}, 200)

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        new_department = Department(name=args.get('name'))
        print(new_department)
        db.session.add(new_department)
        db.session.commit()
        return jsonify({'id': new_department.id, 'name': new_department.name}, 200)
