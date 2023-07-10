"""user"""

from werkzeug.security import generate_password_hash, check_password_hash
from .db import User, Admin, db_commit, db_add, db_del
from .movie import get_movie_weight
from .preference import get_user_preferences, get_movie_preferences
from .relationship import get_relationship, get_user_relationships


def get_all_users():
    """get_all_users"""

    users = User.query.all()
    return users

def get_user(email):
    """get_user"""

    user = User.query.filter_by(email=email).first()
    return user

def get_user_list(user_list):
    """get_user_list"""

    users = []
    for uid in user_list:
        user = User.query.filter_by(id=uid).first()

        if user:
            users.append(user)

    return users

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

def update_email(user, email):
    """update_email"""

    if get_user(email):
        return None

    user.email = email
    db_commit()
    return user

def update_username(user, username):
    """update_username"""

    user.username = username
    db_commit()
    return user

def update_password(user, password):
    """update_password"""

    hashed = generate_password_hash(password, method='sha256')
    user.password = hashed
    db_commit()
    return user

def get_admin(uid):
    """get_admin"""

    admin = Admin.query.filter_by(uid=uid).first()
    return admin

def is_admin(uid):
    """is_admin"""

    return bool(get_admin(uid))

def set_admin(uid):
    """set_admin"""

    if is_admin(uid):
        return None

    admin = Admin(uid=uid)
    db_add(admin)
    db_commit()
    return admin

def remove_admin(uid):
    """remove_admin"""

    admin = get_admin(uid)

    if admin:
        db_del(admin)
        db_commit()

def sort_matches(user):
    """sort_matches"""

    return user[1]

def calc_matches(uid):
    """calc_matches"""

    user_preferences = get_user_preferences(uid)
    user_relationships = get_user_relationships(uid)

    movies_list = []
    for mid in user_preferences:
        movies_list.append([get_movie_weight(mid), get_movie_preferences(mid)])

    user_matches = []
    user_scores = []
    for movie_pair in movies_list:
        for user in movie_pair[1]:
            if user != uid and not user_relationships.count(user):
                if user_matches.count(user):
                    user_scores[user_matches.index(user)] += movie_pair[0]
                else:
                    user_matches.append(user)
                    user_scores.append(movie_pair[0])

    recommendations = []
    for count, user in enumerate(user_matches):
        recommendations.append([user, user_scores[count]])

    recommendations.sort(reverse=True, key=sort_matches)
    return recommendations

def get_relationship_lists(uid):
    """get_relationship_lists"""

    relationships = get_user_relationships(uid)

    friends = []
    pending = []
    requests = []
    for user in relationships:
        relationship = get_relationship(uid, user)

        if relationship.status:
            friends.append(User.query.filter_by(id=user).first())
        else:
            if relationship.uid_1 == uid:
                pending.append(User.query.filter_by(id=user).first())
            else:
                requests.append(User.query.filter_by(id=user).first())

    matches = calc_matches(uid)
    recommendations = []
    for match in matches:
        recommendations.append([User.query.filter_by(id=match[0]).first(), match[1]])

    return [friends, pending, requests, recommendations]
