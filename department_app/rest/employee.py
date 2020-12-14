from datetime import datetime
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from .. import db
from ..models import models
from ..models import schemas


class EmployeeList(Resource):

    def get(self):
        department_id = request.args.get('department_id')
        dob = request.args.get('dob')
        dob_end = request.args.get('dob_end')
        if department_id:
            response = employees_by_department_id(department_id)
        elif dob:
            try:
                response = dob_filter(dob, dob_end)
            except ValueError:
                return {'message': 'Wrong time format! (yyyy-mm-dd)'}, 400
        else:
            employees = models.Employee.query.all()
            if not employees:
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

    def get(self, employee_id):
        employee = models.Employee.query.get_or_404(employee_id)
        schema = schemas.EmployeeSchema()
        response = schema.dump(employee)
        return response, 200

    def put(self, employee_id):
        employee = models.Employee.query.get_or_404(employee_id)
        employee_json = request.get_json()
        schema = schemas.EmployeeSchema()
        new_employee_json = schema.dump(employee)
        for key in new_employee_json:
            if key in employee_json:
                new_employee_json[key] = employee_json[key]
        new_employee = schema.load(new_employee_json)
        db.session.commit()
        return '', 204

    def delete(self, employee_id):
        employee = models.Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


def employees_by_department_id(department_id):
    """Filter employee by department id.
    Form json response requested  department.id, department.name and
    list of employees with columns name, salary.
    """

    schema = schemas.EmployeeSchema(many=True)
    department = models.Department.query.get_or_404(department_id)
    employees = models.Employee.query.filter_by(department_id=department_id)
    response = schema.dump(employees)
    return response


def dob_filter(dob, dob_end):
    """Filter employees by date of dob. If dob_end available
    filter in range of dates, otherwise by single date.

    :return json of employee objects
    """

    schema = schemas.EmployeeSchema(many=True)
    if dob_end is None:
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            raise ValueError
        employees = models.Employee.query.filter_by(dob=dob)
        response = schema.dump(employees)
        return response
    else:
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
            dob_end = datetime.strptime(dob_end, '%Y-%m-%d')
        except ValueError:
            raise ValueError
        if dob > dob_end:
            raise ValueError
        employees = models.Employee.query.filter(
            models.Employee.dob.between(dob, dob_end))
        response = schema.dump(employees)
        return response
