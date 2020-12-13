from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields.html5 import DateField, IntegerField

from .models import models


class AddDepartment(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Add')


class UpdateDepartment(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Update')


class AddEmployee(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=80)])
    dob = DateField('Date of birth',
        validators=[DataRequired()])
    salary = IntegerField('Salary',
        validators=[DataRequired(), NumberRange(min=0)])
    department = SelectField('Department', coerce=int)
    submit = SubmitField('Add')


class UpdateEmployee(AddEmployee):
    submit = SubmitField('Update')
