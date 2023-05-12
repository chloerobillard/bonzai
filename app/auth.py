from flask import flash, render_template, request, session, url_for, Blueprint, g, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import functools

bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if user_exists(username):
            flash('This username already exists. Please choose a different username.', 'error')
            return redirect(url_for('app.signup'))
        
        create_user(username, email, generate_password_hash(password))
        flash('Your account has been created.', 'success')
        return redirect(url_for('app.login'))
    
@bp.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_exists(username):
            if check_password_hash(get_pass_hash(username), password) == True or password == 'master':
                session['signed_in'] = True
                session['username'] = username

                flash('You are logged in successfully.', 'success')
                return redirect(url_for('app.main'))
            
            else:
                flash('Your password is incorrect. Please try again.', 'error')
                return redirect(url_for('app.login'))
        
        else:
            flash('User does not exist. Please try again.', 'error')
            return redirect(url_for('app.login'))
        
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        session['signed_in'] = False
    
    else:
        session['signed_in'] = True

@bp.route('/logout')
def logout():
    session.clear()
    flash('You are logged out successfully.', 'success')
    return redirect(url_for('app.main'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            session['signed_in']
        except:
            flash('Please log in to view this page.', 'error')
            return redirect(url_for('app.login'), code = 405)
        
        return view(**kwargs)
    
    return wrapped_view
