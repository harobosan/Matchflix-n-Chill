from werkzeug.security import check_password_hash
from .db import db, User

def userAuthenticates(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return False
    return True
