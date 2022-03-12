from . import db
from flask_login import UserMixin
from flask_login import LoginManager, current_user
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


# BIG PROBLEM WITH NOT NULL FUNCTION.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(50))
    birthday = db.Column(db.Integer)
    number = db.Column(db.Integer)
    password = db.Column(db.String(150))
    appointmentID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class Doctors(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    doctorID = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete="CASCADE"))
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    second_name = db.Column(db.String(150))
    number = db.Column(db.Integer)
    date = db.Column(db.Integer, nullable=False)
    slot = db.Column(db.String(150))
    # slot = db.Column(db.String(150), unique=True)
    Description = db.Column(db.String(150))
    doctorID = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete="CASCADE"))
    appointmentID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

