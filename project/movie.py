from .db import db,Movies
import random

def get_all_movies():
    movies = Movies.query.all()
    return movies

def get_movie(name):
    movie = Movies.query.filter_by(name=name).first()
    return movie

def movie_exists(name):
    if not get_movie(name):
        return False
    return True

def generate_random_movie_name():
    i = random.randint(1, 300) 
    return f"Filme {i}"

def seed_movies():
    for i in range(10):
        movie_name = f"Filme {i}"
        if movie_exists(movie_name):
            random_name = generate_random_movie_name()
            while movie_exists(random_name):
                random_name = generate_random_movie_name()
            movie = Movies(name=random_name, imageUrl="https://imagem")
        else:
            movie = Movies(name=movie_name, imageUrl="https://imagem")
        db.session.add(movie)
    db.session.commit()

def create_movie(name, imageUrl):
    if movie_exists(name):
        return 409 # http status Conflict
    movie = Movies(name=name, imageUrl=imageUrl)
    db.session.add(movie)
    db.session.commit()
    return 200 # http status OK

def delete_movie(name):
    movie = get_movie()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return 200  # http status OK
    return 404  # http status NOT-FOUND
