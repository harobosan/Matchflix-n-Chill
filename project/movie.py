"""movie"""

from random import randint
from .db import Movie, db_commit, db_add, db_del

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_all_movies()
Assertivas de Entrada: Nenhuma pré-condição específica.
Assertiva de Saída: Retorna uma lista de todos os filmes existentes no banco de dados.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_all_movies():
    """get_all_movies"""

    movies = Movie.query.all()
    return movies

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_movie(name)
Assertivas de Entrada: O parâmetro 'name' é uma string
Assertivas de Saída: Retorna o objeto 'movie' homônimo ao parâmetro, caso este exista, e None, caso contrário.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_movie(name):
    """get_movie"""

    movie = Movie.query.filter_by(name=name).first()
    return movie

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_movie_list(movie_list)
Assertivas de Entrada: O parâmetro 'movie_list' é um array de inteiros 
contendo IDs dos filmes no banco de dados.
Assertivas de Saída: Retorna um array de objetos 'Movie' correspondentes aos IDs fornecidos.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_movie_list(movie_list):
    """get_movie_list"""

    movies = []
    for mid in movie_list:
        movie = Movie.query.filter_by(id=mid).first()

        if movie:
            movies.append(movie)

    return movies

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: movie_exists(name)
Assertivas de Entrada: O parâmetro 'name' é uma string
Assertivas de Saída: Se existe um filme com nome == name no banco
                        Retorna True
                     Senão
                        Retorna False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def movie_exists(name):
    """movie_exists"""

    return bool(get_movie(name))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: create_movie(name, image_url)
Assertivas de Entrada: Os parâmetro 'name' e 'image_url' devem ser strings
Assertivas de Saída: Se existe um filme de nome == name
                        Retorna None
                     Senão
                        Será adicionada ao banco de dados um objeto 'Movie', 
                        tendo 'name' e 'image_url' como atributos.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_movie(name, image_url):
    """create_movie"""

    if movie_exists(name):
        return None

    movie = Movie(name=name, image_url=image_url, weight=0, score=0)
    db_add(movie)
    db_commit()
    return movie

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_movie(name)
Assertivas de Entrada: O parâmetro 'name' é uma string
Assertivas de Saída: Se o filme existe no banco de dados, ele será excluído.
Caso contrário, o estado anterior será igual ao atual.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

def get_movie_weight(mid):
    """get_movie_weight"""

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        return movie.weight

    return 0

def update_movie_weight(mid, weight):
    """update_movie_weight"""

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        movie.weight = weight
        db_commit()

def update_movie_score(mid, score):
    """update_movie_score"""

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        movie.score += score
        db_commit()
