"""relationship"""

from .db import Relationship, db_commit, db_add, db_del


def get_all_relationships():
    """get_all_relationships"""

    relationships = Relationship.query.all()
    return relationships

def get_relationship(uid_1, uid_2):
    """get_relationship"""

    relationship = Relationship.query.filter_by(uid_1=uid_1, uid_2=uid_2).first()

    if not relationship:
        relationship = Relationship.query.filter_by(uid_1=uid_2, uid_2=uid_1).first()

    return relationship

def get_user_relationships(uid):
    """get_user_relationships"""

    rel_1 = Relationship.query.filter_by(uid_1=uid)
    rel_2 = Relationship.query.filter_by(uid_2=uid)
    relationships = []
    for rel in rel_1:
        relationships.append(rel.uid_2)
    for rel in rel_2:
        relationships.append(rel.uid_1)
    return relationships

def relationship_exists(uid_1, uid_2):
    """relationship_exists"""

    return bool(get_relationship(uid_1, uid_2))

def create_relationship(uid_1, uid_2):
    """create_relationship"""

    if relationship_exists(uid_1, uid_2):
        return None

    relationship = Relationship(uid_1=uid_1, uid_2=uid_2)
    db_add(relationship)
    db_commit()
    return relationship

def delete_relationship(uid_1, uid_2):
    """delete_relationship"""

    relationship = get_relationship(uid_1, uid_2)

    if relationship:
        db_del(relationship)
        db_commit()

def delete_user_relationships(uid):
    """delete_user_relationships"""

    relationships = get_user_relationships(uid)

    if relationships:
        for relationship in relationships:
            db_del(relationship)
        db_commit()
