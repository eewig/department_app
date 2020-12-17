from sqlalchemy.sql import func
from sqlalchemy import desc

from .. import db
from . import models


def get_departments_with_avg_salary():
    """Calculates average salary for departments.

    :return: List of departments
    """

    result = db.session.query(
        models.Department.id, models.Department.name,
        func.avg(models.Employee.salary).label('salary'))\
        .select_from(models.Department).join(models.Employee, isouter=True)\
        .group_by(models.Department.id).order_by(desc('salary')).all()
    return result
