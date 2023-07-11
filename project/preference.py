"""Módulo responsável pelo gerenciamento das preferencias dos usuários"""

from .db import Preference, db_commit, db_add, db_del
from .movie import update_movie_weight, update_movie_score

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_all_preferences()
Assertivas de Entrada:
    Nenhuma especifíca
Assertivas de Saída:
    Retorna uma lista de strings contendo as preferências.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_all_preferences():
    """
    Retorna uma lista com todas as preferências existentes no banco de dados.

    Return:
        preferences: Lista de preferências.
    """

    preferences = Preference.query.all()
    return preferences

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_preference(uid,mid)
Assertivas de Entrada:
Há no banco de dados um, e somente um objeto 'User' tal que:
    user.id == uid
Há no banco de dados um, e somente um objeto 'Movie' tal que:
    movie.id  == mid
Assertivas de Saída:
    movie.id = mid
    Se o Usuário tem 'movie.id' como preferência
        Retorna movie.id
    Senão
        Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_user_preferences()
Assertivas de Entrada:
Há no banco de dados um, e somente um, usuário com id = uid
Assertivas de Saída:
Se preferences = []
    Retorna uma lista vazia
Senão
    Retorna uma lista de inteiros contendo os IDs dos filmes 
    preferidos pelo usuário.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_movie_preferences(mid)
Assertivas de Entrada:
Há no banco de dados um, e somente um atributo movie.id = mid
Assertivas de Saída:
Se preferences = []
    Retorna uma lista vazia
Senão
    Retorna uma lista de inteiros contendo os IDs dos usuários
    que tem o filme como preferido.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: preference_exists(uid,mid)
Ver 'get_preference(uid,mid)' para assertivas.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: create_preference(uid,mid)
Assertivas de Entrada:
Há, no banco de dados, objetos 'User' e 'Movie' com atributos user.id = id, 
movie.id = id únicos
Assertivas de Saída:
Se preference_exists(uid,mid) == True
    Retorna None
Senão
    É criado um objeto 'Preference' com atribuitos uid e mid
    O banco de dados é atualizado com o objeto
    É atríbuido peso 1 ao filme
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_preference(uid,mid)
Assertivas de Entrada: 
Ver assertivas de entrada de get_preferece(uid,mid)
Assertivas de Saída:
Se CondRet == OK
    Há preferência é deletada da lista de preferências do usuário
    O banco de dados é atualizado
    movie.weight--
Senão
    PrevEstado = CurrEstado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_user_preferences(uid)
Assertivas de Entrada: 
Ver assertivas de entrada de get_user_preferences(uid)
Assertivas de Saída:
    get_user_preferences(uid) = []
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def delete_user_preferences(uid):
    """
    Deleta a preferência do usuário pelo filme.

    Parâmetros:
        uid: ID do usuário.

        mid: ID do filme.
    """

    preferences = get_user_preferences(uid)

    if preferences:
        for mid in preferences:
            delete_preference(uid, mid)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_movie_preferences(mid)
Assertivas de Entrada: 
Ver assertivas de get_movie_preferences.
Assertivas de Saída:
    get_movie_preferences(mid) = []
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def delete_movie_preferences(mid):
    """
    Deleta todas as preferências do usuário.

    Parâmetros:
        uid: ID do usuário.
    """

    preferences = get_movie_preferences(mid)

    if preferences:
        for uid in preferences:
            delete_preference(uid, mid)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: calc_movie_weighy(mid)
Assertivas de Entrada: Ver assertivas de get_all_preferences e
get_movie_preferences
Assertivas de Saída
Se preferences e movie_presences > 0
    Retorna um float resultante do quociente 'preferences/movie_preferences'
Senão
    Retorna 0
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: update_movie(mid,score)
Assertivas de Entrada:
Ver assertivas de update_movie_weight, update_movie_score,calc_movie_weight
Assertivas de Saída:
Os atributos movie.weight e movie.score serão atualizados no banco de dados. 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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
