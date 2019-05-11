from reflection import db, login_manager
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='propic.jpg')
    reflects = db.relationship('Reflect', backref='author', lazy=True)


class Reflect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reflect = db.Column(db.String(140), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
