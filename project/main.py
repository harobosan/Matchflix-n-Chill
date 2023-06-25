from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .db import db, User, Movies
from .movie import get_all_movies

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
#@login_requried
def profile():
    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=current_user, user_list= User.query.all())

@main.route('/movies', methods=['GET'])
#@login_requried
def get_movies():
    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))
    movies = get_all_movies()
    return render_template('movies.html', user=current_user, movies_list=movies)
