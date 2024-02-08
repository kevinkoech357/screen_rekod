import pytest
from screen_rekod import db
from screen_rekod.models.user import User
from screen_rekod.auth.forms import LoginForm


@pytest.fixture
def user_fixture(app):
    """Fixture to create a user for testing."""
    # Create a user instance
    user = User(
        username="testuser1", email="test1@example.com", password="password1234"
    )

    # Add user to the database
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        # Refresh the user to ensure it's bound to the current session
        db.session.refresh(user)

    return user


@pytest.fixture
def authenticated_client(user_fixture, client):
    # Log in the user before each test
    with client:
        client.post(
            "/login",
            data={"username_or_email": user_fixture.email, "password": "password1234"},
        )
        yield client


def test_login_route(client, user_fixture):
    """Test the login route functionality."""
    # Access the login page
    response = client.get("/login")
    assert response.status_code == 200

    # Test logging in with valid credentials
    form = LoginForm(username_or_email="test1@example.com", password="password1234")
    response = client.post("/login", data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login successful!" in response.data

    # Test logging in with invalid credentials
    form = LoginForm(username_or_email="test1@example.com", password="wrong_password")
    response = client.post("/login", data=form.data, follow_redirects=True)
    assert response.status_code == 200


def test_register_route(client):
    """Test the register route functionality."""
    # Access the register page
    response = client.get("/register")
    assert response.status_code == 200

    # Test registering a new user
    form_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
        "confirm_password": "newpassword",
    }
    response = client.post("/register", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful!" in response.data

    # Assert that the user is redirected to the login page after successful registration
    assert b"Login" in response.data


def test_logout_route(authenticated_client):
    """Test the logout route functionality."""
    response = authenticated_client.get("/logout", follow_redirects=True)

    # Assert that the user is logged out and redirected to the home page
    assert response.status_code == 200
    assert b"You have been logged out." in response.data
    assert b"Login" in response.data
