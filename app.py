# Username and Password Manager Web Application

# Import required libraries
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3

# Configure Application
app = Flask(__name__)

# Configure session to store session info on filesystem.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# TODO: Connect/setup SQLite database here. 

@app.route("/")
# TODO: Make @login_required in helpers.py and add here. Study python decorator functions first.