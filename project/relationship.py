"""Módulo responsável pelo gerenciamento das relações entre usuários"""

from .db import Relationship, db_commit, db_add, db_del

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_all_relationships()
Assertivas de Entrada:
Nenhuma pré-condição específica
Assertivas de Saída:
Retorna uma lista contendo os relacionamentos
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_all_relationships():
    """
    Retorna uma lista com todos os relacionamentos.

    Return:
        relationships: Lista de relacionamentos.
    """

    relationships = Relationship.query.all()
    return relationships

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_relationship(uid_1, uid_2)
Assertivas de Entrada:
uid_1,uid_2 são inteiros > 0.
Há no banco de dados usuários com ids iguais aos dos argumentos.
Assertivas de Saída:
Se os usuários possuem relação
    Retorna um objeto 'Relationship'
Senão
    Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: get_user_relationships(uid)
Assertivas de Entrada:
uid é um inteiro > 0.
Assertivas de Saída:
Retorna uma lista de inteiros contendo IDs relacionados ao ID uid.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: relationship_exists(uid_1, uid_2)
Assertivas de Entrada:
Ver as assertivas de entrada de 'get_relationship".
Assertivas de Saída:
Retorna um booleano
Se get_relationship(uid_1,uid_2) != []
    Retorna True
Senão
    Retorna False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: create_relationship(uid_1,uid_2)
Assertivas de Entrada:
uid_1,uid_2 são inteiros > 0.
Há, no banco de dados, usuários com os respectivos ID's.
Assertivas de Saída:
Se a relação não existir previamente
    O banco de dados será atualizado com a relação criada.
    Retorna o objeto 'Relationship'
Senão
    Retorna None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

    relationship = Relationship(uid_1=uid_1, uid_2=uid_2, status=False)
    db_add(relationship)
    db_commit()
    return relationship

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_relationship(uid_1,uid_2)
Assertivas de Entrada:
Ver assertivas de get_relationship(uid_1,uid_2)
Assertivas de Saída:
Se há relação entre os usuários
    A relação é deletada do banco de dados, que é atualizado
Senão
    O estado permanece inalterado.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: delete_user_relationships(uid)
Assertivas de Entrada: 
Ver assertivas de entrada para get_user_relationships
e get_relationship.
Assertiva de Saída:
Se relationships != []
    relationships = []
    O Banco de dados é atualizado
Senão
    O estado permanece inalterado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: update_status(uid_1,uid_2)
Assertivas de Entrada:
Ver assertivas de get_relationship
Assertivas de Saída:
Se relationship != []
    relationship.status = True
    O banco de dados é atulzado
Senão
    O estado permanece inalterado
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_status(uid_1, uid_2):
    """update_status"""

    relationship = get_relationship(uid_1, uid_2)

    if relationship:
        relationship.status = True
        db_commit()
