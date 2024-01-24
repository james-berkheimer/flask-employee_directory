from datetime import datetime
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
    
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):    
    outX1 = HiddenField()
    outY1 = HiddenField()
    outX2 = HiddenField()
    outY2 = HiddenField()
    outW = HiddenField()
    outH = HiddenField()
    job_title = StringField('Job Title', validators=[DataRequired()])
    department = SelectField('Departments', choices=Config.VISMO_DEPARTMENTS)  
    location = StringField('Location') 
    start_date = DateField("Start Date", format="%Y-%m-%d",
                           default=datetime.today,
                           validators=[DataRequired()])
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField(('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(('Register'))
    fileUpload = FileField('Employee Image',
                               validators=[FileRequired(), FileAllowed(images, 'Images only!')])

    def validate_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee is not None:
            raise ValidationError('Please use a different email address.')
        
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
    
    
    
    