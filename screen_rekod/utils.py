from screen_rekod.extensions import db


def create_database(app):
    """
    Create Database
    """

    with app.app_context():
        db.create_all()
        print("Database created successfully")
