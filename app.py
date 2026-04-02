# Username and Password Manager Web Application
# Design inspired by the Sheikah from the Legend of Zelda series.

# Import required libraries
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
import os

from helpers import connect_to_db, create_fernet_instance, login_required     

# Configure Application
app = Flask(__name__)

# Configure cookies.
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

    # Connect to database.
    connect_to_db()

    # Get the encrypted service names as well as the login ids for all logins.
    encrypted_user_logins = g.db.execute("SELECT service_name, id FROM logins WHERE user_id = ?", (session["user_id"], )).fetchall()

    # Create Fernet instance so we can acess its decryption method.
    f = create_fernet_instance()
    
    # user_logins will hold the decrypted data of encrypted_user_logins.
    user_logins = []

    # Append Sqlite Row data to user_logins and convert each row to a dictionary before doing so.
    for row in encrypted_user_logins:
        user_logins.append(dict(row))

    # Decrypt all service names.
    for row in user_logins:
        for key in row.keys():
            if key == 'service_name':
                row[key] = f.decrypt(row[key]).decode("utf-8")
            else:
                pass
    
    if request.method == "GET":

        # Get encrypted service_name and login ids from the logins table.
        # encrypted_user_logins = g.db.execute("SELECT service_name, id FROM logins WHERE user_id = ?", (session["user_id"], )).fetchall()    

        # Decrypt service_name.

        # Create Fernet instance so we can access its decrypt method.
        # token = g.db.execute("SELECT token FROM users WHERE id = ?", (session["user_id"], )).fetchone()
        # token = token[0]
        # f = Fernet(token)

        # user_logins = []
        
        # Add encrypted_user_login info to user_info dictionary so we can update it before returning.
        # Sqlite3 fetchone return object doesn't allow the editing of indexes.
        #for row in encrypted_user_logins:
            #user_logins.append(dict(row))

        """ for row in user_logins:
            for key in row.keys():
                if key == 'service_name':
                    row[key] = f.decrypt(row[key]).decode("utf-8")        
                else: 
                    pass """

        return render_template("index.html", user_logins=user_logins)
    
    # If method is post then the user wants to reveal a row in the login table.
    if request.method == "POST":

        # Get login id of the login the user wants to see. 
        login_id = request.form.get("user_input")

        if login_id is None:
            flash("How did you even get here?", "user_error")
            return redirect(url_for('index'))
        
        # connect_to_db()
        # revealed_logins = g.db.execute("SELECT service_name, service_username, email, service_password FROM logins WHERE id = ?", (login_id, )).fetchone()
        # user_logins = g.db.execute("SELECT service_name, id FROM logins WHERE user_id = ?", (session["user_id"], )).fetchall()

        # Decrypt login data

        # Will hold the decrypted revealed logins.
        revealed_logins = []

        # Get encrypted_revealed_logins
        encrypted_revealed_logins = g.db.execute("SELECT service_name, service_username, email, service_password FROM logins WHERE id = ?", (login_id, )).fetchone()
    
        revealed_logins.append(dict(encrypted_revealed_logins))

        # Decrypt login info.
        for row in revealed_logins:
            for key in row.keys():
                row[key] = f.decrypt(row[key]).decode("utf-8")

        # Return index with the revealed login information.
        return render_template("index.html", login_id=login_id, revealed_logins=revealed_logins, user_logins=user_logins)



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
    if g.db.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchall() != []:
        return render_template("register.html", error_message="Username already in use, please try a different username.")

    # Update users table with new user 

    # Create instance of PasswordHasher to utilizie its hash method on password before inserting into users table.
    ph = PasswordHasher()

    # Generate a fernet key. (DEK)
    token = Fernet.generate_key()

    # Load env file.
    load_dotenv()

    # Encrypt token with MASTER_KEY (KEK). 
    master_key = Fernet(os.getenv('MASTER_KEY'))
    token = master_key.encrypt(token)
    
    # Add user to users.
    g.db.execute("INSERT INTO users (username, password, token) VALUES (?, ?, ?)", (username, ph.hash(password), token))

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
    user_info = g.db.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username, )).fetchone()

    # If theres no matching rows with the entered username alert user
    if user_info is None:
        # Return login.html with a message asking the user to try again or register
        return render_template("login.html", error_message="No user detected, please reattempt login or reigster.")
    
    # Confirm the correct password was entered
    ph = PasswordHasher()

    try:
        ph.verify(user_info["Password"], password)
        session["user_id"]= user_info["id"]
        return redirect("/")
    except: 
        # Alert user that the password they entered is incorrect
        return render_template("login.html", error_message="Incorrect password")
        


