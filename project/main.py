"""Módulo principal"""

from flask import Blueprint
from flask import render_template, send_from_directory, url_for, redirect, request, flash
from flask_login import current_user
from .user import get_all_users, get_relationship_lists, is_admin
from .user import update_email, update_username, update_password
from .relationship import create_relationship, delete_relationship, update_status
from .movie import get_all_movies, get_movie, create_movie, delete_movie
from .preference import get_user_preferences, create_preference, delete_preference, update_movie


main = Blueprint('main', __name__)


@main.route('/favicon.ico')
def favicon():
    """
    Rota para acessar o arquivo favicon.ico.

    Return:
        send_from_directory: Arquivo favicon.ico.
    """

    return send_from_directory('static','favicon.ico')

@main.route('/')
def index():
    """
    Rota para a página inicial.

    Return:
        render_template: Página index.html.
    """

    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Rota para a página de perfil do usuário.

    Return:
        render_template: Página profile.html.
    """

    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if request.form.get("edit"):
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("password")

            if email:
                if not update_email(current_user, email):
                    flash('Email already in use.')
                    return redirect(url_for('main.profile'))

            if username:
                update_username(current_user, username)

            if password:
                update_password(current_user, password)

        if request.form.get("unfriend"):
            uid = request.form.get("unfriend")
            delete_relationship(uid, current_user.id)

        if request.form.get("befriend"):
            uid = request.form.get("befriend")
            create_relationship(current_user.id, uid)

        if request.form.get("reject"):
            uid = request.form.get("reject")
            delete_relationship(uid, current_user.id)

        if request.form.get("accept"):
            uid = request.form.get("accept")
            update_status(uid, current_user.id)

    rel_lists = get_relationship_lists(current_user.id)

    return render_template(
        'profile.html',
        user=current_user,
        user_list=get_all_users(),
        friends=rel_lists[0],
        pending=rel_lists[1],
        requests=rel_lists[2],
        recommendations=rel_lists[3]
    )

@main.route('/movies', methods=['GET', 'POST'])
def movies():
    """
    Rota para a página de filmes.

    Return:
        render_template: Página movies.html.
    """

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
                delete_movie(request.form.get("remove"))

                for movie in get_all_movies():
                    update_movie(movie.id, 0)

            elif request.form.get('add'):
                if privileged:
                    name = request.form.get("title")

                    if name:
                        create_movie(name,'imageExample.jpeg')

    return render_template(
        'movies.html',
        movies=get_all_movies(),
        privileged=privileged,
        preferences=preferences
    )
