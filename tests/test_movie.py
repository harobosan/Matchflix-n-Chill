from project.db import Movie
from project.movie import create_movie


def test_create_movie(client):
    create_movie('name','url')
    movie = Movie.query.filter_by(name='name').first()
    assert movie.image_url == 'url' and movie.name == 'name'