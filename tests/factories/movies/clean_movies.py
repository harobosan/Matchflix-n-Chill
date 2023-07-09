from project.db import Movie, db_commit

def clean_movies():
    Movie.query.delete()
    db_commit()