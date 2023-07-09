"""Modulo responsável pelo gerenciamento dos filmes"""

from random import randint
from .db import Movie, db_commit, db_add, db_del

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_all_movies()
Assertivas de Entrada: Nenhuma pré-condição específica.
Assertiva de Saída: Retorna uma lista de todos os filmes existentes no banco de dados.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_all_movies():
    """
    Retorna uma lista com todos os filmes existentes no banco de dados.

    Return:
        movies: Lista de filmes.
    """

    movies = Movie.query.all()
    return movies

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_movie(name)
Assertivas de Entrada: O parâmetro 'name' é uma string
Assertivas de Saída: Retorna o objeto 'movie' homônimo ao parâmetro, caso este exista, e None, caso contrário.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_movie(name):
    """
    Retorna o filme correspondente ao nome fornecido.

    Parâmetros:
        name: Nome do filme.

    Returns:
        movie: Objeto do filme encontrado ou None.
    """

    movie = Movie.query.filter_by(name=name).first()
    return movie

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_movie_list(movie_list)
Assertivas de Entrada: O parâmetro 'movie_list' é um array de inteiros 
contendo IDs dos filmes no banco de dados.
Assertivas de Saída: Retorna um array de objetos 'Movie' correspondentes aos IDs fornecidos.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_movie_list(movie_list):
    """
    Retorna uma lista de filmes com base em uma lista de IDs.

    Parâmetros:
        movie_list: Lista de IDs dos filmes.

    Returns:
        movies: Lista de filmes encontrados.
    """

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
    """
    Verifica se um filme com o nome fornecido existe no banco de dados.

    Parâmetros:
        name: Nome do filme a ser verificado.

    Return:
        bool: True se o filme existe, False caso contrário.
    """

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
    """
    Cria um novo filme no banco de dados.

    Parâmetros:
        name: Nome do novo filme.
        image_url: URL da imagem do novo filme.

    Return:
        movie: Objeto do filme criado ou None.
    """

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
    """
    Deleta um filme do banco de dados.

    Parâmetros:
        name: Nome do filme a ser deletado.
    """

    movie = get_movie(name)

    if movie:
        db_del(movie)
        db_commit()

def generate_random_movie_name():
    """
    Gera um nome de filme aleatório.

    Return:
        random_name: Nome de filme aleatório.
    """

    i = randint(1, 300)
    return f"Filme {i}"

def seed_movies():
    """
    Popula o banco de dados com filmes.
    """

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
    """
    Retorna o peso do filme com base no ID fornecido.

    Parâmetros:
        mid: ID do filme.

    Return:
        weight: Peso do filme.
    """

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        return movie.weight

    return 0

def update_movie_weight(mid, weight):
    """
    Atualiza o peso do filme com base no ID fornecido.

    Parâmetros:
        mid: ID do filme.
        weight: Novo peso do filme.
    """

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        movie.weight = weight
        db_commit()

def update_movie_score(mid, score):
    """
    Atualiza a pontuação do filme com base no ID fornecido.

    Parâmetros:
        mid: ID do filme.
        score: Pontuação a ser adicionada ao filme.
    """

    movie = Movie.query.filter_by(id=mid).first()

    if movie:
        movie.score += score
        db_commit()
