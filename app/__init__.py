from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config

mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth
    from app.routes.mood import mood
    app.register_blueprint(auth)
    app.register_blueprint(mood)

    return app