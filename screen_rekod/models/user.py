from screen_rekod.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from screen_rekod.models.video import Video

class User(db.Model):
    """
    User model for representing user data.

    Attributes:
        id (str): Unique user identifier.
        first_name (str): User's first name.
        middle_name (str): User's middle name (optional).
        last_name (str): User's last name.
        password (str): User's password.
        created_at (datetime): Timestamp of when the user was created.

    Relationships:
        videos (List[Video]): A list of videos associated with the user.

    """
    __tablename__ = "user"

    id = db.Column(db.String(32), primary_key=True, default=generate_uuid, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(66), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    # Define the relationship with the Video model
    videos = relationship("Video", back_populates="user")

    def __init__(self, first_name, last_name, middle_name=None, password, created_at):
        """
        Initialize a new User instance.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            middle_name (str, optional): User's middle name (default is None).
            password (str): User's password.
            created_at (datetime): Timestamp of when the user was created.
        """
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        """
        Return an official object representation.

        Returns:
            str: Object representation.
        """
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"

    def format(self):
        """
        Format the object's attributes as a dictionary.

        Returns:
            dict: Dictionary containing user attributes.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "password": self.password,
            "created_at": self.created_at
        }
