"""Módulo responsável pelo gerenciamento das informações de usuário"""

from werkzeug.security import generate_password_hash, check_password_hash
from .db import User, Admin, db_commit, db_add, db_del
from .movie import get_movie_weight
from .preference import get_user_preferences, get_movie_preferences
from .relationship import get_relationship, get_user_relationships

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_all_users()
Assertivas de Entrada:
Nenhuma Pré-condição especifíca
Assertivas de Saída:
Retorna uma lista de objetos 'User' presentes no banco de dados.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_all_users():
    """Retorna uma lista com todos os usuários."""

    users = User.query.all()
    return users

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_user(email)
Assertivas de Entrada:
O parâmetro 'email' é uma string
Assertivas de Saída:
Se há um objeto 'User' com atributo 'email' == email
    Retorna User
Senão
    Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_user_list(user_list)
Assertivas de Entrada:
user_list != []
Assertivas de Saída:
Retorna uma lista 'users' contendo os usuários encontrados.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_user_list(user_list):
    """
    Retorna uma lista de usuários com base em uma lista de IDs.

    Parâmetros:
        user_list: Lista de IDs dos usuários.

    Return:
        users: Lista de usuários encontrados.
    """

    users = []
    for uid in user_list:
        user = User.query.filter_by(id=uid).first()

        if user:
            users.append(user)

    return users

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: user_exists(email)
Assertivas de Entrada:
O parâmetro 'email' é uma string
Assertivas de Saída
Se há User.email == email no banco de Dados
    Retorna True
Senão
    Retorna False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def user_exists(email):
    """
    Verifica se um usuário com o e-mail fornecido existe.

    Parâmetros:
        email: E-mail do usuário a ser verificado.

    Return:
        bool: True se o usuário existe, False caso contrário.
    """

    return bool(get_user(email))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: create_user
Assertivas de Entrada:
email, username, password são strings tais que len(string)>0
Assertivas de Saída:
Se há User.email == email no banco de dados
    Retorna None
Senão
    Gera uma senha string
    Gera um objeto 'User' com os respectivos atributos deslogado
    Este objeto constará no banco de dados após a execução.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_user(email)
Assertivas de Entrada:
Ver assertivas de get_user(email)
Assertivas de Saída:
Se há user.email == email no banco de dados
    Deleta-se usuário do banco de dados
    Banco é atualizado
Senão
    O estado permanece inalterado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: authenticate_user
Assertivas de Entrada:
Parâmetros 'email' e 'password' são strings.
Assertivas de Sáida:
Se user.password != password ou get_user(email) == None
    Retorna None
Senão
    Estado de user.authentciated é alterado
    Banco de dados é atualizado
    Retorna uma string user.email
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: disconnect_user(user)
Assertivas de entrada:
'user' é um objeto 'User'
Assertivas de Saída:
Se o usuário existe
    O estado user.authenticated é alterado
    O banco de dados é atualizado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def disconnect_user(user):
    """
    Desconecta um usuário do sistema.

    Parâmetros:
        user: Objeto do usuário a ser desconectado.
    """

    if user and user_exists(user.email):
        user.authenticated = False
        db_commit()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: update_email(user,email)
Assertivas de Entrada:
'user' é um objeto 'User' e email é uma string 
tal que len(email) > 0
Assertivas de Saída:
Se há user.email == email no banco de dados
    Retorna None
Senão
    user.email == email
    O banco de dados é atualizado
    É retornado um objeto 'User' atualizado.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_email(user, email):
    """update_email"""

    if get_user(email):
        return None

    user.email = email
    db_commit()
    return user

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: update_username(user,username)
Assertivas de Entrada:
'user' é um objeto 'User' e username é uma string
tal que len(username) > 0
Assertivas de Saída:
O atributo 'username' é atualizado no banco de dados.
O objeto 'user' atualizado é retornado.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_username(user, username):
    """update_username"""

    user.username = username
    db_commit()
    return user

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: update_password(user,password)
Assertivas de Entrada:
'user' é um objeto 'User' e password é uma string
Assertivas de Saída:
O atributo user.password é atualizado no banco de dados
É retornado o objeto 'user' atualizado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_password(user, password):
    """update_password"""

    hashed = generate_password_hash(password, method='sha256')
    user.password = hashed
    db_commit()
    return user

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_admin(uid)
Assertivas de Entrada:
uid é um inteiro > 0
Assertivas de Saída:
Se há admin.id == uid
    Retorna objeto 'Admin'
Senão
    Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: is_admin(uid)
Assertivas de Entrada:
uid é um inteiro > 0
Assertivas de Saída:
Se get_admin(uid)
    Retorna True
Senão
    Retorna False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def is_admin(uid):
    """
    Verifica se o usuário com o ID fornecido é um administrador.

    Parâmetros:
        uid: ID do usuário a ser verificado.

    Return:
        bool: True se o usuário é um administrador, False caso contrário.
    """

    return bool(get_admin(uid))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: set_admin(uid)
Assertivas de Entrada:
uid é um inteiro > 0
Assertivas de Saída:
Se !is_admin
    Cria um objeto admin
    Adiciona-se ao banco de dados
    Retorna o objeto
Senão
    Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: remove_admin(uid)
Assertivas de Entrada:
Ver assertivas de get_admin
Assertivas de Saída
Se get_admin
    Tal instância será deletada do banco de dados
Senão
    O estado permanece inalterado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: sort_matches(user)
Assertivas de Entrada:
user é um objeto 'User'
Assertivas de Saída:
    Retorna um valor inteiro
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def sort_matches(user):
    """
    Função chave para ordenar os resultados de acordo com as correspondências do usuário.

    Parâmetros:
        user: Par ID do usuário e Pontuação de correspondência.

    Return:
        user[1]: Valor usado para classificar as correspondências.
    """

    return user[1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: calc_matches
Assertivas de Entrada:
uid é um inteiro > 0
Assertivas de Saída:
Retorna uma lista de recomendações de usuários
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_relationship_lists(uid)
Assertivas de Entrada:
uid é um inteiro > 0
Assertivas de Saída:
Retorna uma matriz contendo listas de amigos,pedidos, pendências
e recomendações.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
