from project.db import db_commit, Movie

def clean_movies():
    Movie.query.delete()
    db_commit()