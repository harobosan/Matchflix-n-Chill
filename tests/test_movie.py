from project.db import Movie
from project.movie import create_movie, get_all_movies
from tests.factories.movies.clean_movies import clean_movies


def test_create_movie(app):
    create_movie('name','url')
    movie = Movie.query.filter_by(name='name').first()
    assert movie.image_url == 'url' and movie.name == 'name'

def test_get_all_movies(app):
    clean_movies()
    create_movie('name1','url1')
    create_movie('name2','url2')
    create_movie('name3','url3')
    movies = get_all_movies()
    print(movies)
    firstCondition = (movies[0].image_url == 'url1' and movies[0].name == 'name1')
    secondCondition = (movies[1].image_url == 'url2' and movies[1].name == 'name2')
    thirdCondition = (movies[2].image_url == 'url3' and movies[2].name == 'name3') 
    assert firstCondition and secondCondition and thirdCondition