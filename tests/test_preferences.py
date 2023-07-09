from project.preference import create_preference
from project.movie import create_movie, delete_movie
from project.user import create_user, delete_user
from tests.factories.movies.clean_movies import clean_movies
from tests.factories.users.clean_users import clean_users


def test_create_preference(app):
    movie = create_movie('nametest','url')
    user = create_user('teste5@gmail.com', 'teste5','senha5')
    preference = create_preference(user.id,movie.id)
    assert preference.mid == movie.id and preference.uid == user.id
    delete_movie('nametest')
    delete_user('teste5@gmail.com')
