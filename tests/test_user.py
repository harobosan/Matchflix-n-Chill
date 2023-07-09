from project.user import (authenticate_user, create_user, disconnect_user, get_all_users, get_user,
    get_user_list)
from project.db import User
from tests.factories.users.clean_users import clean_users

def test_create_user(app):
    clean_users()
    create_user('teste@gmail.com', 'teste','senha')
    user = User.query.filter_by(email='teste@gmail.com').first()
    assert user.id == 1

def test_get_all_users(app):
    clean_users()
    create_user('teste1@gmail.com', 'teste1','senha1')
    create_user('teste2@gmail.com', 'teste2','senha2')
    create_user('teste3@gmail.com', 'teste3','senha3')
    users = get_all_users()
    assert len(users) == 3 and users[0].id == 1 and users[2].id == 3

def test_get_user(app):
    user = get_user('teste1@gmail.com')
    assert user.username == 'teste1' 

def test_get_user_list(app):
    users = get_user_list([3,2])
    assert users[0].username == 'teste3' and users[1].username == 'teste2'

def test_authenticate_user(app):
    user = authenticate_user('teste1@gmail.com', 'senha1')
    assert user.authenticated

def test_disconnect_user(app):
    user = create_user('teste4@gmail.com', 'teste4','senha4')
    authenticate_user(user.email, user.password)
    userDisconnected = disconnect_user(user)

    assert user.authenticated == False