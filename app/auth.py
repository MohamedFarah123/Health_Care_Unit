from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from flask import make_response
from datetime import date as dt
import smtplib
from . import db
from .models import User, Doctors, Appointment
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="Success")
                login_user(user, remember=True)
                return redirect(url_for('routes.userdash'))
            else:
                flash("Password is incorrect", category="Error")
        else:
            flash('Email does not exist', category='Error')
        return render_template('login.html')


@auth.route('/drlogin', methods=['GET', 'POST'])
def drlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        doctor = Doctors.query.filter_by(email=email).first()
        if doctor:
            if doctor.password == password:
                flash("Logged in", category='success')
                login_user(doctor, remember=True)
                return render_template('drdashboard.html')
            else:
                flash("Password is incorrect", category="Error")
        else:
            flash("Email does not exist", category="Error")
    return render_template('drlogin.html')


@auth.route('/home')
def home():
    resp = make_response(render_template(...))
    resp.set_cookie('sessionID', '', expires=0)
    return resp


@auth.route('/userdash')
@login_required
def userdash():
    return render_template('userdash.html', name=current_user.email)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        number = request.form.get('number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash('Email is already in use', category='Error')
        elif password1 != password2:
            flash('Password does not match!', category='error')
        elif len(email) < 6:
            flash("Email is too short", category='Error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        else:
            new_user = User(name=name, email=email, number=number, birthday=birthday,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created')
            return redirect(url_for('routes.userdash'))

    return render_template('register.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been Logged out!")
    return redirect(url_for('routes.login'))


@auth.route('adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form.get("email") == "admin123@management.com" and request.form.get("password") == "admin123":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            flash("Incorrect Email or Password")
            return render_template('adminlogin.html', failed=True)
    return render_template('adminlogin.html')


@auth.route('appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        number = request.form.get('number')
        date = request.form.get('date')
        slot = request.form.get('slot')
        Description = request.form.get('Description')
        appointmentID = current_user.id

        entry = Appointment(first_name=first_name, number=number, second_name=second_name, Description=Description, date=date, slot=slot,
                            appointmentID=appointmentID)

        message = first_name + " " + second_name + " has booked an appointment on" + date + "at" + slot + "Thank you."
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("finalyearproject452@gmail.com", "finalyearproject123")
        server.sendmail("finalyearproject452@gmail.com", email, message)

        db.session.add(entry)
        db.session.commit()
        flash('Successful booking!', category='success')
        return redirect(url_for('routes.confirmation'))


@auth.route('adminlogout')
def adminlogout():
    session.clear()
    return redirect("/")


@auth.route('/drdashboard')
@login_required
def drdashboard():
    return render_template('drdashboard.html', name=current_user.email)


@auth.route('/drlogout')
@login_required
def drlogout():
    session.clear()
    return redirect('routes.drlogout')


@auth.route('/confirmation')
@login_required
def confirmation():
    return render_template('confirmation.html', name=current_user.id)


@auth.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html')
