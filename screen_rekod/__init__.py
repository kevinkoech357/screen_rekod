from flask import Flask
from screen_rekod.extensions import db, login_manager
from screen_rekod.utils import create_database
from flask_cors import CORS
from screen_rekod.config import App_Config
from screen_rekod.models.user import User
from screen_rekod.models.videos import Video
from screen_rekod.models.subtitles import Subtitle

def create_app():
    # Initialize flask
    app = Flask(__name__)
    app.config.from_object(App_Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print("Using main db")

    # Initialize CORS
    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Import blueprints
    from screen_rekod.auth.routes import auth
    from screen_rekod.user.routes import user

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(user)

    create_database(app)

    return app
