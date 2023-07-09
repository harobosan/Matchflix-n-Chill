from project.db import db_commit, User

def clean_users():
    User.query.delete()
    db_commit()