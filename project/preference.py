"""Módulo responsável pelo gerenciamento das preferencias dos usuários"""

from .db import Preference, db_commit, db_add, db_del
from .movie import update_movie_weight, update_movie_score


def get_all_preferences():
    """
    Retorna uma lista com todas as preferências existentes no banco de dados.

    Return:
        preferences: Lista de preferências.
    """

    preferences = Preference.query.all()
    return preferences

def get_preference(uid, mid):
    """
    Retorna a preferência correspondente ao usuário e filme fornecidos.

    Parâmetros:
        uid: ID do usuário.

        mid: ID do filme.

    Return:
        preference: Objeto da preferência encontrada ou None.
    """

    preference = Preference.query.filter_by(uid=uid, mid=mid).first()
    return preference

def get_user_preferences(uid):
    """
    Retorna uma lista de filmes preferidos pelo usuário fornecido.

    Parâmetros:
        uid: ID do usuário.

    Return:
        user_preferences: Lista de IDs dos filmes preferidos pelo usuário.
    """

    preferences = Preference.query.filter_by(uid=uid)

    user_preferences = []
    for pref in preferences:
        user_preferences.append(pref.mid)

    return user_preferences

def get_movie_preferences(mid):
    """
    Retorna uma lista de usuários que preferiram o filme fornecido.

    Parâmetros:
        mid: ID do filme.

    Return:
        movie_preferences: Lista de IDs dos usuários que preferiram o filme.
    """

    preferences = Preference.query.filter_by(mid=mid)

    movie_preferences = []
    for pref in preferences:
        movie_preferences.append(pref.uid)

    return movie_preferences

def preference_exists(uid, mid):
    """
    Verifica se existe uma preferência do usuário pelo filme fornecidos.

    Parâmetros:
        uid: ID do usuário.

        mid: ID do filme.

    Return:
        bool: True se a preferência existe, False caso contrário.
    """

    return bool(get_preference(uid, mid))

def create_preference(uid, mid):
    """
    Cria uma nova preferência de um usuário por um filme.

    Parâmetros:
        uid: ID do usuário.

        mid: ID do filme.

    Return:
        preference: Objeto da preferência criada ou None.
    """

    if preference_exists(uid, mid):
        return None

    preference = Preference(uid=uid, mid=mid)
    db_add(preference)
    db_commit()
    update_movie(mid, 1)
    return preference

def delete_preference(uid, mid):
    """
    Deleta a preferência do usuário pelo filme.

    Parameters:
        uid: ID do usuário.

        mid: ID do filme.
    """

    preference = get_preference(uid, mid)

    if preference:
        db_del(preference)
        db_commit()
        update_movie(mid, -1)

def delete_user_preferences(uid):
    """
    Deleta todas as preferências do usuário.

    Parâmetros:
        uid: ID do usuário.
    """

    preferences = get_user_preferences(uid)

    if preferences:
        for mid in preferences:
            delete_preference(uid, mid)

def delete_movie_preferences(mid):
    """
    Deleta todas as preferências por um filme.

    Parâmetros:
        mid: ID do filme.
    """

    preferences = get_movie_preferences(mid)

    if preferences:
        for uid in preferences:
            delete_preference(uid, mid)

def calc_movie_weight(mid):
    """
    Calcula o peso de um filme com base nas preferências.

    Parâmetros:
        mid: ID do filme.

    Return:
        weight: Peso do filme.
    """

    preferences = len(get_all_preferences())
    movie_preferences = len(get_movie_preferences(mid))

    if preferences and movie_preferences:
        return round(1/(movie_preferences/preferences),1)

    return 0

def update_movie(mid, score):
    """
    Atualiza as informações de peso e pontuação do filme.

    Parâmetros:
        mid: ID do filme.

        score: Pontuação a ser adicionada ao filme.
    """

    preferences = get_all_preferences()

    for preference in preferences:
        update_movie_weight(preference.mid, calc_movie_weight(preference.mid))

    update_movie_weight(mid, calc_movie_weight(mid))
    update_movie_score(mid, score)
