from flask import request, render_template, flash, redirect, url_for
from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.models import Department, Employee
from ..models import queries
from ..forms import AddDepartment, UpdateDepartment


@app.route('/', methods=['GET', ])
def home():
    departments = queries.get_departments_with_avg_salary()
    return render_template('department/departments.html',
                           departments=departments)


@app.route('/department/<int:id>')
def department(id):
    department = Department.query.get_or_404(id)
    employees = Employee.query.filter_by(department_id=id)
    return render_template('department/department.html',
                           department=department, employees=employees)


@app.route('/department/add', methods=['POST', 'GET'])
def add_department():
    form = AddDepartment()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_department = Department(name=form.name.data)
            db.session.add(new_department)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Department already exists!', 'warning')
                return redirect(url_for('add_department'))

            flash(f'Department {form.name.data} created!', 'success')
            return redirect(url_for('home'))

        flash('Name not defined.', 'warning')
    return render_template('department/department_add.html', form=form)


@app.route('/department/update/<int:id>', methods=('POST', 'GET'))
def update_department(id):
    form = UpdateDepartment()
    department = Department.query.get_or_404(id)
    if request.method == 'POST':
        if form.validate_on_submit():
            department.name = form.name.data
            try:
                db.session.commit()
            except IntegrityError:
                flash('Department with this name already exists.', 'warning')
                db.session.rollback()
                return render_template('department/department_update.html',
                                       form=form)

            flash(f'Department name successfully changed!', 'success')
            return redirect(url_for('home'))
    return render_template('department/department_update.html',
                           form=form, department=department)
