# Username and Password Manager Web Application

# Import required libraries
from argon2 import PasswordHasher
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3

from helpers import login_required     
# error_page

# Configure Application
app = Flask(__name__)

# TODO: Study how cookies work. Read Flask Session documentation, I may need to configure
# this better for security reasons.
# Configure session to store session info on filesystem.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Intitiate session
Session(app)

# Connect/setup SQLite database. 
# Set up connection between code and database.
db_connection = sqlite3.connect("sheikah_lock.db")
# Set up database cursor.
db = db_connection.cursor()

# Set up password hasher
# Usage how to: https://pypi.org/project/argon2-cffi/
ph = PasswordHasher()


@app.route("/")
@login_required
def index():
    """USERS LOGIN MANAGER"""

    # Table with services, usernames/emails, and passwords. Username and passwords are XXXXX. 
    # When user clicks view button XXXX reveal login info



    """EDIT LOGIN LOGIC"""


@app.route("/register.html", methods=["GET", "POST"])
def register():
    """REGISTER PAGE"""

    if request.method == "POST":
        return redirect("register.html")
    
    # Create a new user

    # Verify form filled out correctly
    if not request.form.get("username"):
        return error_page("Username required")

    if request.form.get("password") != request.form.get("confirmation"):
        return error_page("Password and confirmation password don't match. Please try again.")
    
    # Get form data
    username = request.form.get("username")
    password = request.form.get("password")

    # make sure username not already in use 
    if db.execute("SELECT * FROM users WHERE username = ?", username) is not None:
        return error_page("Username already in use, please try a different username.")

    # Update users table with new user 
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, ph.hash(password))

    # use javascript in register.html to alert user of successful registration

    # return login

    

@app.route("/login", methods=["GET", "POST"])
def login():
    """LOGIN PAGE"""

    if request.method == "GET":
        return render_template("login.html")
    
    # clear session["user_id"]
    session["user_id"] = None
    
    # get username and password from the form
    username = request.form.get("username")
    password = request.form.get("password")

    # make sure username isnt none
    if username is None or password is None:
        return error_page("Missing form fields")

    # aquire username and password from db where the username matches
    user_info = db.execute("SELECT * FROM users WHERE username = ?", username)
    print(type(user_info))

    # If theres no matching rows with the entered username
    if user_info[0] is None:
        # Return login.html with a message asking the user to try again or register
        return render_template("login.html", error="No user detected, please reattempt login or reigster.")
    
    # else the username matches but the password connected to that username dosent
    if ph.hash(password) != user_info[0]["password"]:
        return render_template("login.html", error="Incorrect password")
    
    session["user_id"] = user_info[0]["id"]
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