from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    # Authentication Data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    tasks = db.relationship('Task')

    #Personal Details
    fullname = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    url = db.Column(db.String(150))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline_date = db.Column(db.DateTime(timezone=True), default=None)
    state = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))