from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from .user import get_all_users#, Movies
from .movie import get_all_movies

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))

    return render_template('profile.html', user=current_user, user_list=get_all_users())

@main.route('/movies')
def movies():
    return render_template('movies.html', filmes = get_all_movies())
