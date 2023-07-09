from project.preference import create_preference, get_all_preferences
from project.movie import create_movie, delete_movie
from project.user import create_user, delete_user
from tests.factories.movies.clean_movies import clean_movies
from tests.factories.users.clean_users import clean_users
from tests.factories.preferences.clean_preferences import clean_preferences


def test_create_preference(app):
    clean_movies()
    clean_users()
    clean_preferences()
    movie = create_movie('nametest','url')
    user = create_user('teste5@gmail.com', 'teste5','senha5')
    preference = create_preference(user.id,movie.id)
    assert preference.mid == movie.id and preference.uid == user.id

def test_get_all_preferences(app):
    clean_movies()
    clean_users()
    clean_preferences()
    create_movie('nametest1', 'url')
    create_movie('nametest2', 'url')
    create_user('teste6@gmail.com', 'teste6', 'senha6')
    create_preference(1, 1)
    create_preference(1, 2)
    preferences = get_all_preferences()
    assert len(preferences) == 2