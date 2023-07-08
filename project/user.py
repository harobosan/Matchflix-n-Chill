"""user"""

from werkzeug.security import generate_password_hash, check_password_hash
from .db import User, db_commit, db_add, db_del


def get_all_users():
    """get_all_users"""

    users = User.query.all()
    return users

def get_user(email):
    """get_user"""

    user = User.query.filter_by(email=email).first()
    return user

def user_exists(email):
    """user_exists"""

    return bool(get_user(email))

def create_user(email, username, password):
    """create_user"""

    if user_exists(email):
        return None

    hashed = generate_password_hash(password, method='sha256')
    user = User(email=email, username=username, password=hashed, authenticated=False)
    db_add(user)
    db_commit()
    return user

def delete_user(email):
    """delete_user"""

    user = get_user(email)

    if user:
        db_del(user)
        db_commit()

def authenticate_user(email, password):
    """authenticate_user"""

    user = get_user(email)

    if user and check_password_hash(user.password, password):
        user.authenticated = True
        db_commit()
        return user

    return None

def disconnect_user(user):
    """disconnect_user"""

    if user and user_exists(user.email):
        user.authenticated = False
        db_commit()