@app.route("/logout")
@login_required
def logout():
    "LOGOUT PAGE"
    
    # Clear session info and return user to the login page.
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
    
    # Make sure a password was entered
    if "" in (service, password):
        flash("Service name or password is missing.", "user_error")
        return redirect(url_for('index'))

    # Update logins with new login
    connect_to_db()

    f = create_fernet_instance()

    # Encrypt login.
    service = f.encrypt(service.encode())
    username = f.encrypt(username.encode())
    email = f.encrypt(email.encode())
    password = f.encrypt(password.encode())


    g.db.execute("""INSERT INTO logins 
                 (user_id, service_name, service_username, email, service_password) 
                 VALUES (?, ?, ?, ?, ?)
                 """, (session["user_id"], service, username, email, password))
    
    # Return index.html with the new updated login list.
    flash("Login added successfully.", "user_success")
    return redirect(url_for('index'))



@app.route("/edit_login", methods=["GET", "POST"])
@login_required
def edit_login():
    """ EDIT AND REMOVE LOGIN LOGIC """

    # If form user opens the form fill in the placeholder values, else, update the login and return index. 
    form_data = request.form.to_dict()
    if form_data == {}: 
        data = request.get_json()

        # Get login_id, this is the row we are editing.
        login_id = data["login_id"]

        # Connect to sheikah_lock.db.
        connect_to_db()

        # Get login information.
        encrypted_revealed_logins = g.db.execute("SELECT service_username, email, service_password FROM logins WHERE id = ?", (login_id, )).fetchone()

        # Decrypt login information.

        revealed_logins = []

        # Append encrypted_revealed_logins to revealed_logins.
        revealed_logins.append(dict(encrypted_revealed_logins))

        # Create Fernet instance so we can access its decryption method.
        f = create_fernet_instance()
  
        # Decrypt login info.
        for row in revealed_logins:
            for key in row.keys():
                row[key] = f.decrypt(row[key]).decode("utf-8")

        # Return username, email, and password to frontend to fill in the edit form placeholder values.
        return jsonify(user_data = {
            "username": revealed_logins[0]["service_username"],
            "email": revealed_logins[0]["email"],
            "password": revealed_logins[0]["service_password"]
        })
    
    # Verify that a service name was entered and password was entered
    if "" in (form_data["service_name_edit"], form_data["password_edit"]):
        flash("Service name or password is missing", "user_error")
        return redirect(url_for('index'))

    # Verify that either a username or email was entered 
    if form_data["service_name_edit"] == "" and form_data["email"] == "":
        flash("Either a username or email is required", 'user_error')
        return redirect(url_for('index'))

    # Connect to db.
    connect_to_db()

    # Encrypt login information before updating.

    # Get Fernet instance so we can access its encrypt method.
    f = create_fernet_instance()

    # Encrypt info.
    form_data["service_name_edit"] = f.encrypt(form_data["service_name_edit"].encode())
    form_data["username_edit"] = f.encrypt(form_data["username_edit"].encode())
    form_data["email_edit"] = f.encrypt(form_data["email_edit"].encode())
    form_data["password_edit"] = f.encrypt(form_data["password_edit"].encode())

    # Update logins with sql statement.
    g.db.execute("""UPDATE logins
                 SET service_name = ?,
                     service_username = ?,
                     email = ?,
                     service_password = ?
                 WHERE id = ?
                 """, (form_data["service_name_edit"], form_data["username_edit"], form_data["email_edit"], form_data["password_edit"], form_data["row_to_edit"]))

    return redirect(url_for('index'))


# Executes after route execution.
@app.teardown_appcontext
def close_db(exception): 
    db = g.pop('db', None)
    if db is not None:
        db.close()