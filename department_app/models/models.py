from sqlalchemy import types

from .. import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.id} - {self.name}>'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(types.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),
        nullable=False)

    def __repr__(self):
        return f'<Employee {self.id} - {self.name}: {self.department}>'
