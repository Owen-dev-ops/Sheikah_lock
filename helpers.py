# Helper functions for app.py

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import redirect, session, g
from functools import wraps
import os
import sqlite3


# Create connection to database.
def connect_to_db():
    if "db" not in g:
        g.db = sqlite3.connect("sheikah_lock.db", isolation_level=None)
        g.db.row_factory = sqlite3.Row
    return


# Create Fernet instance.
def create_fernet_instance():
    # Get Fernet instance so we can use its encrypt method.
    token = g.db.execute("SELECT token FROM users WHERE id = ?", (session["user_id"], )).fetchone()
    token = token[0]

    # Load .env file.
    load_dotenv()

    # Create Fernet instance using the Master Key.
    master_key = Fernet(os.getenv('MASTER_KEY'))

    # Return instance.
    return Fernet(master_key.decrypt(token))


# Decorator to ensure the user is logged in.
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper



