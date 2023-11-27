from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from screen_rekod import db
from sqlalchemy.orm import relationship
from sqlalchemy import func
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    """
    User model for representing user data.

    Attributes:
        id (str): Unique user identifier.
        username (str): User's last name.
        email (str): User's email address.
        password_hash (str): Hashed user password.
        created_at (datetime): Timestamp of when the user was created.

    Relationships:
        videos (List[Video]): A list of videos associated with the user.
    """

    __tablename__ = "user"

    id = db.Column(
        db.String(32), primary_key=True, default=generate_uuid, nullable=False
    )
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Define the relationship with the Video model
    videos = db.relationship("Video", back_populates="user")

    def __init__(self, username, email, password):
        """
        Initialize a new User instance.

        Args:
            username (str): User's username.
            email (str): User's email.
            password (str): User's password.
        """
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """
        Set the user's password by hashing the provided password.

        Args:
            password (str): The plain-text password to be hashed.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plain-text password to be checked.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Return an official object representation.

        Returns:
            str: Object representation.
        """
        return f"<User(id={self.id}, username={self.username}, email={self.email}, created_at={self.created_at})>"

    def format(self):
        """
        Format the object's attributes as a dictionary.

        Returns:
            dict: Dictionary containing user attributes.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
        }
