"""Módulo responsável pelo gerenciamento das informações de usuário"""

from werkzeug.security import generate_password_hash, check_password_hash
from .db import User, Admin, db_commit, db_add, db_del
from .movie import get_movie_weight
from .preference import get_user_preferences, get_movie_preferences
from .relationship import get_relationship, get_user_relationships


def get_all_users():
    """Retorna uma lista com todos os usuários."""

    users = User.query.all()
    return users

def get_user(email):
    """
    Retorna o usuário correspondente ao email fornecido.

    Parâmetros:
        email: E-mail do usuário a ser buscado.

    Returns:
        user: Objeto do usuário encontrado ou None.
    """

    user = User.query.filter_by(email=email).first()
    return user

def get_user_list(user_list):
    """
    Retorna uma lista de usuários com base em uma lista de IDs.
    """

    users = []
    """

    Parâmetros:
        user_list: Lista de IDs dos usuários.

    Return:
        users: Lista de usuários encontrados.
    """
    for uid in user_list:
        user = User.query.filter_by(id=uid).first()

        if user:
            users.append(user)

    return users

def user_exists(email):
    """
    Verifica se um usuário com o e-mail fornecido existe.

    Parâmetros:
        email: E-mail do usuário a ser verificado.

    Return:
        bool: True se o usuário existe, False caso contrário.
    """

    return bool(get_user(email))

def create_user(email, username, password):
    """
    Cria um novo usuário no banco de dados.

    Parameters:
        email: E-mail do novo usuário.
        username: Nome de usuário do novo usuário.
        password: Senha do novo usuário.

    Returns:
        user: Objeto do usuário criado ou None.
    """

    if user_exists(email):
        return None

    hashed = generate_password_hash(password, method='sha256')
    user = User(email=email, username=username, password=hashed, authenticated=False)
    db_add(user)
    db_commit()
    return user

def delete_user(email):
    """
    Deleta um usuário do banco de dados.

    Parâmetros:
        email: E-mail do usuário a ser deletado.
    """

    user = get_user(email)

    if user:
        db_del(user)
        db_commit()

def authenticate_user(email, password):
    """
    Realiza a autenticação um usuário com base no e-mail e senha fornecidos.

    Parâmetros:
        email: E-mail do usuário a ser autenticado.
        password: Senha do usuário a ser autenticado.

    Return:
        user: Objeto do usuário autenticado ou None.
    """

    user = get_user(email)

    if user and check_password_hash(user.password, password):
        user.authenticated = True
        db_commit()
        return user

    return None

def disconnect_user(user):
    """
    Desconecta um usuário do sistema.

    Parâmetros:
        user: Objeto do usuário a ser desconectado.
    """

    if user and user_exists(user.email):
        user.authenticated = False
        db_commit()

def update_email(user, email):
    """update_email"""

    if get_user(email):
        return None

    user.email = email
    db_commit()
    return user

def update_username(user, username):
    """update_username"""

    user.username = username
    db_commit()
    return user

def update_password(user, password):
    """update_password"""

    hashed = generate_password_hash(password, method='sha256')
    user.password = hashed
    db_commit()
    return user

def get_admin(uid):
    """
    Retorna o objeto de administração associado ao ID do usuário fornecido.

    Parâmetros:
        uid: ID do usuário.

    Return:
        admin: Objeto de administração ou None.
    """

    admin = Admin.query.filter_by(uid=uid).first()
    return admin

def is_admin(uid):
    """
    Verifica se o usuário com o ID fornecido é um administrador.

    Parâmetros:
        uid: ID do usuário a ser verificado.

    Return:
        bool: True se o usuário é um administrador, False caso contrário.
    """

    return bool(get_admin(uid))

def set_admin(uid):
    """
    Define o usuário com o ID fornecido como administrador.

    Parâmetros:
        uid: ID do usuário a ser definido como administrador.

    Return:
        admin: Objeto de administração criado ou None.
    """

    if is_admin(uid):
        return None

    admin = Admin(uid=uid)
    db_add(admin)
    db_commit()
    return admin

def remove_admin(uid):
    """
    Remove a atribuição de administrador do usuário com o ID fornecido.

    Parâmetros:
        uid: ID do usuário a ter a atribuição de administrador removida.
    """

    admin = get_admin(uid)

    if admin:
        db_del(admin)
        db_commit()

def sort_matches(user):
    """
    Função auxiliar para classificar os resultados de acordo com as correspondências do usuário.

    Parâmetros:
        user: Objeto de usuário.

    Return:
        user[1]: Valor usado para classificar as correspondências.
    """

    return user[1]

def calc_matches(uid):
    """
    Calcula as correspondências entre um usuário e outros usuários com base em suas preferências.

    Parâmetros:
        uid: ID do usuário.

    Return:
        recommendations: Lista de correspondências ordenadas por pontuação.
    """

    user_preferences = get_user_preferences(uid)
    user_relationships = get_user_relationships(uid)

    movies_list = []
    for mid in user_preferences:
        movies_list.append([get_movie_weight(mid), get_movie_preferences(mid)])

    user_matches = []
    user_scores = []
    for movie_pair in movies_list:
        for user in movie_pair[1]:
            if user != uid and not user_relationships.count(user):
                if user_matches.count(user):
                    user_scores[user_matches.index(user)] += movie_pair[0]
                else:
                    user_matches.append(user)
                    user_scores.append(movie_pair[0])

    recommendations = []
    for count, user in enumerate(user_matches):
        recommendations.append([user, user_scores[count]])

    recommendations.sort(reverse=True, key=sort_matches)
    return recommendations

def get_relationship_lists(uid):
    """get_relationship_lists"""

    relationships = get_user_relationships(uid)

    friends = []
    pending = []
    requests = []
    for user in relationships:
        relationship = get_relationship(uid, user)

        if relationship.status:
            friends.append(User.query.filter_by(id=user).first())
        else:
            if relationship.uid_1 == uid:
                pending.append(User.query.filter_by(id=user).first())
            else:
                requests.append(User.query.filter_by(id=user).first())

    matches = calc_matches(uid)
    recommendations = []
    for match in matches:
        recommendations.append([User.query.filter_by(id=match[0]).first(), match[1]])

    return [friends, pending, requests, recommendations]
