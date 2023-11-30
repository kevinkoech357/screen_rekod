import os
from dotenv import load_dotenv

load_dotenv(".env")


class App_Config:
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get("SECRET_KEY", "hello_world!")
    # Database URI. Default is SQLite in-memory database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///test.db"
    )
    # Disable modification tracking for SQLAlchemy, unless explicitly set to True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Disable echoing SQL statements to the console
    SQLALCHEMY_ECHO = False
    # Flashed message duration
    MESSAGE_FLASHING_OPTIONS = {"duration": 5}
    SESSION_PERMANENT = False
    # Video uploads folder
    UPLOAD_FOLDER = "uploads"
