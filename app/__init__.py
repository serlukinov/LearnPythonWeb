from flask import Flask, flash, render_template, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate

from app.db import db
from app.lessons.models import Content, Lesson, Sprint, Track, progress
from app.users.models import User

from app.admins.views import blueprint as admin_blueprint
from app.lessons.views import blueprint as lessons_blueprint
from app.users.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(lessons_blueprint)
    app.register_blueprint(user_blueprint)

    admin = Admin(app, name="Admin", template_mode="bootstrap4")
    admin.add_view(ModelView(Track, db.session))
    admin.add_view(ModelView(Sprint, db.session))
    admin.add_view(ModelView(Lesson, db.session))
    admin.add_view(ModelView(Content, db.session))
    admin.add_view(ModelView(User, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
