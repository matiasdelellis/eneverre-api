import sqlite3
from flask import g
from app.config import DB_FILE

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_FILE)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()
