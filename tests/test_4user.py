from project.user import (authenticate_user, calc_matches, create_user, disconnect_user, get_admin,
    get_all_users, get_user, get_user_list, remove_admin, set_admin)
from project.db import Admin, User
from tests.factories.users.clean_users import clean_admins, clean_users
from project.movie import create_movie
from project.preference import create_preference
from tests.factories.preferences.clean_preferences import clean_users_movies_preferences

def generate_matches():
    user = create_user('teste6@gmail.com', 'teste6', 'senha6')
    user2 = create_user('teste7@gmail.com', 'teste7', 'senha7')
    user3 = create_user('teste8@gmail.com', 'teste8', 'senha8')
    user4 = create_user('teste9@gmail.com', 'teste9', 'senha9')
    movie = create_movie('nametest1', 'url')
    movie2 = create_movie('nametest2', 'url')
    movie3 = create_movie('nametest3', 'url')
    create_preference(user.id, movie.id)
    create_preference(user.id, movie2.id)
    create_preference(user.id, movie3.id)
    create_preference(user2.id, movie2.id)
    create_preference(user2.id, movie3.id)
    create_preference(user3.id, movie3.id)
    create_preference(user4.id, movie.id)
    create_preference(user4.id, movie2.id)
    create_preference(user4.id, movie3.id)
    return [user.id, user2.id, user3.id]

def test_create_user(app):
    clean_users()
    create_user('teste@gmail.com', 'teste','senha')
    user = User.query.filter_by(email='teste@gmail.com').first()
    assert user.id == 1

def test_create_repeated_user(app):
    user = create_user('teste@gmail.com', 'teste','senha')
    assert user == None

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

def test_set_admin(app):
    clean_users()
    clean_admins()
    user = create_user('adminteste@gmail.com', 'adminteste','adminteste')
    adminAttempt1 = Admin.query.filter_by(uid=user.id).first()
    set_admin(user.id)
    adminAttempt2 = Admin.query.filter_by(uid=user.id).first()
    assert adminAttempt1 == None and adminAttempt2.uid == user.id

def test_remove_admin(app):
    clean_users()
    clean_admins()
    user = create_user('adminteste2@gmail.com', 'adminteste2','adminteste2')
    set_admin(user.id)
    adminAttempt1 = Admin.query.filter_by(uid=user.id).first()
    remove_admin(1)
    adminAttempt2 = Admin.query.filter_by(uid=user.id).first()
    assert adminAttempt1.uid == user.id and adminAttempt2 == None

def test_calc_matches(app):
    clean_users_movies_preferences()
    returnal = generate_matches()
    recommendations = calc_matches(returnal[0])
    print(recommendations)
    assert recommendations[0][0] == 4 and recommendations[2][0] == 3
    