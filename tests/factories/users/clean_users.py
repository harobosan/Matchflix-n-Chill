from project.db import Admin, db_commit, User

def clean_users():
    User.query.delete()
    db_commit()

def clean_admins():
    Admin.query.delete()
    db_commit()