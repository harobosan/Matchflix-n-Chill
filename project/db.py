"""Banco de Dados"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Classe para representar um usuário.        
    """

    id = db.Column(db.Integer, primary_key=True)
    """
    id (int): ID do usuário.
    """
    email = db.Column(db.String(100), unique=True)
    """
    email (str): E-mail do usuário.
    """
    username = db.Column(db.String(1000))
    """
    username (str): Nome de usuário.
    """
    password = db.Column(db.String(100))
    """
    password (str): Senha do usuário.
    """
    authenticated = db.Column(db.Boolean, default=False)
    """
    authenticated (bool): Indica se o usuário está autenticado.
    """

    uid_1 = db.relationship(
        'Relationship',
        foreign_keys='Relationship.uid_1',
        cascade='all,delete'
    )
    """
    uid_1 (Relationship): Relacionamentos em que o usuário é o uid_1.
    """

    uid_2 = db.relationship(
        'Relationship',
        foreign_keys='Relationship.uid_2',
        cascade='all,delete'
    )
    """
    uid_2 (Relationship): Relacionamentos em que o usuário é o uid_2.
    """

    sender = db.relationship(
        'UserMessages',
        foreign_keys='UserMessages.sender',
        cascade='all,delete'
    )
    """
    sender (UserMessages): Mensagens enviadas pelo usuário.
    """

    receiver = db.relationship(
        'UserMessages',
        foreign_keys='UserMessages.receiver',
        cascade='all,delete'
    )
    """
    receiver (UserMessages): Mensagens recebidas pelo usuário.
    """

class Admin(db.Model):
    """
        Classe responsável pelos usuários administradores
    """

    uid = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    """
    user (User): Usuário associado ao administrador.
    """
    user = db.relationship(
        'User',
        backref=db.backref(
            'Admin',
            cascade='all,delete'
        )
    )

class Movie(db.Model):
    """Dados que representam informações sobre os filmes"""

    id = db.Column(db.Integer, primary_key=True)
    """
    id (int): ID do filme (chave primária).
    """
    name = db.Column(db.String(100))
    """
    name (str): Nome do filme.
    """
    image_url = db.Column(db.String(200))
    """
    image_url (str): URL da imagem do filme.
    """

class Preference(db.Model):
    """ Classe que representa as preferências dos usuários em relação aos filmes."""

    uid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    """
    uid (int): ID do usuário (chave primária composta).
    """
    mid = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    """
    mid (int): ID do filme (chave primária composta).
    """

    user = db.relationship(
        'User',
        backref=db.backref(
            'Preference',
            cascade='all,delete'
        )
    )
    """
    user (User): Usuário associado à preferência.
    """
    movie = db.relationship(
        'Movie',
        backref=db.backref(
            'Preference',
            cascade='all,delete'
        )
    )
    """
    movie (Movie): Filme associado à preferência.
    """

class Relationship(db.Model):
    """Classe que representa os relacionamentos entre os usuários."""

    uid_1 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    """
    uid_1 (int): ID do primeiro usuário no relacionamento (chave primária composta).
    """
    uid_2 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    """
    uid_2 (int): ID do segundo usuário no relacionamento (chave primária composta).
    """
    status = db.Column(db.Boolean)
    """
    status (bool): Indica o status do relacionamento.
    """

class Messages(db.Model):
    """
    Classe que representa as mensagens.
    """
    id = db.Column(db.Integer, primary_key=True)
    """
    id (int): ID da mensagem (chave primária).
    """
    date = db.Column(db.Date)
    """
    date (Date): Data da mensagem.
    """
    text = db.Column(db.String(250))
    """
    text (str): Texto da mensagem.
    """

class UserMessages(db.Model):
    """
    Classe que representa as mensagens trocadas entre usuários.
    """
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    """
    sender (int): ID do remetente da mensagem (chave primária composta).
    """
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    """
    receiver (int): ID do destinatário da mensagem (chave primária composta).
    """
    mid = db.Column(db.Integer, db.ForeignKey('messages.id'), primary_key=True)
    """
    mid (int): ID da mensagem (chave primária composta).
    """

def db_commit():
    """
    Realiza o commit das alterações no banco de dados.
    """
    db.session.commit()

def db_add(item):
    """
    Adiciona um item no banco de dados.

    Parâmetros:
        item: Item a ser adicionado no banco de dados.
    """
    db.session.add(item)

def db_del(item):
    """
    Deleta um item do banco de dados.

    Parâmetros:
        item: Item a ser deletado do banco de dados.
    """

    db.session.delete(item)

def clean_db():
    """
    Exclui todos os registros da tabela User
    """
    User.query.delete()
    """
    Exclui todos os registros da tabela Messages
    """
    Messages.query.delete()
    """
    Exclui todos os registros da tabela Preference
    """
    Preference.query.delete()
    """
    Exclui todos os registros da tabela Movie
    """
    Movie.query.delete()
    """
    Realiza o commit das alterações no banco de dados
    """
    db_commit()
