from datetime import datetime
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, FieldList, FormField, \
RadioField, IntegerField, HiddenField, SelectField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import ValidationError, DataRequired, Length, \
NoneOf, EqualTo, Email
from app import images
from app.models import Employee
from config import Config


class MainForm(FlaskForm):
    image_name = StringField('StringField')    
    def sortByLetter(self, letter):
        return Employee.query.filter(Employee.last_name.startswith(letter)).all()    
    
class EditProfileForm(FlaskForm):
    outX1 = HiddenField()
    outY1 = HiddenField()
    outX2 = HiddenField()
    outY2 = HiddenField()
    outW = HiddenField()
    outH = HiddenField()
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField(('Email'), validators=[DataRequired(), Email()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    department = SelectField('Departments', choices=Config.VISMO_DEPARTMENTS) 
    location = StringField('Location') 
    start_date = DateField("Start Date", format="%Y-%m-%d",
                           default=datetime.today,
                           validators=[DataRequired()])
    current_employee = BooleanField("Current Employee")    
    fileUpload = FileField('Employee Image',
                               validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Update Profile')

    def __init__(self, original_email, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            employee = Employee.query.filter_by(email=self.email.data).first()
            if employee is not None:
                raise ValidationError('Please use a different email address.')
            
            
class SearchForm(FlaskForm):
    q = StringField(('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
            
            

