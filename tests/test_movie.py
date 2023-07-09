from project.db import Movie
from project.movie import create_movie, delete_movie, get_all_movies, get_movie_list
from tests.factories.movies.clean_movies import clean_movies


def test_create_movie(app):
    clean_movies()
    create_movie('name','url')
    movie = Movie.query.filter_by(name='name').first()
    assert movie.id == 1 and movie.image_url == 'url' and movie.name == 'name'

def test_get_all_movies(app):
    clean_movies()
    create_movie('name1','url1')
    create_movie('name2','url2')
    create_movie('name3','url3')
    movies = get_all_movies()
    assert movies[0].id == 1 and movies[1].id == 2 and movies[2].id == 3

def test_get_movie_list(app):
    movies = get_movie_list([2,3])
    assert movies[0].id == 2 and movies[1].id == 3

def test_delete_movie(app):
    delete_movie('name2')
    movies = get_all_movies()
    moviesNames = []
    for i in movies:
        moviesNames.append(i.name)
    assert 'name2' not in moviesNames
