from flask import Flask
from screen_rekod.extensions import db
from screen_rekod.utils import create_database

def create_app():
    app = Flask(__name__)

    db.init(app)

    create_database(app)

    return app
