from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from app.extensions import db
from app.passwordresetform import ResetPasswordForm, RequestResetForm
import smtplib
from flask_mail import Message
from app import mail
from app.models import User, Appointment, Slots
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/home')
def home():
    resp = make_response(render_template(...))
    resp.set_cookie('sessionID', '', expires=0)
    return resp


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
        em = request.form.get('dr_email')
        pwd = request.form.get('dr_password')
        doctor = User.query.filter_by(dr_email=em).first()
        if doctor:
            if doctor.dr_password == pwd:
                login_user(doctor, remember=True)
                flash('Logged in successfuly', category='success')
                return redirect(url_for('routes.drdashboard'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash("Email does not exist")

        return render_template('drlogin.html')


@auth.route('/userdash')
@login_required
def userdash():
    return render_template('userdash.html', name=current_user.name)


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
    session.pop()
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


@auth.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        number = request.form.get('number')
        date = request.form.get('date')
        Description = request.form.get('Description')
        slot_time = request.form.get('slot_time')
        is_booked = request.form.get('is_booked')
        doctorID = request.form.get('doctorID')
        booked_by_email = request.form.get('booked_by_email')
        doctor_names = request.form.get('doctor_name')
        appointmentID = current_user.id
        selected_doc = User.query.all()
        doctor_select = ""
        for doctorid in selected_doc:
            if doctorid.doctor_name == doctor_names.strip():
                doctor_select = doctorid.id
                break

        entry = Appointment(email=email, first_name=first_name, number=number, second_name=second_name,
                            Description=Description,
                            date=date, slot_time=slot_time, appointmentID=appointmentID, doctorID=doctor_select,
                            doctor_name=doctor_names)

        message = "We are very happy to confirm that,\n" + first_name + " " + second_name + " has booked an appointment on " + date + " at " + slot_time + "with " + doctor_names
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("finalyearproject452@gmail.com", "finalyearproject123")
        server.sendmail("finalyearproject452@gmail.com", booked_by_email, message)

        exists = Slots.query.filter_by(slot_time=slot_time, is_booked=True, date=date).first()

        if not exists:
            check = Slots(slot_time=slot_time, is_booked=True, booked_by_email=booked_by_email, date=date)
            db.session.add(check)
            db.session.commit()
            flash("Successful booking!", category='success')
        else:
            flash("This slot has been taken! Please choose another one")
            return render_template('appointment.html')

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('routes.confirmation'))

    selected_doctors = User.query.filter_by(User.doctor_name)
    return render_template('appointment.html', name=current_user.email, all_doctors=selected_doctors)


@auth.route('adminlogout')
def adminlogout():
    session.clear()
    return redirect("/")


@auth.route('/drdashboard')
def drdashboard():
    return render_template('drdashboard.html')


@auth.route('/drlogout')
@login_required
def drlogout():
    logout_user()
    flash("You have been Logged out!")
    return redirect('routes.drlogin')


@auth.route('/confirmation')
@login_required
def confirmation():
    return render_template('confirmation.html', name=current_user.id)


@login_required
@auth.route('/')
def history():
    return render_template('history')


@auth.route('/api/data')
@login_required
def data():
    appointmentID = current_user.id
    new2 = [current_user.to_dict() for current_user in Appointment.query.filter_by(appointmentID=appointmentID)]
    print(new2)
    return {
        'data': [current_user.to_dict() for current_user in Appointment.query.filter_by(appointmentID=appointmentID)]}


@auth.route('/')
@login_required
def schedules():
    return render_template('schedule')


@auth.route('/api/schedule')
@login_required
def schedule():
    doctorID = current_user.id
    new = [current_user.to_dict() for current_user in Appointment.query.filter_by(doctorID=doctorID)]
    print(new)

    return {
        'data': [current_user.to_dict() for current_user in Appointment.query.filter_by(doctorID=doctorID)]}


@auth.route('/drprofile')
@login_required
def drprofile():
    return render_template('drprofile.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='finalyearproject452@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@auth.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('routes.login'))
    return render_template('emailstuff/reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('emailstuff/reset_token.html', title='Reset Password', form=form)
