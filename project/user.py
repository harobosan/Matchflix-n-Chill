from werkzeug.security import generate_password_hash, check_password_hash
from .db import db, User

def get_all_users():
    users = User.query.all()
    return users

def get_user(email):
    user = User.query.filter_by(email=email).first()
    return user

def user_exists(email):
    return bool(get_user(email))

def create_user(email, username, password):
    if user_exists(email):
        return None

    hashed = generate_password_hash(password, method='sha256')
    user = User(email=email, username=username, password=hashed, authenticated=False)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(email):
    user = get_user(email)

    if user:
        db.session.delete(user)
        db.session.commit()

def authenticate_user(email, password):
    user = get_user(email)

    if user and check_password_hash(user.password, password):
        user.authenticated = True
        db.session.commit()
        return user

    return None

def disconnect_user(user):
    if user and user_exists(user.email):
        user.authenticated = False
        db.session.commit()
