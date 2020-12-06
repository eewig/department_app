from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from .. import db
from ..models import models
from ..models import schemas


class EmployeeList(Resource):

    def get(self):
        employees = models.Employee.query.all()
        if not len(employees):
            return '', 204

        schema = schemas.EmployeeSchema(many=True)
        response = schema.dump(employees)
        return response, 200

    def post(self):
        json_employee = request.get_json()
        schema = schemas.EmployeeSchema()
        try:
            employee = schema.load(json_employee)
        except ValidationError as err:
            return err.messages, 400
        db.session.add(employee)
        db.session.commit()
        return json_employee, 201


class Employee(Resource):

    def get(self, id):
        employee = models.Employee.query.get_or_404(id)
        schema = schemas.EmployeeSchema()
        response = schema.dump(employee)
        return response, 200

    def put(self, id):
        employee = models.Employee.query.get_or_404()
        employee_json = request.get_json()
        new_employee = schemas.EmployeeSchema(employee_json,
            instance=employee)
        print('*'*50, new_employee)
        return new_employee, 200
