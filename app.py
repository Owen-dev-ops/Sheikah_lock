# Username and Password Manager Web Application

# Import required libraries
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import flask_login
import sqlite3

from helpers import login_required

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




@app.route("/")
@login_required
def index():
    """Users Login Manager"""

    # Table with services, usernames/emails, and passwords. Username and passwords are XXXXX. 
    # When user clicks view button XXXX reveal login info



    """EDIT LOGIN LOGIC"""
     


@app.route("/login")
def login():
    """Login Page"""

    if request.method == "GET":
        return render_template("login.html")
    
    # clear session["user_id"]
    
    # get username and password from the form

    # make sure username isnt none
        # else return error page
    # make sure password isnt none
        #else return error page

    # aquire username and password from db where the username matches
    # if theres no matching username 
        # return login.html with a message asking the user to try again or register
    # elif the username matches but the password connected to that username dosent 
        # return login.html and inform the username the incorrect passwrod was entered
    # else 
        # session["user_id"] = this users id
        # return index.html
        

@app.route("/logout")
@login_required
def logout():
    "Logout Page"

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