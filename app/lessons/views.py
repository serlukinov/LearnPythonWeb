from flask import Blueprint, render_template, redirect, url_for
from app.lessons.models import Lesson, Sprint, Track
from flask_admin import form

blueprint = Blueprint("lessons", __name__, url_prefix='/lessons')


@blueprint.route("/")
def index():
    # progress = progress.query.filter_by(user_id=request.user.id).order_by('-created').first()  # для фильтрации прогресса для user
    lesson = Lesson.query.first()

    return redirect(url_for("lessons.lesson", pk=lesson.id))


@blueprint.route("/lesson/<int:pk>")
def lesson(pk):
    title = "Learn Python Web"
    tracks = Track.query.all()
    current_lesson = Lesson.query.filter_by(id=pk).first()

    context = {
        "tracks": tracks,
        "current_lesson": current_lesson,

    }

    return render_template("lessons/index.html", page_title=title, thumbnail=form.thumbgen_filename, **context)


@blueprint.route("/track/<int:pk>")
def track(pk):
    track = Track.query.filter_by(id=pk).first()
    sprint = track.sprints.first()
    lesson = sprint.lessons.first()

    return redirect(url_for("lessons.lesson", pk=lesson.id))
