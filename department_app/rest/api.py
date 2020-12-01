from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse

from .. import db
from ..models import models


api_bp = Blueprint('api', __name__, url_prefix='/api')


class DepartmentList(Resource):
    """Rest class with methods for adding new department,
    fetching list of departments."""

    def get(self):
        departments = models.Department.query.all()
        if departments is None:
            return jsonify({'message': 'There is no departments.'}, 204)

        department_schema = models.DepartmentSchema(many=True)
        response = department_schema.dump(departments)
        return jsonify({'departments': response}, 200)

    def post(self):
        json_department = request.get_json()
        if json_department is None:
            return jsonify({'message': 'No data provided.'}, 400)
        schema = models.DepartmentSchema()
        new_department = schema.load(json_department)
        print('-'*30, new_department)
        db.session.add(new_department)
        db.session.commit()
        return jsonify(json_department, 201)


class Department(Resource):
    "Rest class with methods for "
    def get(self, id):
        department = models.Department.query.get_or_404(id)
        schema = models.DepartmentSchema()
        response = schema.dump(department)
        return jsonify(response, 200)

    def put(self, id):
        department = models.Department.query.get_or_404(id)
        new_name = request.json.get('name')
        if new_name is None:
            return jsonify(
                {'message': 'Name of department is not specified.'}, 400)

        department.name = new_name
        db.session.commit()
        return jsonify('', 204)

    def delete(self, id):
        department = models.Department.query.get_or_404(id)
        db.session.delete(department)
        db.session.commit()
        return jsonify('', 204)
