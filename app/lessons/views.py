from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_admin import form
from flask_login import current_user

from app import User
from app.db import db
from app.lessons.models import Content, Lesson, Sprint, Track, progress

blueprint = Blueprint("lessons", __name__, url_prefix='/lessons')


@blueprint.route("/")
def index():
    lesson = Lesson.query.first()

    return redirect(url_for("lessons.lesson", pk=lesson.id))


@blueprint.route("/lesson/<int:pk>")
def lesson(pk):
    title = "Learn Python Web"
    tracks = Track.query.all()
    current_lesson = Lesson.query.filter_by(id=pk).first()
    contents = Content.query.all()
    avatar = current_user.avatar

    sprint = Sprint.query.filter_by(id=current_lesson.sprint_id).first()

    lesson_ids = [id[0] for id in Lesson.query.filter_by(sprint_id=sprint.id).with_entities(Lesson.id).all()]
    total_lesson_content_number = Content.query.filter(Content.lesson_id.in_(lesson_ids)).count()
    content_ids = [id[0] for id in Content.query.filter_by(lesson_id=pk).with_entities(Content.id).all()]
    completed_lesson_content_number = len(User.query.filter_by(id=current_user.id).first().progress)
    sprint_progress = (completed_lesson_content_number / total_lesson_content_number) * 100

    context = {
        "tracks": tracks,
        "current_lesson": current_lesson,
        "contents": contents,
        "avatar": avatar,
        "lesson_ids": lesson_ids,
        "content_ids": content_ids,
        "total_lesson_content_number": total_lesson_content_number,
        "completed_lesson_content_number": completed_lesson_content_number,
        "sprint_progress": sprint_progress,
    }

    return render_template("lessons/index.html", page_title=title, thumbnail=form.thumbgen_filename, **context)


@blueprint.route("/track/<int:pk>")
def track(pk):
    track = Track.query.filter_by(id=pk).first()
    sprint = track.sprints.first()
    lesson = sprint.lessons.first()

    return redirect(url_for("lessons.lesson", pk=lesson.id))


@blueprint.route('/progress/<int:pk>', methods=['POST'])
def create_lesson_progress(pk):
    if request.method == 'POST':
        query = progress.select().where(progress.c.user_id == current_user.id, progress.c.content_id == pk)
        lesson_progress = db.session.execute(query).first()
        if not lesson_progress:
            statement = progress.insert().values(user_id=current_user.id, content_id=pk)
            db.session.execute(statement)
            db.session.commit()
        return jsonify({'detail': 'completed'})
