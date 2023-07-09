from project.preference import (calc_movie_weight, create_preference, delete_movie_preferences,
    delete_preference, delete_user_preferences, get_all_preferences, get_movie_preferences,
    get_user_preferences)
from project.movie import create_movie
from project.user import create_user
from tests.factories.preferences.clean_preferences import (
    clean_users_movies_preferences)


def generate_preferences():
    user = create_user('teste6@gmail.com', 'teste6', 'senha6')
    movie = create_movie('nametest1', 'url')
    create_movie('nametest2', 'url')
    create_preference(1, 1)
    create_preference(1, 2)
    return [user.id, movie.id]

def test_create_preference(app):
    clean_users_movies_preferences()
    movie = create_movie('nametest','url')
    user = create_user('teste5@gmail.com', 'teste5','senha5')
    preference = create_preference(user.id,movie.id)
    assert preference.mid == movie.id and preference.uid == user.id

def test_get_all_preferences(app):
    clean_users_movies_preferences()
    generate_preferences()
    preferences = get_all_preferences()
    assert len(preferences) == 2

def test_get_user_preferences(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    preferences = get_user_preferences(returnal[0])
    assert len(preferences) == 2

def test_get_movie_preferences(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    preferences = get_movie_preferences(returnal[1])
    assert len(preferences) == 1

def test_delete_preference(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    length1 = len(get_all_preferences())
    delete_preference(returnal[0],returnal[1])
    length2 = len(get_all_preferences())
    assert length1 == length2+1

def test_delete_user_preferences(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    delete_user_preferences(returnal[0])
    length = len(get_user_preferences(returnal[0]))
    assert length == 0

def test_delete_movie_preferences(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    delete_movie_preferences(returnal[1])
    length = len(get_movie_preferences(returnal[1]))
    assert length == 0

def test_calc_movie_weight(app):
    clean_users_movies_preferences()
    returnal = generate_preferences()
    weight = calc_movie_weight(returnal[1])
    assert weight == 2