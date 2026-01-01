# Username and Password Manager Web Application

# Import required libraries
from argon2 import PasswordHasher
from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
import sqlite3
# TODO: Add crytopgrahy here. https://pypi.org/project/cryptography/

from helpers import connect_to_db, login_required     
# error_page

# Configure Application
app = Flask(__name__)

# TODO: Study how cookies work. Read Flask Session documentation, I may need to configure
# this better for security reasons.
# Configure session to store session info on filesystem. Don't store session info after user leaves site.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Intitiate session
Session(app)

# Set up password hasher as needed in routes
# Usage how to: https://pypi.org/project/argon2-cffi/
# ph = PasswordHasher()


@app.route("/")
@login_required
def index():
    """USERS LOGIN MANAGER"""
    print(session["user_id"])
    return render_template("error_page.html", error="TODO")
    
    # Table with services, usernames/emails, and passwords. Username and passwords are XXXXX. 
    # When user clicks view button XXXX reveal login info



    """EDIT LOGIN LOGIC"""


@app.route("/register", methods=["GET", "POST"])
def register():
    """REGISTER PAGE"""

    if request.method == "GET":
        return render_template("register.html")
    
    # Get form data
    username = request.form.get("username")
    password = request.form.get("password")

    # Verify form filled out correctly
    if not username or not password:
        return render_template("register.html", error_message="Username or password is missing. Please try again.")

    if password != request.form.get("confirmation"):
        return render_template("register.html", error_message="Password and confirm password do not match. Please try again.")

    # Create a connection to the database for this users request
    connect_to_db()

    # Make sure username is not already in use 
    if g.db.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone():
        return render_template("register.html", error_message="Username already in use, please try a different username.")

    # Update users table with new user 
    ph = PasswordHasher()
    g.db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, ph.hash(password)))

    # Send user to login page
    return render_template("login.html", message=f"Sucess! {username} has been registered.", username=username)

    

@app.route("/login", methods=["GET", "POST"])
def login():
    """LOGIN PAGE"""

    if request.method == "GET":
        return render_template("login.html")
    
    # Clear session["user_id"]
    session["user_id"] = None
    
    # get username and password from the form
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Make sure username and password were entered
    if username is None or password is None:
        return render_template("login.html", error_message="Missing username or password.")

    # Create a connection to the database for this users request
    connect_to_db()

    # Aquire the id, username, and login info of this user
    user_info = g.db.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchone()

    # If theres no matching rows with the entered username alert user
    if user_info is None:
        # Return login.html with a message asking the user to try again or register
        return render_template("login.html", error_message="No user detected, please reattempt login or reigster.")
    
    # Confirm the correct password was entered
    ph = PasswordHasher()
    if not ph.verify(user_info["password"], password):
        # Alert user that the password they entered is incorrect
        return render_template("login.html", error_message="Incorrect password")
    
    session["user_id"] = user_info["id"]
    return redirect("/")
        

@app.route("/logout")
@login_required
def logout():
    "LOGOUT PAGE"

    # To get to this route have a logout button somewhere
    # Use javascript on page to confirm the user wants to logout before doing so
    # clear session["user_id"]
    # return login.html

@app.route("/new_login")
@login_required
def new_login():
      """NEW LOGIN LOGIC"""
    # Top right or somewhere there will be a button to add logins
    # When clicked a modal will appear which includes a form which post here.
    # Form will include, service name, user name, email (optional, either username or email must be filled out), and password
    # allow multiple logins to be added at once within form
    # When form is received put form fields into variables
    # for each login entered within the form
        # make sure either email or username is not none
            # else return error page
        # make sure password is not none
            # else return error page
        # else 
            # update a dictionary with the login info
    # Update db with the dictionary of new logins
    # return index.html with there new updated login list.

@app.route("/remove_login")
@login_required
def remove_login():
        """ REMOVE LOGIN LOGIC """


@app.teardown_appcontext
def close_db(exception): 
    db = g.pop('db', None)
    if db is not None:
        db.close()