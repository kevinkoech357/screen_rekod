from screen_rekod.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from screen_rekod.models.user import User

class Video(db.Model):
    """
    Represents a video record associated with a user.

    Attributes:
        id (int): Unique identifier for the video.
        user_id (str): Foreign key referencing the user who uploaded the video.
        file_path (str): Path to the video file on the server.
        title (str): Title or name of the video (optional).
        description (str): Description or additional information about the video (optional).
        created_at (datetime): Timestamp indicating when the video was created.

    Relationships:
        user (User): Relationship to the User model to associate videos with their respective users.

    Methods:
        __init__(self, user, file_path, title=None, description=None):
            Initializes a new Video instance.

        format(self):
            Converts the Video object to a dictionary for serialization.

    """
    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    # Define a relationship between the Video and User models
    user = relationship("User", back_populates="videos")

    def __init__(self, user, file_path, title=None, description=None, created_at):
        """
        Initializes a new Video instance.

        Args:
            user (User): The user who uploaded the video.
            file_path (str): Path to the video file on the server.
            title (str, optional): Title or name of the video (default is None).
            description (str, optional): Description or additional information about the video (default is None).
        """
        self.user = user
        self.file_path = file_path
        self.title = title
        self.description = description
        self.created_at = created_at

    def format(self):
        """
        Converts the Video object to a dictionary for serialization.

        Returns:
            dict: A dictionary containing video attributes.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_path': self.file_path,
            'title': self.title,
            'description': self.description
            'created_at': self.created_at
        }
