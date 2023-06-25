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

class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship('User', backref='admin')