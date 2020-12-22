from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..models import models
from ..models import schemas
from ..models import queries


class DepartmentList(Resource):
    """Rest class with methods for adding new department,
    fetching list of departments.
    """

    def get(self):
        """Fetches a list of departments.
        If the avg argument in a request is not None, then returns
        the list of departments with an average salary.
        Otherwise returns the ordinary list of departments.

        If there are no departments it returns the 204 status code.

        :rtype json
        """

        if request.args.get('avg'):
            result = queries.get_departments_with_avg_salary()
            response = []
            for entry in result:
                avg_salary = round(float(entry.salary), 2)
                response.append({"id": entry.id, "name": entry.name,
                                 "average-salary": avg_salary})
        else:
            departments = models.Department.query.all()
            if not departments:
                return '', 204

            schema = schemas.DepartmentSchema(many=True)
            response = schema.dump(departments)
        return response, 200

    def post(self):
        """Adds a new department.
        If sent data is not valid returns the 400 status code
        with JSON message.
        If a department with the sent name already exists returns
        the 400 status code with the appropriate JSON message.

        On success returns sent data with the 201 status code.

        :rtype json
        """

        json_department = request.get_json()
        schema = schemas.DepartmentSchema()
        try:
            new_department = schema.load(json_department)
        except ValidationError:
            return {'message': 'Data is not valid.'}, 400
        db.session.add(new_department)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message':
                    'Department with this name already exists.'}, 400
        return json_department, 201


class Department(Resource):
    """Rest class with methods GET, PUT, DELETE department."""

    def get(self, department_id):
        """Gets department by id.

        :param department_id: Id of the department being fetched.

        On success returns department data.
        On failure returns the status code 404.

        :rtype json
        """

        department = models.Department.query.get_or_404(department_id)
        schema = schemas.DepartmentSchema()
        response = schema.dump(department)
        return response, 200

    def put(self, department_id):
        """Updates a department.

        :param department_id: Id of the department being updated.

        If the department with the department_id does not exist returns
        the status code 404.
        If the name of the department is not specified returns
        the status code 400 with the appropriate message.
        If a department with the same name already exists returns
        the status code 400 with the appropriate message.

        On success returns the status code 204.

        :rtype json
        """

        department = models.Department.query.get_or_404(department_id)
        new_name = request.json.get('name')
        if new_name is None:
            return {'message': 'Name of department is not specified.'}, 400
        department.name = new_name
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message':
                    'Department with this name already exists.'}, 400
        return '', 204

    def delete(self, department_id):
        """Delete department.

        :param department_id: Id of the department being deleted.

        On success returns the status code 204.

        :rtype json
        """

        department = models.Department.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return '', 204
