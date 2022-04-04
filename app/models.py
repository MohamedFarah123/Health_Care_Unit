from app.extensions import db
from app import app
import jwt
from flask_login import UserMixin, login_manager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from time import time
from sqlalchemy.sql import func


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

    is_doctor = db.Column(db.Boolean, nullable=False, default=False)
    doctor_name = db.Column(db.String(150))
    dr_email = db.Column(db.String(150), unique=True)
    doctorID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    dr_password = db.Column(db.String(150))
    dr_department = db.Column(db.String(150))

    def to_dict(self):
        return {
            'doctor_name': self.doctor_name,
            'dr_email': self.dr_email,
            'doctorID': self.doctorID,
            'dr_password': self.dr_password,
            'dr_department': self.dr_department
        }

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user.id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user.id']
        except:
            return None
        return User.query.get(user_id)


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    second_name = db.Column(db.String(150))
    number = db.Column(db.Integer)
    date = db.Column(db.Integer, nullable=False)
    slot_time = db.Column(db.String, db.ForeignKey('slots.id', ondelete="CASCADE"))
    Description = db.Column(db.String(150))
    doctorID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    doctor_name = db.Column(db.String(150))
    appointmentID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'second_name': self.second_name,
            'date': self.date,
            'slot_time': self.slot_time,
            'Description': self.Description,
            'appointmentID': self.appointmentID,
            'doctorID': self.doctorID,
            'doctor_name': self.doctor_name
        }


class Slots(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    slot_time = db.Column(db.String(150), db.ForeignKey('slots.id', ondelete="CASCADE"))
    date = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, nullable=False, default=False)
    doctorID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    booked_by_email = db.Column(db.String(150))


