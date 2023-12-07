from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from screen_rekod.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from screen_rekod.models.user import User
from screen_rekod import db
import logging

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

logger = logging.getLogger(__name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in a user.

    If the user is already authenticated, redirects to the dashboard.
    If the form is submitted and valid, logs in the user and redirects to the dashboard.
    """
    if current_user.is_authenticated:
        logger.warning(
            "User attempted to access login page while already authenticated."
        )
        return redirect(
            url_for("user.dashboard")
        )  # Redirect to dashboard if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.username == form.username_or_email.data)
            | (User.email == form.username_or_email.data)
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            logger.info("User %s logged in successfully.", user.username)
            flash("Login successful!", "success")
            return redirect(url_for("user.dashboard"))
        else:
            logger.warning(
                "Failed login attempt for user %s.", form.username_or_email.data
            )
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user.

    If the user is already authenticated, redirects to the dashboard.
    If the form is submitted and valid, creates a new user and redirects to the login page.
    """
    if current_user.is_authenticated:
        logger.warning(
            "User attempted to access registration page while already authenticated."
        )
        return redirect(
            url_for("user.dashboard")
        )  # Redirect to dashboard if already logged in

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_email_user = User.query.filter_by(email=form.email.data).first()
        existing_username_user = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_email_user:
            flash("Email already in use. Please choose another email.", "danger")
            logger.warning(
                "Registration failed. Email already in use: %s", form.email.data
            )
            return render_template("register.html", form=form)

        if existing_username_user:
            flash("Username already in use. Please choose another username.", "danger")
            logger.warning(
                "Registration failed. Username already in use: %s", form.username.data
            )
            return render_template("register.html", form=form)

        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match. Please enter matching passwords.", "danger")
            logger.warning("Registration failed. Passwords do not match.")
            return render_template("register.html", form=form)

        # Create a new user instance
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(new_user)
        db.session.commit()

        logger.info("User %s registered successfully.", new_user.username)
        flash("Registration successful! You can now log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """
    Log out the current user.

    Redirects to the home page after logout.
    """
    logger.info("User %s logged out.", current_user.username)
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("user.index"))  # Redirect to home after logout


@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """
    Reset user password.

    If the user is already authenticated, redirects to the dashboard.
    If the form is submitted and valid, resets the user's password and redirects to the login page.
    """
    if current_user.is_authenticated:
        logger.warning(
            "User attempted to access password reset page while already authenticated."
        )
        return redirect(
            url_for("user.dashboard")
        )  # Redirect to dashboard if already logged in

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if not user:
            logger.warning("Password reset failed. Invalid email: %s", form.email.data)
            flash("Invalid email", "danger")
            return render_template("reset_password.html", form=form)

        if form.new_password.data != form.confirm_new_password.data:
            logger.warning("Password reset failed. Passwords do not match.")
            flash("Passwords do not match. Please enter matching passwords.", "danger")
            return render_template("reset_password.html", form=form)

        user.set_password(form.new_password.data)
        db.session.commit()
        logger.info("User %s successfully reset their password.", user.username)
        flash("Password reset successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)
