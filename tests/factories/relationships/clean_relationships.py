from project.db import db_commit, Relationship

def clean_relationships():
    Relationship.query.delete()
    db_commit()