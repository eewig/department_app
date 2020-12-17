from flask import render_template, request, flash, redirect, url_for
from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.models import Employee, Department
from ..forms import AddEmployee, UpdateEmployee, SearchEmployeeForm


@app.route('/employee')
def employees():
    form = SearchEmployeeForm()
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('employee/employees.html', employees=employees,
                           form=form)


@app.route('/employee/<int:id>')
def employee(id):
    employee = Employee.query.get_or_404(id)
    department = Department.query.join(Department.employees) \
        .filter(Employee.id == id).first()
    return render_template('employee/employee.html', employee=employee,
                           department=department)


@app.route('/employee/add', methods=('POST', 'GET'))
def add_employee():
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


@app.route('/employee/update/<int:id>', methods=('POST', 'GET'))
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    form = UpdateEmployee()
    form.department.choices = get_departments_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee.name = form.name.data
            employee.dob = form.dob.data
            employee.salary = form.salary.data
            if form.department.data:
                employee.department_id = form.department.data
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Error! Check data you have submitted.', 'warning')
                return redirect(url_for('update_employee', id=employee.id))
        else:
            flash('Error! Check data you have entered.', 'warning')
            return redirect(url_for('update_employee', id=employee.id))
        flash(f'Employee updated!', 'success')
        return redirect(url_for('employees'))
    return render_template('employee/employee_update.html',
                           form=form, employee=employee)


@app.route('/employee/delete/<int:employee_id>', methods=('GET', ))
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash(f'Employee {employee.name} successfully deleted.', 'success')
    return redirect(url_for('employees'))


def get_departments_choices():
    departments = Department.query.order_by(Department.name).all()
    choices = [(dep.id, dep.name) for dep in departments]
    choices.insert(0, (0, 'No department'))
    return choices
