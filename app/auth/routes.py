from datetime import datetime
import os
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, json, current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.main import imageManip
from app.models import Employee
from app.auth.forms import RegistrationForm, LoginForm, \
ResetPasswordForm, ResetPasswordRequestForm
from werkzeug.utils import secure_filename
from app.auth.email import send_password_reset_email



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        employee = Employee.query.filter_by(email=email.lower()).first()
        if employee is None or not employee.check_password(form.password.data):            
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(employee, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        print("Register button pressed")
        firstname = registrationForm.first_name.data
        lastname = registrationForm.last_name.data
        email = registrationForm.email.data.lower()
        jobTitle = registrationForm.job_title.data
        department = registrationForm.department.data
        location = registrationForm.location.data
        startDate = registrationForm.start_date.data
        editordata = request.form.get('editordata').rstrip().lstrip()
        userImage = request.files['fileUpload']
        if userImage:
            x1 = request.form.get('outX1')
            y1 = request.form.get('outY1')
            x2 = request.form.get('outX2')
            y2 = request.form.get('outY2')
            if x1 is '' or x2 is '' or y1 is '' or y2 is '':
                flash('Please drag a crop box on your uploaded images.', 'error')
                exit
            else:
                print ("Crop Coords: ", x1, x2, y1, y2)
                imageName = imageManip.cropNsave(userImage, email, x1, y1, x2, y2)
                
                print (imageName)
                        
                newEmployee = Employee(email = email,
                                       first_name = firstname,
                                       last_name = lastname,
                                       job_title = jobTitle,
                                       department = department,
                                       location = location,
                                       start_date = startDate,
                                       current_employee = True,
                                       about_me = editordata,
                                       image_name = imageName)
                newEmployee.set_password(registrationForm.password.data)
                db.session.add(newEmployee)
                db.session.commit()
                
                flash(("Congratulations %s %s , you are now a registered user!" % (firstname, lastname)))
                return redirect(url_for('auth.login'))
        else:
            flash('Please upload a user profile image.')
    print("Before render_template return")
    return render_template('auth/register.html', title=('Register'),
                           registrationForm=registrationForm)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            send_password_reset_email(employee)
        flash('Email sent to address: ' + employee.email)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    employee = Employee.verify_reset_password_token(token)
    if not employee:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        employee.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)








