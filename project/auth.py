"""auth"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from .user import create_user, authenticate_user, disconnect_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login"""

    if current_user.is_authenticated:
        flash('You are already authenticated, logout first to access this page.')
        return redirect(url_for('main.profile'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = authenticate_user(email, password)

        if not user:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup"""

    if current_user.is_authenticated:
        flash('You are already authenticated, logout first to access this page.')
        return redirect(url_for('main.profile'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = create_user(email, username, password)

        if not user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/logout')
def logout():
    """logout"""

    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))

    disconnect_user(current_user)
    logout_user()
    return redirect(url_for('main.index'))
