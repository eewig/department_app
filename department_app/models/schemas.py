from .. import ma
from .models import Employee, Department


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Employee model."""
    class Meta:
        """Meta class"""
        model = Employee
        include_fk = True
        load_instance = True


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Department model."""
    class Meta:
        """Meta class"""
        model = Department
        include_relationships = True
        load_instance = True
