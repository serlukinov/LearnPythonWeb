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
        tracks =  Track.query.all()
        sprints = Sprint.query.filter_by(track_id=1).all()

        context = {
            "tracks": tracks,
            "sprints": sprints,
        }

        return render_template('index.html', page_title=title, **context)


    # @app.route("/track/<int:pk>")
    # def track(pk):
    #     tracks = Track.query.all()
    #     sprints=current_sprint
    #     current_track = Track.query.filter_by(id=pk).first()
    #     current_sprint = Sprint.query.filter_by(track_id=current_track).first()
    #     current_lesson = Lesson.query.filter_by(sprint_id=current_sprint).first()

    #     context = {
    #         "tracks": tracks,
    #         "current_lesson": current_lesson,
    #         "current_sprint": current_sprint,
    #         "current_track": current_track,
    #     }

    #     return render_template('track.html', **context)

    return app



