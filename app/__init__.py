from flask import Flask
# from flask_login import LoginManager
import os

from . import auth

def create_app(test_config = None):
    template_dir = os.path.abspath('frontend')
    app = Flask(__name__, instance_relative_config = True, template_folder = template_dir, static_folder = template_dir, static_url_path = '')
    app.config.from_mapping(SECRET_KEY = 'admin', DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'))

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user():
        pass

    return app
