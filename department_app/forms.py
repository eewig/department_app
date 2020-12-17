from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields.html5 import DateField, IntegerField


class AddDepartment(FlaskForm):
    """Form for adding a department."""
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Add')


class UpdateDepartment(AddDepartment):
    """Form for updating a department."""
    submit = SubmitField('Update')


class AddEmployee(FlaskForm):
    """Form for adding an employee."""
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=80)])
    dob = DateField('Date of birth',
                    validators=[DataRequired()])
    salary = IntegerField('Salary',
                          validators=[DataRequired(), NumberRange(min=0)])
    department = SelectField('Department', coerce=int)
    submit = SubmitField('Add')


class UpdateEmployee(AddEmployee):
    """Form for updating an employee."""
    submit = SubmitField('Update')


class SearchEmployeeForm(FlaskForm):
    """Form for filtering employees by date of birth."""
    dob = DateField('Beginning', validators=[DataRequired()])
    dob_end = DateField('End')
    submit = SubmitField('Search')
