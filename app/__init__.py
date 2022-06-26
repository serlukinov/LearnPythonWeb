from app.model import db, Track, Sprint, Lesson, Content, User, progress
from flask import Flask, redirect, render_template, request, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # указываем откуда брать параметры конфигурации
    db.init_app(app)  # инициализируем базу данных
    migrate = Migrate(app, db)

    admin = Admin(app, name='Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(Track, db.session))
    admin.add_view(ModelView(Sprint, db.session))
    admin.add_view(ModelView(Lesson, db.session))
    admin.add_view(ModelView(Content, db.session))
    admin.add_view(ModelView(User, db.session))


    @app.route("/")
    def index():
        # progress = progress.query.filter_by(user_id=request.user.id).order_by('-created').first()  # для фильтрации прогресса для user
        lesson = Lesson.query.first()

        return redirect(url_for('lesson', pk=lesson.id))


    @app.route("/lesson/<int:pk>")
    def lesson(pk):
        title = "Learn Python Web"
        tracks = Track.query.all()
        lesson = Lesson.query.filter_by(id=pk).first()

        context = {
            "tracks": tracks,
            "current_lesson": lesson,
        }

        return render_template('index.html', page_title=title, **context)


    @app.route("/track/<int:pk>")
    def track(pk):
        track = Track.query.filter_by(id=pk).first()
        sprint = track.sprints.first()
        lesson = sprint.lessons.first()

        return redirect(url_for('lesson', pk=lesson.id))

    return app



