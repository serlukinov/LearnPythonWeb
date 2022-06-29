from flask import (
    abort,
    Blueprint,
    current_app,
    flash,
    render_template,
    redirect,
    request,
    url_for,
)
from flask_login import current_user, login_required
from app.lessons.models import Lesson, Track


blueprint = Blueprint("lessons", __name__)


@blueprint.route("/")
def index():
    # progress = progress.query.filter_by(user_id=request.user.id).order_by('-created').first()  # для фильтрации прогресса для user
    lesson = Lesson.query.first()

    return redirect(url_for("lesson", pk=lesson.id))


@blueprint.route("/lesson/<int:pk>")
def lesson(pk):
    title = "Learn Python Web"
    tracks = Track.query.all()
    current_lesson = Lesson.query.filter_by(id=pk).first()

    context = {
        "tracks": tracks,
        "current_lesson": current_lesson,
    }

    return render_template("index.html", page_title=title, **context)


@blueprint.route("/track/<int:pk>")
def track(pk):
    track = Track.query.filter_by(id=pk).first()
    sprint = track.sprints.first()
    lesson = sprint.lessons.first()

    return redirect(url_for("lesson", pk=lesson.id))
