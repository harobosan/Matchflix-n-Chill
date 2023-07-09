"""main"""

from flask import Blueprint
from flask import render_template, send_from_directory, url_for, redirect, request, flash
from flask_login import current_user
from .user import get_all_users, is_admin
from .movie import get_all_movies, get_movie, create_movie, delete_movie
from .preference import get_user_preferences, create_preference, delete_preference


main = Blueprint('main', __name__)


@main.route('/favicon.ico')
def favicon():
    """favicon"""

    return send_from_directory('static','favicon.ico')

@main.route('/')
def index():
    """index"""

    return render_template('index.html')

@main.route('/profile')
def profile():
    """profile"""

    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))

    return render_template('profile.html', user=current_user, user_list=get_all_users())

@main.route('/movies', methods=['GET', 'POST'])
def movies():
    """movies"""

    privileged = False
    preferences = None
    if current_user.is_authenticated:
        privileged = is_admin(current_user.id)
        preferences = get_user_preferences(current_user.id)

    if request.method == 'POST':

        if current_user.is_authenticated:

            if request.form.get("like"):
                mid = get_movie(request.form.get("like")).id
                create_preference(current_user.id, mid)
                preferences.append(mid)

            elif request.form.get("dislike"):
                mid = get_movie(request.form.get("dislike")).id
                delete_preference(current_user.id, mid)
                preferences.remove(mid)

            elif request.form.get("remove"):
                #mid = get_movie(request.form.get("remove")).id
                delete_movie(request.form.get("remove"))

                #if mid in preferences:
                #    preferences.remove(mid)

    return render_template(
        'movies.html',
        movies=get_all_movies(),
        privileged=privileged,
        preferences=preferences
    )
