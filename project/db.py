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
        cascade='all,delete'
    )

    receiver = db.relationship(
        'UserMessages',
        foreign_keys='UserMessages.receiver',
        cascade='all,delete'
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
    weight = db.Column(db.Integer)
    score = db.Column(db.Integer)

class Preference(db.Model):
    """Preference"""
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    mid = db.Column(db.Integer, db.ForeignKey('movie.id'))

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
    id = db.Column(db.Integer, primary_key=True)
    uid_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    uid_2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Boolean)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    text = db.Column(db.String(250))

class UserMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    mid = db.Column(db.Integer, db.ForeignKey('messages.id'))

def db_commit():
    """db_commit"""

    db.session.commit()

def db_add(item):
    """db_add"""

    db.session.add(item)

def db_del(item):
    """db_del"""

    db.session.delete(item)

def clean_db():
    """clean_db"""
    # Exclui todos os registros da tabela User
    User.query.delete()

    # Exclui todos os registros da tabela Messages
    Messages.query.delete()

    # Exclui todos os registros da tabela Preference
    Preference.query.delete()

    # Exclui todos os registros da tabela Movie
    Movie.query.delete()

    # Comita as alterações no banco de dados
    db_commit()
