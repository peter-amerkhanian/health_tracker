from health_tracker import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Entry(db.Model):
    __tablename__ = "entry"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    hours_of_sleep = db.Column(db.Integer, unique=False, nullable=True)
    rest = db.Column(db.Integer, unique=False, nullable=True)
    fatigue = db.Column(db.Integer, unique=False, nullable=True)
    exercise = db.Column(db.Integer, unique=False, nullable=True)
    meditation = db.Column(db.String(10), unique=False, nullable=True)
    stress = db.Column(db.Integer, unique=False, nullable=True)
    emotion = db.Column(db.Integer, unique=False, nullable=True)
    comfort = db.Column(db.Integer, unique=False, nullable=True)
    arousal = db.Column(db.Integer, unique=False, nullable=True)
    headache = db.Column(db.String(10), unique=False, nullable=True)
    cannabis = db.Column(db.String(10), unique=False, nullable=True)
    morning = db.Column(db.String(50), unique=False, nullable=True)
    pills = db.Column(db.String(50), unique=False, nullable=True)

    def __repr__(self):
        return "<Entry('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')>".format(
            self.name,
            self.date,
            self.arousal,
            self.comfort,
            self.emotion,
            self.stress,
            self.meditation,
            self.exercise,
            self.fatigue,
            self.rest,
            self.hours_of_sleep,
            self.headache,
            self.cannabis,
            self.morning,
            self.pills)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
