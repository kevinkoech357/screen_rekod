import pytest
from screen_rekod import db
from screen_rekod.models.user import User
import uuid


def is_valid_uuidv4(user_id):
    """
    Check if a given string represents a valid UUIDv4.

    Args:
        user_id (str): The string to check.

    Returns:
        bool: True if the string is a valid UUIDv4, False otherwise.
    """
    try:
        uuid_obj = uuid.UUID(user_id)
        return uuid_obj.version == 4
    except ValueError:
        return False


@pytest.fixture
def user_fixture(app):
    """
    Fixture to set up a User instance in the database and retrieve it.

    Args:
        app: The Flask application.

    Returns:
        User: The retrieved User instance.
    """
    # Create a user instance
    user = User(
        username="testuser1", email="test1@example.com", password="password1234"
    )

    # Add user to the database
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Retrieve the user from the database
    retrieved_user = User.query.filter_by(email="test1@example.com").first()

    return retrieved_user


def test_user_model(user_fixture):
    """
    Test the User model by verifying various properties.

    Args:
        user_fixture (User): The User instance retrieved from the database.
    """
    # Use the user_fixture to get the user
    retrieved_user = user_fixture
    user_id = retrieved_user.id

    # Assert that the user is retrieved correctly
    assert retrieved_user is not None
    assert is_valid_uuidv4(user_id) is True
    assert retrieved_user.username == "testuser1"
    assert retrieved_user.check_password("password1234") is True


def test_known_user(user_fixture):
    """
    Test a known User instance by verifying various properties.

    Args:
        user_fixture (User): The User instance retrieved from the database.
    """
    # Use the user_fixture to get the user
    retrieved_user = user_fixture
    user_id = retrieved_user.id

    # Assert that the user is retrieved correctly
    assert retrieved_user is not None
    assert is_valid_uuidv4(user_id) is True
    assert retrieved_user.username == "testuser1"
    assert retrieved_user.check_password("password1234") is True
