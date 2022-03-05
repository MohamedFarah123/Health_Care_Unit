from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from functools import wraps
from flask_login import login_user, login_required, logout_user, current_user
from flask import session

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
def profile():
    return render_template('profile.html')


@routes.route('/drdashboard')
@login_required
def drdashboard():
    return render_template('drdashboard.html', name=current_user.email)


@routes.route('/drlogout')
@login_required
def drlogout():
    logout_user()
    flash("You have been Logged out!")
    return redirect(url_for('routes.drlogout'))

