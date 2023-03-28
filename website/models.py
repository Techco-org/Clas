from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import datetime

class User(db.Model, UserMixin):
    __searchable__ = ['fullname', 'id', 'email']

    # Authentication Data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    #Relationships
    tasks = db.relationship('Task')
    images = db.relationship('Img')
    grades = db.relationship('Grade')

    #Personal Details
    fullname = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    url = db.Column(db.String(150))

    #Basic info
    home_address = db.Column(db.String(150))
    date_of_birth = db.Column(db.DateTime(timezone=True))
    current_grade = db.Column(db.Integer)
    highschool = db.Column(db.String(150))

    #Account type(False: Student, True: Recruiter)
    account_type = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User_ID:{}>'.format(self.id)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline_date = db.Column(db.DateTime(timezone=True), default=None)
    state = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    overall = db.Column(db.Float)
    grade = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))