# Helper functions for app.py

from flask import redirect, session
from functools import wraps


# Wraps each route to ensure the user is logged in.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# TODO: Make an error page function