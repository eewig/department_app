from datetime import datetime
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from ..models import db
from ..models import models
from ..models import schemas


class EmployeeList(Resource):
    """Rest class with methods for adding new employee,
    fetching list of employees.
    """

    def get(self):
        """Fetches a list of employees.
        If the department_id argument in a request is specified, then
        returns employees filtered by the given department.
        If the dob argument in a request is specified, then
        returns employees filtered by the given date of birth.
        If the dob and dob_end arguments in a request are specified,
        then returns employees filtered in a range by the given
        dates of birth.
        Otherwise returns the ordinary list of employees.

        If there are no departments it returns the 204 status code.

        :return: List of employees
        """

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
        """Adds a new employee.
        If sent data is not valid returns the 400 status code
        with the appropriate json message.
        On success returns sent data with the 201 status code.

        :return: The sent employee and status code 201
        """

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
    """Rest class with methods GET, PUT, DELETE department."""

    def get(self, employee_id):
        """Gets employee by id.

        :param employee_id:  Id of the employee being fetched.

        :return: Employee
        """

        employee = models.Employee.query.get_or_404(employee_id)
        schema = schemas.EmployeeSchema()
        response = schema.dump(employee)
        return response, 200

    def put(self, employee_id):
        """Update an employee.

        :param employee_id: Id of the employee being updated.

        :return: 204 status code
        """

        employee = models.Employee.query.get_or_404(employee_id)
        employee_json = request.get_json()
        schema = schemas.EmployeeSchema()
        new_employee_json = schema.dump(employee)
        for key in new_employee_json:
            if key in employee_json:
                new_employee_json[key] = employee_json[key]
        db.session.commit()
        return '', 204

    def delete(self, employee_id):
        """Delete an employee.

        :param employee_id: Id of the employee being deleted.

        :return: 204 status code
        """

        employee = models.Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


def employees_by_department_id(department_id):
    """Filter employees by department id.

    :param department_id: Department id by which employees being filtered.

    :return: List of employees
    """

    schema = schemas.EmployeeSchema(many=True)
    # department = models.Department.query.get_or_404(department_id)
    employees = models.Employee.query.filter_by(department_id=department_id)
    response = schema.dump(employees)
    return response


def dob_filter(dob, dob_end):
    """Filter employees by date of birth.

    :param dob: Date of birth.
    :param dob_end: The end date of birth in range. If dob_end
    presented function filters employees in range of dates of birth.
    Otherwise by one single date (dob).

    :raises: :class:`ValueError`: If dob > dob_end or date inputted
    in bad format

    :return List of employees
    """

    schema = schemas.EmployeeSchema(many=True)
    if dob_end is None:
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        except ValueError as exc:
            raise ValueError from exc
        employees = models.Employee.query.filter_by(dob=dob)
        response = schema.dump(employees)
        return response
    try:
        dob = datetime.strptime(dob, '%Y-%m-%d')
        dob_end = datetime.strptime(dob_end, '%Y-%m-%d')
    except ValueError as exc:
        raise ValueError from exc
    if dob > dob_end:
        raise ValueError
    employees = models.Employee.query.filter(
        models.Employee.dob.between(dob, dob_end))
    response = schema.dump(employees)
    return response
