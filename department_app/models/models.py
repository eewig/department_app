from .. import db, ma
# from marshmallow_sqlalchemy.fields import Nested


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    employees = db.relationship('Employee', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Department {self.id} - {self.name}>'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department = db.Column(db.Integer, db.ForeignKey('department.id'),
        nullable=False)

    def __repr__(self):
        return f'<Employee {self.id} - {self.name}: {self.department}>'


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True
        load_instance = True


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        include_relationships = True
        load_instance = True

    # employees = ma.List(Nested(EmployeeSchema))
