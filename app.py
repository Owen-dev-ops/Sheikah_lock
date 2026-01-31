# Username and Password Manager Web Application
# Design inspired by the Sheikah from the Legend of Zelda series.

# TODO: Before uploading this to CS50 course remove all todo comments.

# Import required libraries
from argon2 import PasswordHasher
from flask import Flask, flash, g, redirect, render_template, request, session, url_for
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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """USERS LOGIN MANAGER"""
    # Table with services, usernames/emails, and passwords. 
    
    if request.method == "GET":
        # Connect to database
        connect_to_db()
        user_logins = g.db.execute("SELECT service_name, id FROM logins WHERE user_id = ?", (session["user_id"], )).fetchall()
        return render_template("index.html", user_logins=user_logins)
    
    # If method is post complete user request.
    if request.method == "POST":
        return render_template("error_page.html", error="TODO")

        # Get login id of the login the user wants to see. 
    



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
    
    session["user_id"] = None
    return render_template("login.html")


@app.route("/new_login", methods=["GET", "POST"])   
@login_required
def new_login():
    """NEW LOGIN LOGIC"""
    # When form is received put form fields into variables
    service = request.form.get("service")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Make sure either a Username or Email is entered
    if not email and not username:
        flash("Email or username is required. Please try again.", "user_error")
        return redirect(url_for('index'))
    
    # TODO: If email is entered verify it has correct format. 
    # if email:

    # Make sure a password was entered
    if "" in (service, password):
        flash("Service name or password is missing.", "user_error")
        return redirect(url_for('index'))

    # Encrypt service_username, email, and service_password.


    # Update logins with new login
    connect_to_db()
    g.db.execute("""INSERT INTO logins 
                 (user_id, service_name, service_username, email, service_password) 
                 VALUES (?, ?, ?, ?, ?)
                 """, (session["user_id"], service, username, email, password))
    
    # Return index.html with the new updated login list.
    flash("Login added successfully.", "user_success")
    return redirect(url_for('index'))

@app.route("/remove_login")
@login_required
def remove_login():
    """ REMOVE LOGIN LOGIC """

@app.route("/reveal_login", methods=["GET", "POST"])
@login_required
def reveal_login():
    """ REVEAL LOGIN IN LOGIN MANAGER """

    login_id = request.form.get("user_input")

    # login_id is returning as undefined
    print(login_id)
    return render_template("error_page.html", error="TODO")


@app.teardown_appcontext
def close_db(exception): 
    db = g.pop('db', None)
    if db is not None:
        db.close()