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
    tasks = db.relationship('Task')
    images = db.relationship('Img')

    #Personal Details
    fullname = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    url = db.Column(db.String(150))

    #Basic info
    home_address = db.Column(db.String(150))
    day_birth = db.Column(db.Integer, default=datetime.datetime.now().day)
    month_birth = db.Column(db.Integer, default=datetime.datetime.now().month)
    year_birth = db.Column(db.Integer, default=datetime.datetime.now().year)


    def __repr__(self):
        return '<User_ID:{}>'.format(self.id)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline_date = db.Column(db.DateTime(timezone=True), default=None)
    state = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))