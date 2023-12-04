from flask import Flask, render_template
from flask_cors import CORS
from screen_rekod.config import App_Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
import logging
import os
from logging.handlers import RotatingFileHandler

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    # Initialize Flask
    app = Flask(__name__)

    # Load configuration from App_Config
    app.config.from_object(App_Config)

    # Allow URLs with or without trailing slashes
    app.url_map.strict_slashes = False

    # Initialize CORS
    CORS(app)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Ensure that the 'logs' directory exists
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Create a specific logger instance for the application
    logger = logging.getLogger(__name__)

    # Configure a rotating file handler
    log_file = os.path.join(log_dir, "screen_rekod.log")
    log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.DEBUG)

    # Set a custom log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )
    log_handler.setFormatter(formatter)

    # Add the rotating file handler to the logger
    logger.addHandler(log_handler)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load a user from the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            User: The user object.
        """
        return User.query.get(user_id)

    # Import blueprints
    from screen_rekod.auth.routes import auth
    from screen_rekod.user.routes import user
    from screen_rekod.video.routes import video
    from screen_rekod.share.routes import share

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(video)
    app.register_blueprint(share)

    # Import models
    from screen_rekod.models.user import User
    from screen_rekod.models.videos import Video

    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database created successfully")

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """
        Handle 404 errors.

        Args:
            error: The error information.

        Returns:
            tuple: The rendered 404 page and the HTTP status code.
        """
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Handle 500 errors.

        Args:
            error: The error information.

        Returns:
            tuple: The rendered 500 page and the HTTP status code.
        """
        return render_template("500.html"), 500

    return app
