from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    sprint = db.relationship('Sprint', backref='track', lazy=True)

    def __repr__(self):
        return '<Track %r>' % self.name


class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('track_id'), 
        nullable=False)
    description = db.Column(db.Text, nullable=True)
    lesson = db.relationship('Lesson', backref='sprint', lazy=True)

    def __repr__(self):
        return '<Sprint %r>' % self.name


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint_id'), 
        nullable=False)
    description = db.Column(db.Text, nullable=True)
    content = db.relationship('Content', backref='lesson', lazy=True)

    def __repr__(self):
        return '<Lesson %r>' % self.name


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson_id'), 
        nullable=False)
    type = db.Column(db.Integer,  nullable=False)

    def __repr__(self):
        return '<Content %r>' % self.url


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_pass = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)
    telegram = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


progress = db.Table('progress',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True),
    db.Column('track_progress', db.Integer, nullable=False)
)