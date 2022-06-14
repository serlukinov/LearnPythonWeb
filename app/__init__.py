from app.model import db, Track, Sprint, Lesson, Content, User
from flask import Flask, render_template

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py') #указываем откуда брать параметры конфигурации
    db.init_app(app) #инициализируем базу данных

    admin = Admin(app, name='Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(Track, db.session))
    admin.add_view(ModelView(Sprint, db.session))
    admin.add_view(ModelView(Lesson, db.session))
    admin.add_view(ModelView(Content, db.session))
    admin.add_view(ModelView(User, db.session))

    @app.route("/")
    def index():
        title = "Learn Python Web"
        return render_template('index.html', page_title=title)

    return app



