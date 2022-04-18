from flask_wtf import FlaskForm
from app.extensions import db
from app.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError
from wtforms.validators import EqualTo, Email, DataRequired, Length


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    address = StringField('address', validators=[DataRequired()])
    number = StringField('number', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UpdateDrForm(FlaskForm):
    dr_email = StringField('Doctor Email',
                           validators=[DataRequired(), Email()])

    doctor_name = StringField('Doctor name', validators=[DataRequired()])
    dr_department = StringField('Doctor Department', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, dr_email):
        if dr_email.data != current_user.dr_email:
            user = User.query.filter_by(dr_email=dr_email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
