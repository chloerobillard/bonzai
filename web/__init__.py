# Importing necessary modules:
from flask import Flask
from flask_login import LoginManager
from . import auth
from . import bonzaiapp
import os

# Creating and configuring the app via Flask:
def create_app(test_config = None):
    
    # Directing the app to frontend folder for templating: 
    template_dir = os.path.abspath('frontend')

    # Defining and configuring the app:
    app = Flask(__name__, template_folder = template_dir, static_folder = template_dir, static_url_path = '', instance_relative_config = True)
    app.config.from_mapping(SECRET_KEY = 'admin', DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'))

    # Loading instance config:
    if test_config is None:

        # Loading only when it exists and when not testing:
        app.config.frompyfile('config.py', silent = True)

    # Checking existence of instance folder:
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Registering necessary blueprints for authentication and app:
    app.register_blueprint(auth.bp)
    app.register_blueprint(bonzaiapp.bp)

    # Setting Flask's Login Manager for user sessions:
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Loading users via Login Manager:
    @login_manager.user_loader
    def load_user():
        pass

    # Returning app to run:
    return app
