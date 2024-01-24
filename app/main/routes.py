import os, string
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, json, current_app
from flask_login import current_user, login_required
from app.models import Employee
from app import db
from app.main import bp
from app.main.forms import MainForm, EditProfileForm, SearchForm
from app.main import imageManip
from config import Config


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        db.session.commit()
    g.search_form = SearchForm()
    g.departments = ["Viscira"]
    for employee in Employee.query.order_by(Employee.department).all():
        if employee.department not in g.departments:      
            g.departments.append(employee.department)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    employees = Employee.query.order_by(Employee.last_name).paginate(
        page,
        Config.EMPLOYEES_PER_PAGE,
        False)
    next_url = url_for('main.index', page=employees.next_num) if employees.has_next else None
    prev_url = url_for('main.index', page=employees.prev_num) if employees.has_prev else None
    return render_template('index.html', title=('Home'),
                           paginatedEmployees=employees,
                           employees=employees.items,
                           total_pages=employees.pages,
                           next_url=next_url,
                           prev_url=prev_url)

@bp.route('/employee/<displayname>')
def employee(displayname):
    email = displayname + "@viscira.com"
    ADMIN = False
    if current_user.is_authenticated:
        if current_user.email in Config.ADMINS:
            ADMIN = True
        elif current_user.email == email:
            ADMIN =False
        print ("ADMIN =  %s " % (ADMIN))
    employee = Employee.query.filter_by(email=email).first_or_404()  
    date = employee.start_date
    formatedDate = (date.strftime("%B %d %Y"))
    return render_template('employee.html',
                           employee=employee,
                           formatedDate=formatedDate,
                           ADMIN=ADMIN)

@bp.route('/edit_profile/<displayname>', methods=['GET', 'POST'])
@login_required
def edit_profile(displayname):
    email = displayname + "@viscira.com"
    employee_to_edit = Employee.query.filter_by(email=email).first_or_404()
    print ("employee_to_edit: %s" % (employee_to_edit))
    if current_user.email == email:
        form = EditProfileForm(current_user.email)
    else:
        form = EditProfileForm(email)
    if form.validate_on_submit():
        employee_to_edit.email = form.email.data.lower()
        employee_to_edit.first_name = form.first_name.data
        employee_to_edit.last_name = form.last_name.data
        employee_to_edit.job_title = form.job_title.data
        employee_to_edit.department = form.department.data
        employee_to_edit.location = form.location.data
        employee_to_edit.start_date = form.start_date.data
        employee_to_edit.current_employee = form.current_employee.data
        employee_to_edit.about_me = request.form.get('editordata').rstrip().lstrip()
        userImage = request.files['fileUpload']
        if userImage.filename:
            x1 = request.form.get('outX1')
            y1 = request.form.get('outY1')
            x2 = request.form.get('outX2')
            y2 = request.form.get('outY2')
            if x1 is '' or x2 is '' or y1 is '' or y2 is '':
                flash('Uploaded image not saved.  Please drag a crop box over your image!.', 'error')
                exit
            else:
                print ("Crop Coords: ", x1, x2, y1, y2)
                image_name = imageManip.cropNsave(userImage, form.email.data, x1, y1, x2, y2)
                employee_to_edit.image_name = image_name
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.employee', displayname=displayname))
    
    elif request.method == 'GET':
        form.email.data = employee_to_edit.email.lower()
        form.first_name.data = employee_to_edit.first_name
        form.last_name.data = employee_to_edit.last_name
        form.job_title.data = employee_to_edit.job_title
        form.department.data = employee_to_edit.department
        form.location.data = employee_to_edit.location
        form.start_date.data = employee_to_edit.start_date
        form.current_employee.data = employee_to_edit.current_employee
        about_me = employee_to_edit.about_me
        imageName = employee_to_edit.image_name
        imagePath = Config.STATIC_IMG_PATH + employee_to_edit.image_name
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form,
                           imagePath=imagePath,
                           imageName=imageName,
                           about_me=about_me)

@bp.route('/<filterKey>')
def departmentFilter(filterKey="All", label="Departments"):
    page = request.args.get('page', 1, type=int)
    if filterKey != 'Viscira':
        filtered_employees = Employee.query.filter_by(department=filterKey).order_by(Employee.last_name).paginate(
            page, Config.EMPLOYEES_PER_PAGE, False)
    else:
        filtered_employees = Employee.query.order_by(Employee.last_name).paginate(page, Config.EMPLOYEES_PER_PAGE, False)
    next_url = url_for('main.index', page=filtered_employees.next_num) if filtered_employees.has_next else None
    prev_url = url_for('main.index', page=filtered_employees.prev_num) if filtered_employees.has_prev else None
    return render_template('index.html',
                           label=label,
                           title=filterKey,
                           paginatedEmployees=filtered_employees,
                           employees=filtered_employees.items,
                           total_pages=filtered_employees.pages,
                           next_url=next_url,
                           prev_url=prev_url)

@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    search_word = g.search_form.q.data
    employees, total = Employee.search(search_word, page,
                                       current_app.config['EMPLOYEES_PER_PAGE'])
    next_url = url_for('main.search', q=search_word, page=page + 1) \
        if total > page * current_app.config['EMPLOYEES_PER_PAGE'] else None
    prev_url = url_for('main.search', q=search_word, page=page - 1) \
        if page > 1 else None
    return render_template('search.html',
                           title=('Search'),
                           search_word=search_word,
                           employees=employees,
                           total=total,
                           next_url=next_url,
                           prev_url=prev_url)
