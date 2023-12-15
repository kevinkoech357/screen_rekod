import pytest
from screen_rekod import db
from screen_rekod.models.videos import Video
from screen_rekod.models.user import User
from datetime import datetime


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

    return user


@pytest.fixture
def video_fixture(app, user_fixture):
    """
    Fixture to set up a Video instance associated with a User in the database and retrieve it.

    Args:
        app: The Flask application.
        user_fixture: The user_fixture fixture providing a User instance.

    Returns:
        Video: The retrieved Video instance.
    """
    # Create a video instance associated with the user
    video = Video(
        user=user_fixture,
        title="Test Video",
        description="This is a test video.",
        filename="test_video.mp4",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        sharing_token="random_token",
        browser_name="Chrome",
        browser_version="90.0",
        browser_layout="Blink",
        operating_system="Windows 10",
    )

    # Add video to the database
    with app.app_context():
        db.session.add(video)
        db.session.commit()

        # Refresh the video to ensure it's bound to the current session
        db.session.refresh(video)

    return video


def test_video_model(video_fixture):
    """
    Test the Video model by verifying various properties.

    Args:
        video_fixture (Video): The Video instance retrieved from the database.
    """
    # Use the video_fixture to get the video
    retrieved_video = video_fixture

    # Assert that the video is retrieved correctly
    assert retrieved_video is not None
    assert isinstance(retrieved_video.id, str)  # Assuming Video ID is a UUID string
    assert retrieved_video.title == "Test Video"
    assert retrieved_video.description == "This is a test video."
    assert retrieved_video.filename == "test_video.mp4"
    assert retrieved_video.sharing_token == "random_token"
    assert retrieved_video.browser_name == "Chrome"
    assert retrieved_video.browser_version == "90.0"
    assert retrieved_video.browser_layout == "Blink"
    assert retrieved_video.operating_system == "Windows 10"


def test_known_video(video_fixture):
    """
    Test a known Video instance by verifying various properties.

    Args:
        video_fixture (Video): The Video instance retrieved from the database.
    """
    # Use the video_fixture to get the video
    retrieved_video = video_fixture

    # Assert that the video is retrieved correctly
    assert retrieved_video is not None
    assert isinstance(retrieved_video.id, str)  # Assuming Video ID is a UUID string
    assert retrieved_video.title == "Test Video"
    assert retrieved_video.description == "This is a test video."
    assert retrieved_video.filename == "test_video.mp4"
    assert retrieved_video.sharing_token == "random_token"
    assert retrieved_video.browser_name == "Chrome"
    assert retrieved_video.browser_version == "90.0"
    assert retrieved_video.browser_layout == "Blink"
    assert retrieved_video.operating_system == "Windows 10"
