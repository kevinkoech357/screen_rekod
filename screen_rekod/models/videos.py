from datetime import datetime
from screen_rekod import db
from sqlalchemy.orm import relationship
import uuid
import secrets


# Helper function to generate a random UUID
def generate_uuid():
    return str(uuid.uuid4())


# Helper function to generate a random sharing token
def generate_sharing_token():
    return secrets.token_urlsafe(16)


class Video(db.Model):
    """
    Represents a video record associated with a user.

    Attributes:
        id (str): Unique identifier for the video.
        user_id (str): Foreign key referencing the user who uploaded the video.
        title (str): Title of the video.
        description (str): Description of the video.
        filename (str): Filename of the video.
        created_at (datetime): Timestamp indicating when the video was created.

    Relationships:
        user (User): Relationship to the User model to associate videos with their respective users.

    Methods:
        __init__(self, user, title, description, filename, created_at=None, screen_size=None, browser_info=None, operating_system=None):
            Initializes a new Video instance.

        format(self):
            Converts the Video object to a dictionary for serialization.

    """

    __tablename__ = "video"

    id = db.Column(
        db.String(32), primary_key=True, default=generate_uuid, nullable=False
    )
    user_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False,
    )

    # Additional columns for  sharing token , browser and OS
    sharing_token = db.Column(db.String(32), unique=True, nullable=False)
    browser_name = db.Column(db.String(50), nullable=True)
    browser_version = db.Column(db.String(50), nullable=True)
    browser_layout = db.Column(db.String(50), nullable=True)
    operating_system = db.Column(db.String(50), nullable=True)

    # Define a relationship between the Video and User models
    user = relationship("User", back_populates="videos")

    def __init__(
        self,
        user,
        title,
        description,
        filename,
        created_at=None,
        sharing_token=None,
        browser_name=None,
        browser_version=None,
        browser_layout=None,
        operating_system=None,
    ):
        """
        Initializes a new Video instance.

        Args:
            user (User): The user who uploaded the video.
            title (str): Title of the video.
            description (str): Description of the video.
            filename (str): Filename of the video.
            created_at (datetime): Timestamp indicating when the video was created.
            sharing_token: Random strong to enable video share.
            browser_name: Name of browser.
            browser_version: Version of browser.
            browser_layout: Browser's layout engine.
            operating_system: Type of OS.
        """
        self.user = user
        self.title = title
        self.description = description
        self.filename = filename
        self.created_at = created_at or datetime.utcnow()
        self.sharing_token = sharing_token or generate_sharing_token()
        self.browser_name = browser_name
        self.browser_version = browser_version
        self.browser_layout = browser_layout
        self.operating_system = operating_system

    def format(self):
        """
        Converts the Video object to a dictionary for serialization.

        Returns:
            dict: A dictionary containing video attributes.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "filename": self.filename,
            "sharing_token": self.sharing_token,
            "browser_name": self.browser_name,
            "browser_version": self.browser_version,
            "browser_layout": self.browser_layout,
            "operating_system": self.operating_system,
            "created_at": self.created_at,
        }
