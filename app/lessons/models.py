import os

from app.db import db
from sqlalchemy_utils import ChoiceType
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask import url_for

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    sprints = db.relationship(
        "Sprint",
        backref="track",
        lazy="dynamic",
    )

    def __repr__(self):
        return "<Track %r>" % self.name


class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    track_id = db.Column(
        db.Integer,
        db.ForeignKey("track.id"),
        nullable=False,
    )
    description = db.Column(db.Text, nullable=True)
    lessons = db.relationship(
        "Lesson",
        backref="sprint",
        lazy="dynamic",
    )
    contents = db.relationship(
        "Content",
        backref="sprint",
        lazy="dynamic",
    )

    # def github_reposit(self):
    #     return Content.query.filter_by(sprint_id=self.id)

    def __repr__(self):
        return "<Sprint %r>" % self.name


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sprint_id = db.Column(
        db.Integer,
        db.ForeignKey("sprint.id"),
        nullable=False,
    )
    description = db.Column(db.Text, nullable=True)
    contents = db.relationship(
        "Content",
        backref="lesson",
        lazy="dynamic",
    )

    def lesson_video(self):
        return Content.query.filter_by(lesson_id=self.id, type=Content.YOUTUBE)

    def __repr__(self):
        return "<Lesson %r>" % self.name


progress = db.Table(
    "progress",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("content_id", db.Integer, db.ForeignKey("content.id"), primary_key=True),
)


class Content(db.Model):
    YOUTUBE, SLIDES, GITHUB = range(1, 4)
    CONTENT_TYPE = (
        (YOUTUBE, "YOUTUBE"),
        (SLIDES, "SLIDES"),
        (GITHUB, "GITHUB"),
    )

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lesson.id"),
        nullable=True,
    )
    sprint_id = db.Column(
        db.Integer,
        db.ForeignKey("sprint.id"),
        nullable=True,
    )
    type = db.Column(ChoiceType(CONTENT_TYPE, impl=db.Integer()))
    image = db.Column(db.Unicode(128), nullable=True)

    def __repr__(self):
        return "<Content %r>" % self.image


class ContentModelView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        filename = form.thumbgen_filename(model.path)
        url = url_for('static', filename=filename)

        return Markup(f'<img src="{url}">')

    column_formatters = {
        'path': _list_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField(
            'Image',
            base_path=os.path.join(os.path.dirname(__file__), '..', 'static'),
            thumbnail_size=(320, 320, True),
        )
    }
