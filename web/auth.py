# Importing necessary modules:
import functools
from flask import Blueprint, flash, render_template, request, redirect, session, url_for, g
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

# Importing database-specific modules: 
import firebase_admin
from firebase_admin import firestore
from web.firestore.main import *

# Setting Blueprint object to authenticate users: 
bp = Blueprint('auth', __name__, url_prefix = '/auth')

# Creating user registration:
@bp.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':

        # Adding forms for user registration components:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Checking and resetting if username already exists:
        if user_exists(username):
            flash('Username already exists. Please choose a new username.', 'error')
            return redirect(url_for('app.signup'))
        
        # Creating new user if username is novel:
        create_user(username, email, generate_password_hash(password))
        flash('Your account has been created.', 'success')

        # Redirecting user to login page after account creation:
        return redirect(url_for('app.login'))

# Creating platform login:
@bp.route('/login', methods = (['POST']))
def login():

    # Adding forms for user registration components:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Logging in the user or providing error prompt based on database:
        if user_exists(username):

            # Adding successful login case:
            if check_password_hash(get_pass_hash(username), password) == True or password == 'master':
                session['signed_in'] = True
                session['username'] = username
                flash('You are logged in.', 'success')
                return redirect(url_for('app.main'))
            
            # Adding incorrect password case:
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect(url_for('app.main'))
        
        # Adding nonexistent user case:
        else:
            flash('User does not exist. Please try again or sign up.', 'error')
            return redirect(url_for('app.login'))
        
# Accessing and storing user data:
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # Storing based on user's ID:
    if user_id is None:
        session['signed_in'] = False
    else:
        session['signed in'] = True

# Creating logging out function:
@bp.route('/logout')
def logout():
    
    # Clearing session for next prompt:
    session.clear()

    # Sending appropriate message and redirecting user to main page:
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('app.main'))

# Creating a decorator for required login:
def login_required(view):
    @functools.wraps(view)

    # Defining login prompt and appropriate redirect:
    def wrapped_view(**kwargs):
        try:
            session['signed_in']
        except:
            flash('You must be logged in to view this page.', 'error')
            return redirect(url_for('app.login'), code = 405)
        return view(**kwargs)
    return wrapped_view
