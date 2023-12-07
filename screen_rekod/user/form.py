from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    """
    Form for user contact.

    Attributes:
        name (StringField): The user's name.
        email (StringField): The user's email address.
        message (TextAreaField): The user's message.
    """

    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Your Message", validators=[DataRequired()])
