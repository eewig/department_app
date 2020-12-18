from flask import render_template, request, flash, redirect, url_for
from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.models import Employee, Department
from ..forms import AddEmployee, UpdateEmployee, SearchEmployeeForm


@app.route('/employee')
def employees():
    """View for listing employees."""
    form = SearchEmployeeForm()
    employees_list = Employee.query.order_by(Employee.name).all()
    return render_template('employee/employees.html',
                           employees=employees_list, form=form)


@app.route('/employee/<int:employee_id>')
def employee(employee_id):
    """View for a certain employee with a department he belongs to.

    :param employee_id: Id of the employee that will be viewed.
    """

    employee_obj = Employee.query.get_or_404(employee_id)
    department = Department.query.join(Department.employees) \
        .filter(Employee.id == employee_id).first()
    return render_template('employee/employee.html', employee=employee_obj,
                           department=department)


@app.route('/employee/add', methods=('POST', 'GET'))
def add_employee():
    """View for adding an employee."""
    form = AddEmployee()
    form.department.choices = get_departments_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.department.data:
                new_employee = Employee(name=form.name.data, dob=form.dob.data,
                                        salary=form.salary.data,
                                        department_id=form.department.data)
            else:
                new_employee = Employee(name=form.name.data, dob=form.dob.data,
                                        salary=form.salary.data)
            db.session.add(new_employee)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Error! Check data you have submitted', 'warning')
                return redirect(url_for('add_employee'))

            flash(f'Employee {form.name.data} created!', 'success')
            return redirect(url_for('employees'))

        flash('Error! Check data you have entered.', 'warning')
    return render_template('employee/employee_add.html',
                           form=form)


@app.route('/employee/update/<int:employee_id>', methods=('POST', 'GET'))
def update_employee(employee_id):
    """View for editing an employee.

    :param employee_id: Id of employee that will be edited.
    """

    employee_obj = Employee.query.get_or_404(employee_id)
    form = UpdateEmployee()
    form.department.choices = get_departments_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee_obj.name = form.name.data
            employee_obj.dob = form.dob.data
            employee_obj.salary = form.salary.data
            if form.department.data:
                employee_obj.department_id = form.department.data
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Error! Check data you have submitted.', 'warning')
                return redirect(url_for('update_employee',
                                        employee_id=employee_obj.id))
        else:
            flash('Error! Check data you have entered.', 'warning')
            return redirect(url_for('update_employee',
                                    employee_id=employee_obj.id))
        flash('Employee updated!', 'success')
        return redirect(url_for('employees'))
    return render_template('employee/employee_update.html',
                           form=form, employee=employee_obj)


@app.route('/employee/delete/<int:employee_id>', methods=('GET', ))
def delete_employee(employee_id):
    """View for deleting an employee.

    :param employee_id: Id of employee that will be deleted.
    """

    employee_obj = Employee.query.get_or_404(employee_id)
    db.session.delete(employee_obj)
    db.session.commit()
    flash(f'Employee {employee_obj.name} successfully deleted.', 'success')
    return redirect(url_for('employees'))


def get_departments_choices():
    """Create a list of choices for Form's SelectField."""
    departments = Department.query.order_by(Department.name).all()
    choices = [(dep.id, dep.name) for dep in departments]
    choices.insert(0, (0, 'No department'))
    return choices
