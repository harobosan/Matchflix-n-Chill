from project.db import db_commit, Preference

def clean_preferences():
    Preference.query.delete()
    db_commit()