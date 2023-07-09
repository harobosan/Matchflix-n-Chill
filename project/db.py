"""db"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    uid_1 = db.relationship(
        'Relationship',
        foreign_keys='Relationship.uid_1',
        cascade='all,delete'
    )

    uid_2 = db.relationship(
        'Relationship',
        foreign_keys='Relationship.uid_2',
        cascade='all,delete'
    )

    sender = db.relationship(
        'UserMessages',
        foreign_keys='UserMessages.sender',
        cascade='all_delete'
    )

    receiver = db.relationship(
        'UserMessages',
        foreign_keys='UserMessages.receiver',
        cascade='all_delete'
    )

class Admin(db.Model):
    """Admin"""

    uid = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)

    user = db.relationship(
        'User',
        backref=db.backref(
            'Admin',
            cascade='all,delete'
        )
    )

class Movie(db.Model):
    """Movie"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

class Preference(db.Model):
    """Preference"""

    uid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)

    user = db.relationship(
        'User',
        backref=db.backref(
            'Preference',
            cascade='all,delete'
        )
    )
    movie = db.relationship(
        'Movie',
        backref=db.backref(
            'Preference',
            cascade='all,delete'
        )
    )

class Relationship(db.Model):
    """Relationship"""

    uid_1 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    uid_2 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.Boolean)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    text = db.Column(db.String(250))

class UserMessages(db.Model):
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey('messages.id'), primary_key=True)

def db_commit():
    """db_commit"""

    db.session.commit()

def db_add(item):
    """db_add"""

    db.session.add(item)

def db_del(item):
    """db_del"""

    db.session.delete(item)
