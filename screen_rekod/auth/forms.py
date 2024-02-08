from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """
    Form for user login.
    """

    username_or_email = StringField(
        "Username or Email", validators=[validators.DataRequired()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class ResetPasswordForm(FlaskForm):
    """
    Form for resetting user password.
    """

    email = StringField(
        "Email", validators=[validators.DataRequired(), validators.Email()]
    )
    new_password = PasswordField("New Password", validators=[validators.DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[validators.DataRequired(), validators.EqualTo("new_password")],
    )
    submit = SubmitField("Reset Password")
