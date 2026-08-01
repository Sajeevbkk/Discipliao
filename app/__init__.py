from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-prod'

    login_manager.init_app(app)
    bcrypt.init_app(app)

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
