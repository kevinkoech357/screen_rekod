from flask import Flask, render_template
from flask_cors import CORS
from screen_rekod.config import App_Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5


db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()


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
    bootstrap.init_app(app)

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

    # Import models
    from screen_rekod.models.user import User
    from screen_rekod.models.videos import Video

    with app.app_context():
        db.create_all()
        print("Database created successfully")

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    return app
