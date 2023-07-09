from project.relationship import create_relationship
from project.user import create_user
from tests.factories.relationships.clean_relationships import clean_relationships
from tests.factories.users.clean_users import clean_users

def test_create_relationship(app):
    clean_relationships()
    user1 = create_user('teste1@gmail.com', 'teste1','senha1')
    user2 = create_user('teste2@gmail.com', 'teste2','senha2')
    relationship = create_relationship(user1.id, user2.id)
    assert relationship.uid_1 == user1.id and relationship.uid_2 == user2.id

def test_create_repeated_relationship(app):
    clean_users()
    user1 = create_user('teste1@gmail.com', 'teste1','senha1')
    user2 = create_user('teste2@gmail.com', 'teste2','senha2')
    relationship1 = create_relationship(user1.id, user2.id)
    relationship2 = create_relationship(user1.id, user2.id)
    assert relationship2 == None