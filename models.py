from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(128), nullable=False)
    vacancies = db.relationship('Vacancy', backref='author', lazy=True)

    @property
    def password(self):
        raise AttributeError('Reading unhashed password is prohibited!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Vacancy {self.title}>"
