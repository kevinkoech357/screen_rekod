from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from screen_rekod.auth.forms import LoginForm, RegistrationForm
from screen_rekod.models.user import User
from screen_rekod.extensions import db

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))  # Redirect to home if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
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
            return redirect(url_for('auth.register'))

        if existing_username_user:
            flash('Username already in use. Please choose another username.', 'danger')
            return redirect(url_for('auth.register'))

        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please enter matching passwords.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
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
