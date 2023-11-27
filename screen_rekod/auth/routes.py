from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from screen_rekod.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from screen_rekod.models.user import User
from screen_rekod import db

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))  # Redirect to home if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username_or_email.data) | (User.email == form.username_or_email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('user.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))  # Redirect to home if already logged in

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_email_user = User.query.filter_by(email=form.email.data).first()
        existing_username_user = User.query.filter_by(username=form.username.data).first()

        if existing_email_user:
            flash('Email already in use. Please choose another email.', 'danger')
            return render_template('register.html', form=form)

        if existing_username_user:
            flash('Username already in use. Please choose another username.', 'danger')
            return render_template('register.html', form=form)

        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please enter matching passwords.', 'danger')
            return render_template('register.html', form=form)

        # Create a new user instance
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)


        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.index'))  # Redirect to home after logout


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))  # Redirect to home if already logged in

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if not user:
            flash('Invalid email', 'danger')
            return render_template('reset_password.html', form=form)

        if form.new_password.data != form.confirm_new_password.data:
            flash('Passwords do not match. Please enter matching passwords.', 'danger')
            return render_template('reset_password.html', form=form)

        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password reset successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)


