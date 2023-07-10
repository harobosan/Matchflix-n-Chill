"""Módulo responsável pelo gerenciamento das relações entre usuários"""

from .db import Relationship, db_commit, db_add, db_del


def get_all_relationships():
    """
    Retorna uma lista com todos os relacionamentos.

    Return:
        relationships: Lista de relacionamentos.
    """

    relationships = Relationship.query.all()
    return relationships

def get_relationship(uid_1, uid_2):
    """
    Retorna o relacionamento entre os dois usuários fornecidos.

    Parâmetros:
        uid_1: ID do primeiro usuário.

        uid_2: ID do segundo usuário.

    Return:
        relationship: Objeto do relacionamento encontrado ou None.
    """

    relationship = Relationship.query.filter_by(uid_1=uid_1, uid_2=uid_2).first()

    if not relationship:
        relationship = Relationship.query.filter_by(uid_1=uid_2, uid_2=uid_1).first()

    return relationship

def get_user_relationships(uid):
    """
    Retorna uma lista de IDs dos usuários relacionados ao usuário fornecido.

    Parâmetros:
        uid: ID do usuário.

    Return:
        relationships: Lista de IDs dos usuários relacionados.
    """

    rel_1 = Relationship.query.filter_by(uid_1=uid)
    rel_2 = Relationship.query.filter_by(uid_2=uid)

    relationships = []
    for rel in rel_1:
        relationships.append(rel.uid_2)
    for rel in rel_2:
        relationships.append(rel.uid_1)

    return relationships

def relationship_exists(uid_1, uid_2):
    """
    Verifica se existe um relacionamento entre os dois usuários fornecidos.

    Parâmetros:
        uid_1: ID do primeiro usuário.

        uid_2: ID do segundo usuário.

    Return:
        bool: True se o relacionamento existe, False caso contrário.
    """

    return bool(get_relationship(uid_1, uid_2))

def create_relationship(uid_1, uid_2):
    """
    Cria um novo relacionamento entre os dois usuários fornecidos.

    Parâmetros:
        uid_1: ID do primeiro usuário.

        uid_2: ID do segundo usuário.

    Return:
        relationship: Objeto do relacionamento criado ou None.
    """

    if relationship_exists(uid_1, uid_2):
        return None

    relationship = Relationship(uid_1=uid_1, uid_2=uid_2)
    db_add(relationship)
    db_commit()
    return relationship

def delete_relationship(uid_1, uid_2):
    """
    Deleta o relacionamento entre os dois usuários fornecidos.

    Parâmetros:
        uid_1: ID do primeiro usuário.

        uid_2: ID do segundo usuário.
    """

    relationship = get_relationship(uid_1, uid_2)

    if relationship:
        db_del(relationship)
        db_commit()

def delete_user_relationships(uid):
    """
    Deleta todos os relacionamentos do usuário fornecido.

    Parâmetros:
        uid: ID do usuário.
    """

    relationships = get_user_relationships(uid)

    if relationships:
        for uid_2 in relationships:
            db_del(get_relationship(uid, uid_2))
        db_commit()
