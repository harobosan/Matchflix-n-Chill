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
    id = db.Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', backref='admin')

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    imageUrl = db.Column(db.String(200))

class UserPreferences(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    user = relationship('User', backref='preferences')
    movieId = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True)
    movie = relationship('Movies', backref='preferences')