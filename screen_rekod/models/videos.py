from screen_rekod.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Video(db.Model):
    """
    Represents a video record associated with a user.

    Attributes:
        id (int): Unique identifier for the video.
        user_id (str): Foreign key referencing the user who uploaded the video.
        file_path (str): Path to the video file on the server.
        created_at (datetime): Timestamp indicating when the video was created.

    Relationships:
        user (User): Relationship to the User model to associate videos with their respective users.

    Methods:
        __init__(self, user, file_path,):
            Initializes a new Video instance.

        format(self):
            Converts the Video object to a dictionary for serialization.

    """

    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False
    )

    # Define a relationship between the Video and User models
    user = relationship("User", back_populates="videos")

    # Define the relationship between the Video and Subtitle models
    subtitles = db.relationship("Subtitle", back_populates="video")

    def __init__(self, user, file_path, created_at):
        """
        Initializes a new Video instance.

        Args:
            user (User): The user who uploaded the video.
            file_path (str): Path to the video file on the server.
        """
        self.user = user
        self.file_path = file_path
        self.created_at = created_at

    def format(self):
        """
        Converts the Video object to a dictionary for serialization.

        Returns:
            dict: A dictionary containing video attributes.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "file_path": self.file_path,
            "created_at": self.created_at,
        }
