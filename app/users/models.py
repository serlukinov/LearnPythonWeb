from app.db import db
from app.lessons.models import progress
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), index=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.Unicode(128), nullable=True)
    telegram = db.Column(db.String, nullable=True)

    progress = db.relationship(
        "Content",
        secondary=progress,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return "<User name {} id={}>".format(self.username, self.id)
