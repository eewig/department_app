from flask import request, render_template, flash, redirect, url_for
from flask import current_app as app
from ..models.models import db, Department


@app.route('/departments/add', methods=['POST','GET'])
def department_add():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            new_department = Department(
                name=name
            )
            db.session.add(new_department)
            db.session.commit()

            return redirect(url_for('departments'))

        flash('Name not defined.')

    return render_template('department_add.html')


@app.route('/departments', methods=['GET',])
def departments():

    return render_template('departments.html', departments=Department.query.all())
