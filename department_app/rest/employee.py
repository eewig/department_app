from datetime import datetime
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from .. import db
from ..models import models
from ..models import schemas


class EmployeeList(Resource):

    def get(self):
        id = request.args.get('department_id')
        birth = request.args.get('dob')
        birth_end = request.args.get('dob_end')
        if id:
            response = employees_by_department_id(id)
        elif birth:
            try:
                response = dob_filter(birth, birth_end)
            except ValueError:
                return {'message': 'Wrong time format! (yyyy-mm-dd)'}, 400
        else:
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
        employee = models.Employee.query.get_or_404(id)
        employee_json = request.get_json()
        schema = schemas.EmployeeSchema()
        new_employee_json = schema.dump(employee)
        for key in new_employee_json:
            if key in employee_json:
                new_employee_json[key] = employee_json[key]
        new_employee = schema.load(new_employee_json)
        db.session.commit()
        return '', 204

    def delete(self, id):
        employee = models.Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


def employees_by_department_id(id):
    """Filter employee by department id.
    Form json response requested  department.id, department.name and
    list of employees with columns name, salary.
    """

    schema = schemas.EmployeeSchema(many=True)
    department = models.Department.query.get_or_404(id)
    employees = models.Employee.query.filter_by(department_id=id)
    response = schema.dump(employees)
    return response


def dob_filter(birth, birth_end):
    """Filter employees by date of birth (dob). If birth_end available
    filter in range of dates, otherwise by single date.

    :return json of employee objects
    """

    schema = schemas.EmployeeSchema(many=True)
    if birth_end is None:
        try:
            birth = datetime.strptime(birth, '%Y-%m-%d')
        except ValueError:
            raise ValueError
        employees = models.Employee.query.filter_by(dob=birth)
        response = schema.dump(employees)
        return response
    else:
        try:
            birth = datetime.strptime(birth, '%Y-%m-%d')
            birth_end = datetime.strptime(birth_end, '%Y-%m-%d')
        except ValueError:
            raise ValueError
        if birth > birth_end:
            raise ValueError
        employees = models.Employee.query.filter(
            models.Employee.dob.between(birth, birth_end))
        response = schema.dump(employees)
        return response
