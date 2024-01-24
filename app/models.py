from datetime import datetime
from hashlib import md5
from time import time
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import current_app
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from config import Config

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Employee(UserMixin, SearchableMixin, db.Model):
    """
    Create an Employee table
    """    
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'
    __searchable__= ['email', 'first_name', 'last_name', 'job_title', 'department', 'location', 'about_me']
    
    id = db.Column(db.Integer, primary_key=True)    
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))    
    first_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    job_title = db.Column(db.String(64), index=True, unique=False)
    department = db.Column(db.String(64), index=True, unique=False)
    location = db.Column(db.String(64), index=True, unique=False)
    start_date = db.Column(db.DateTime)
    current_employee = db.Column(db.Boolean, index=True, default=True)
    image_name = db.Column(db.String, default=None, nullable=True)
    about_me = db.Column(db.Text)

    def __repr__(self):
        return '<Employee: {}, {}, {}, {}, {}, {}>'.format(self.last_name, self.first_name,
                                               self.email, self.job_title,
                                               self.department, self.location)
    
    def getEmployeePhoto(self):
        return Config.STATIC_IMG_PATH + self.image_name
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Employee.query.get(id)


@login.user_loader
def load_employee(id):
    return Employee.query.get(int(id))


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

