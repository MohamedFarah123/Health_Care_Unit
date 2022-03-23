from flask import Flask, session, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Doctors, Appointment, Slots

    admin = Admin(app)

    class SecureModelView(ModelView):
        def is_accessible(self):
            if "logged_in" in session:
                return True
            else:
                abort(403)

    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Doctors, db.session))
    admin.add_view(SecureModelView(Appointment, db.session))
    admin.add_view(SecureModelView(Slots, db.session))

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")

