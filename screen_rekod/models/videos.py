from screen_rekod import db
from sqlalchemy.orm import relationship
from sqlalchemy import func


def generate_uuid():
    return str(uuid.uuid4())


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
        __init__(self, user, title, description, filename, created_at=None):
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
        db.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Define a relationship between the Video and User models
    user = relationship("User", back_populates="videos")

    def __init__(self, user, title, description, filename, created_at=None):
        """
        Initializes a new Video instance.

        Args:
            user (User): The user who uploaded the video.
            title (str): Title of the video.
            description (str): Description of the video.
            filename (str): Filename of the video.
        """
        self.user = user
        self.title = title
        self.description = description
        self.filename = filename
        self.created_at = created_at or db.func.current_timestamp()

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
            "created_at": self.created_at,
        }
