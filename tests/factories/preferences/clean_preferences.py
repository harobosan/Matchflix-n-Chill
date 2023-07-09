from project.db import db_commit, Preference
from tests.factories.movies.clean_movies import clean_movies
from tests.factories.users.clean_users import clean_users

def clean_preferences():
    Preference.query.delete()
    db_commit()

def clean_users_movies_preferences():
    clean_preferences()
    clean_movies()
    clean_users()