from app.db import db
from flask import Blueprint,  jsonify, render_template, redirect, request, url_for
from app.lessons.models import Lesson, Track, Content, SprintProgress, Sprint
from flask_admin import form
from flask_login import current_user

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
    current_sprint = Sprint.query.filter_by(id=current_lesson.sprint_id).first()
    lesson_list=[]
    for lesson in current_sprint.lessons:
        lesson_list.append(lesson)
    print(len(lesson_list))
    contents = Content.query.all()
    avatar = current_user.avatar

    context = {
        "tracks": tracks,
        "current_lesson": current_lesson,
        "contents": contents,
        "avatar": avatar,
    }

    return render_template("lessons/index.html", page_title=title, thumbnail=form.thumbgen_filename, **context)


@blueprint.route("/track/<int:pk>")
def track(pk):
    track = Track.query.filter_by(id=pk).first()
    sprint = track.sprints.first()
    lesson = sprint.lessons.first()

    return redirect(url_for("lessons.lesson", pk=lesson.id))


@blueprint.route('/api/progress/sprint/<int:pk>')
def learn_progress(pk):
    sprint = Sprint.query.filter_by(id=pk).first()
    sprint_progress = SprintProgress.query.filter_by(object=sprint).count()
    return jsonify({'sprint_progress': sprint_progress})


# @app.route('/api/likes/cactus/<int:pk>')
# def cactus_likes(pk):
#     cactus = Cactus.query.filter_by(id=pk).first()
#     likes = Like.query.filter_by(object=cactus).count()
#     return jsonify({'likes': likes})


@blueprint.route('/api/progress/sprint', methods=['POST'])
def create_learn_progress():
    if request.method == 'POST':
        data = request.json
        pk = data.get('pk')
        sprint = Sprint.query.filter_by(id=pk).first()
        progress = SprintProgress(object=sprint)
        db.session.add(progress)
        db.session.commit()
        return jsonify({'detail': 'liked'})


# @app.route('/api/likes/cactus', methods=['POST'])
# def create_cactus_likes():
#     if request.method == 'POST':
#         data = request.json
#         pk = data.get('pk')
#         cactus = Cactus.query.filter_by(id=pk).first()
#         like = Like(object=cactus)
#         db.session.add(like)
#         db.session.commit()
#         return jsonify({'detail': 'liked'})