"""movie"""

from random import randint
from .db import Movie, db_commit, db_add, db_del


def get_all_movies():
    """get_all_movies"""

    movies = Movie.query.all()
    return movies

def get_movie(name):
    """get_movie"""

    movie = Movie.query.filter_by(name=name).first()
    return movie

def movie_exists(name):
    """movie_exists"""

    return bool(get_movie(name))

def create_movie(name, image_url):
    """create_movie"""

    if movie_exists(name):
        return None

    movie = Movie(name=name, image_url=image_url)
    db_add(movie)
    db_commit()
    return movie

def delete_movie(name):
    """delete_movie"""

    movie = get_movie(name)

    if movie:
        db_del(movie)
        db_commit()

def generate_random_movie_name():
    """generate_random_movie_name"""

    i = randint(1, 300)
    return f"Filme {i}"

def seed_movies():
    """seed_movies"""

    for i in range(10):
        movie_name = f"Filme {i}"

        if movie_exists(movie_name):
            random_name = generate_random_movie_name()
            while movie_exists(random_name):
                random_name = generate_random_movie_name()
            movie = Movie(name=random_name, image_url="https://imagem")
        else:
            movie = Movie(name=movie_name, image_url="https://imagem")

        db_add(movie)

    db_commit()
