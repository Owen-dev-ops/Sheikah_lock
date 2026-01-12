# Helper functions for app.py

from flask import redirect, session, g
from functools import wraps
import sqlite3

# Decorator to ensure the user is logged in.
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

# Create connection to database.
def connect_to_db():
    if "db" not in g:
        g.db = sqlite3.connect("sheikah_lock.db", isolation_level=None)
        g.db.row_factory = sqlite3.Row
    return


