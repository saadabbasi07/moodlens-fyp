from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config

# Initialise extensions
# MySQL Reference: Oracle Corporation (2023) MySQL 8.0 Reference Manual.
# Available at: https://dev.mysql.com/doc/refman/8.0/en/ (Accessed: 16 May 2026)
mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise extensions with app
    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints — MVC Controller layer
    # Views folder contains all Flask route handlers
    # Reference: Pallets Projects (2023) Flask Documentation.
    # Available at: https://flask.palletsprojects.com (Accessed: 16 May 2026)
    from app.views.auth import auth
    from app.views.mood import mood
    app.register_blueprint(auth)
    app.register_blueprint(mood)

    return app