"""preference"""

from .db import Preference, db_commit, db_add, db_del
from .movie import update_movie_weight, update_movie_score


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

    user_preferences = []
    for pref in preferences:
        user_preferences.append(pref.mid)

    return user_preferences

def get_movie_preferences(mid):
    """get_movie_preferences"""

    preferences = Preference.query.filter_by(mid=mid)

    movie_preferences = []
    for pref in preferences:
        movie_preferences.append(pref.uid)

    return movie_preferences

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
    update_movie(mid, 1)
    return preference

def delete_preference(uid, mid):
    """delete_preference"""

    preference = get_preference(uid, mid)

    if preference:
        db_del(preference)
        db_commit()
        update_movie(mid, -1)

def delete_user_preferences(uid):
    """delete_user_preferences"""

    preferences = get_user_preferences(uid)

    if preferences:
        for mid in preferences:
            delete_preference(uid, mid)

def delete_movie_preferences(mid):
    """delete_movie_preferences"""

    preferences = get_movie_preferences(mid)

    if preferences:
        for uid in preferences:
            delete_preference(uid, mid)

def calc_movie_weight(mid):
    """calc_movie_weight"""

    preferences = len(get_all_preferences())
    movie_preferences = len(get_movie_preferences(mid))

    if preferences and movie_preferences:
        return round(1/(movie_preferences/preferences),1)

    return 0

def update_movie(mid, score):
    """update_movie"""

    preferences = get_all_preferences()

    for preference in preferences:
        update_movie_weight(preference.mid, calc_movie_weight(preference.mid))

    update_movie_weight(mid, calc_movie_weight(mid))
    update_movie_score(mid, score)
