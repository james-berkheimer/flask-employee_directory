import os
from pathlib import Path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ELASTICSEARCH_URL= os.environ.get('ELASTICSEARCH_URL') or \
        'http://localhost:9200'
    DEBUG=True
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['jberkheimer@viscira.com',
              'dshah@viscira.com',
              'ahada@viscira.com',
              'CHong@viscira.com']
    POSTS_PER_PAGE = 24
    SESSION_TYPE = 'redis'
    ROOT_APP_DIR = basedir
    EMPLOYEES_PER_PAGE = 24
    VISMO_LOGO = basedir / Path('app/static/img/viscira_squarelogo.png')
    VISMO_DEPARTMENTS = [('Account Management', 'Account Management'), ('Animation', 'Animation'),
        ('Business Development', 'Business Development'), ('Content', 'Content'), ('Design', 'Design'),
        ('Development', 'Development'), ('Executive', 'Executive'),('IT', 'IT'), ('MGFX & Video', 'MGFX & Video'),
        ('Production', 'Production')]
    
    # Uploads    
    UPLOADED_IMAGES_DEST = basedir / Path('app/static/img')
    UPLOADED_IMAGES_URL = 'http://employee_directory.viscira.local/static/img/'
    STATIC_IMG_PATH = "/static/img/employeePhotos/"