from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

from app.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "SECRET KEY")

    login_manager.init_app(app)
    bcrypt.init_app(app)

    add_admin(os.getenv("ADMIN_USERNAME", "admin"), os.getenv("ADMIN_PASSWORD", "admin"))

    # Register blueprints
    from .auth import auth_bp
    from .main import main_bp
    from .add import add_bp
    from .edit import edit_bp
    from .delete import delete_bp
    from .timetable import timetable_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(add_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(timetable_bp)

    return app

def add_admin(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    User.add_user(username, hashed_password)