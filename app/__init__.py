from flask import Flask, session, abort, render_template
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from app.extensions import db
from os import path
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user

DB_NAME = "database.db"
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'finalyearproject452@gmail.com'
app.config['MAIL_PASSWORD'] = 'nilajcekrdvbdpad'
bcrypt = Bcrypt(app)
mail = Mail(app)


def create_app():
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Appointment, Slots

    admin = Admin(app)

    class SecureModelView(ModelView):
        def is_accessible(self):
            if "logged_in" in session:
                return True
            else:
                abort(403)

    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Appointment, db.session))
    admin.add_view(SecureModelView(Slots, db.session))
    admin.add_link(MenuLink(name='Logout', category='', url='/adminlogout'))

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_view = "auth.drlogin"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# return Doctor.query.get(int(id))


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")

