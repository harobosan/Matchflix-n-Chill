from project.relationship import (create_relationship, delete_relationship,
    delete_user_relationships, get_all_relationships, get_relationship, get_user_relationships)
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

def test_get_relationship(app):
    relationship = get_relationship(1, 2)
    assert relationship.uid_1 == 1 and relationship.uid_2 == 2

def test_get_user_relationships(app):
    user3 = create_user('teste3@gmail.com', 'teste3','senha3')
    relationship1 = create_relationship(1, user3.id)
    relationships = get_user_relationships(1)
    print(relationships)
    assert len(relationships) == 2 and relationships[0] == 2

def test_get_all_relationships(app):
    clean_relationships()
    create_relationship(1, 2)
    create_relationship(1, 3)
    relationships = get_all_relationships()
    assert len(relationships) == 2

def test_delete_relationship(app):
    length1 = len(get_user_relationships(1))
    delete_relationship(1,3)
    length2 = len(get_user_relationships(1))
    assert length1 == 2 and length2 == 1

'''
def test_delete_user_relationships(app):
    create_relationship(1, 3)
    length1 = len(get_user_relationships(1))
    delete_user_relationships(1)
    length2 = len(get_user_relationships(1))
    assert length1 == 2 and length2 == 0
'''