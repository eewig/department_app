from flask import jsonify, request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from .. import db
from ..models import models
from ..models import schemas


class DepartmentList(Resource):
    """Rest class with methods for adding new department,
    fetching list of departments."""

    def get(self):
        departments = models.Department.query.all()
        if len(departments) == 0:
            return '', 204

        schema = schemas.DepartmentSchema(many=True)
        response = schema.dump(departments)
        return jsonify(response)

    def post(self):
        json_department = request.get_json()
        schema = schemas.DepartmentSchema()
        try:
            new_department = schema.load(json_department)
        except ValidationError:
            return {'message': 'Data is not valid.'}, 400
        db.session.add(new_department)
        db.session.commit()
        return json_department, 201


class Department(Resource):
    "Rest class with methods for "
    def get(self, id):
        department = models.Department.query.get_or_404(id)
        schema = schemas.DepartmentSchema()
        response = schema.dump(department)
        return response, 200

    def put(self, id):
        department = models.Department.query.get_or_404(id)
        new_name = request.json.get('name')
        if new_name is None:
            return jsonify(
                {'message': 'Name of department is not specified.'}, 400)

        department.name = new_name
        db.session.commit()
        return '', 204

    def delete(self, id):
        department = models.Department.query.get_or_404(id)
        db.session.delete(department)
        db.session.commit()
        return '', 204
