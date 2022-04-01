from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from functools import wraps
from flask import session
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Doctors, Appointment, Slots

routes = Blueprint('routes', __name__)


@routes.route('/')
@routes.route('/home')
def home():
    return render_template('home.html')


@routes.route('/login')
def login():
    return render_template('login.html')


@routes.route('/register')
def register():
    return render_template('register.html')


@routes.route('/drlogin')
def drlogin():
    return render_template('drlogin.html')


@routes.route('/userdash')
@login_required
def userdash():
    return render_template('userdash.html', name=current_user.email)


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been Logged out!")
    return redirect(url_for('routes.login'))


@routes.route('profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email)


@routes.route('appointment')
@login_required
def appointment():
    selected_doctors = Doctors.query.filter_by()
    return render_template('appointment.html', name=current_user.email, all_doctors=selected_doctors)


@routes.route('/drdashboard')
@login_required
def drdashboard():
    return render_template('drdashboard.html', name=current_user.email)


@routes.route('/confirmation')
@login_required
def confirmation():
    return render_template('confirmation.html', name=current_user.id)


@routes.route('forgot')
def forgot():
    return render_template('forgot.html')


@routes.route('/schedule')
@login_required
def schedules():
    return render_template('schedule.html')


@routes.route('/drlogout')
@login_required
def drlogout():
    logout_user()
    flash("You have been Logged out!")
    return redirect(url_for('routes.drlogin'))


@routes.route('/history')
@login_required
def history():
    return render_template('history.html')


@routes.route('/prescription')
@login_required
def prescription():
    return render_template('prescription.html')


@routes.route('/drprofile')
@login_required
def drprofile():
    return render_template('drprofile.html', name=current_user.email)


