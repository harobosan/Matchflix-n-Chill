"""preference"""

from .db import Preference, db_commit, db_add, db_del


def get_all_preferences():
    """get_all_preferences"""

    preferences = Preference.query.all()
    return preferences

def get_preference(uid, mid):
    """get_preference"""

    preference = Preference.query.filter_by(uid=uid, mid=mid).first()
    return preference

def get_user_preferences(uid):
    """get_user_preferences"""

    preferences = Preference.query.filter_by(uid=uid)
    return preferences

def get_movie_preferences(mid):
    """get_movie_preferences"""

    preferences = Preference.query.filter_by(mid=mid)
    return preferences

def preference_exists(uid, mid):
    """preference_exists"""

    return bool(get_preference(uid, mid))

def create_preference(uid, mid):
    """create_preference"""

    if preference_exists(uid, mid):
        return None

    preference = Preference(uid=uid, mid=mid)
    db_add(preference)
    db_commit()
    return preference

def delete_preference(uid, mid):
    """delete_preference"""

    preference = get_preference(uid, mid)

    if preference:
        db_del(preference)
        db_commit()

def delete_user_preferences(uid):
    """delete_user_preferences"""

    preferences = get_user_preferences(uid)

    if preferences:
        for preference in preferences:
            db_del(preference)
        db_commit()

def delete_movie_preferences(mid):
    """delete_movie_preferences"""

    preferences = get_movie_preferences(mid)

    if preferences:
        for preference in preferences:
            db_del(preference)
        db_commit()
