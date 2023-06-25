from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from .db import db, User
from .user import userAuthenticates

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already authenticated, logout first to access this page.')
        return redirect(url_for('main.profile'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if userAuthenticates(email, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        current_user.authenticated = True
        db.session.commit()
        return redirect(url_for('main.profile'))

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are already authenticated, logout first to access this page.')
        return redirect(url_for('main.profile'))
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        db.session.add(User(email=email, username=username, password=generate_password_hash(password, method='sha256'), authenticated=False))
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/logout')
def logout():
    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))
    current_user.authenticated = False
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))
