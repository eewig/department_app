from flask import request, render_template, flash, redirect, url_for
from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..models.models import Department, Employee
from ..models import queries
from ..forms import AddDepartment, UpdateDepartment


@app.route('/', methods=['GET', ])
def home():
    """View for listing departments with average salaries."""
    departments = queries.get_departments_with_avg_salary()
    return render_template('department/departments.html',
                           departments=departments)


@app.route('/department/<int:department_id>')
def department(department_id):
    """View for a certain department with a list of employees in it.

    :param department_id: Id of the department that will be viewed.
    """

    department_obj = Department.query.get_or_404(department_id)
    employees = Employee.query.filter_by(department_id=department_id)
    return render_template('department/department.html',
                           department=department_obj, employees=employees)


@app.route('/department/add', methods=['POST', 'GET'])
def add_department():
    """View for adding a department."""
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


@app.route('/department/update/<int:department_id>', methods=('POST', 'GET'))
def update_department(department_id):
    """View for editing a department.

    :param department_id: Id of department that will be edited.
    """

    form = UpdateDepartment()
    department_obj = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            department_obj.name = form.name.data
            try:
                db.session.commit()
            except IntegrityError:
                flash('Department with this name already exists.', 'warning')
                db.session.rollback()
                return redirect(url_for('update_department',
                                        department_id=department_obj.id))
            flash('Department name successfully changed!', 'success')
            return redirect(url_for('home'))
    return render_template('department/department_update.html',
                           form=form, department=department_obj)


@app.route('/department/delete/<int:department_id>', methods=('GET', ))
def delete_department(department_id):
    """View for deleting an employee.

    :param department_id: Id of department that will be deleted.
    """

    department_obj = Department.query.get_or_404(department_id)
    db.session.delete(department_obj)
    db.session.commit()
    flash(f'Department {department_obj.name} successfully deleted.', 'success')
    return redirect(url_for('home'))
