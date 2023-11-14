from screen_rekod.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Subtitle(db.Model):
    """
    Represents subtitles associated with a video.

    Attributes:
        id (int): Unique identifier for the subtitles.
        video_id (int): Foreign key referencing the video for which subtitles are created.
        file_path (str): Path to the subtitles file on the server.
        created_at (datetime): Timestamp indicating when the subtitles were created.

    Relationships:
        video (Video): Relationship to the Video model to associate subtitles with their respective videos.

    Methods:
        __init__(self, video, file_path, created_at):
            Initializes a new Subtitle instance.

        format(self):
            Converts the Subtitle object to a dictionary for serialization.

    """

    __tablename__ = "subtitle"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False
    )

    # Define the relationship between the Subtitle and Video models
    video = db.relationship("Video", back_populates="subtitles")

    def __init__(self, video, file_path, created_at):
        """
        Initializes a new Subtitle instance.

        Args:
            video (Video): The video for which subtitles are created.
            file_path (str): Path to the subtitles file on the server.
            created_at (datetime): Timestamp indicating when the subtitles were created.
        """
        self.video = video
        self.file_path = file_path
        self.created_at = created_at

    def format(self):
        """
        Converts the Subtitle object to a dictionary for serialization.

        Returns:
            dict: A dictionary containing subtitle attributes.
        """
        return {
            "id": self.id,
            "video_id": self.video_id,
            "file_path": self.file_path,
            "created_at": self.created_at,
        }
