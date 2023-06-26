from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

class UserAdmin(db.Model):
    id = db.Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    user = relationship('User', backref='admin')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

class UserPreference(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    user = relationship('User', backref='preferences')
    movieId = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True)
    movie = relationship('Movie', backref='preferences')
