from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from time import time


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
    slot_time = db.Column(db.String, db.ForeignKey('slots.id', ondelete="CASCADE"))
    Description = db.Column(db.String(150))
    doctorID = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete="CASCADE"))
    appointmentID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'second_name': self.second_name,
            'date': self.date,
            'slot_time': self.slot_time,
            'Description': self.Description,
            'appointmentID': self.appointmentID
        }


class Slots(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    slot_time = db.Column(db.String(150), db.ForeignKey('slots.id', ondelete="CASCADE"))
    date = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, nullable=False, default=False)
    booked_by_email = db.Column(db.String(150))
