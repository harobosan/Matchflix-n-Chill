"""Módulo de autenticação"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from .user import create_user, authenticate_user, disconnect_user


auth = Blueprint('auth', __name__)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: login()
Assertivas de Entrada:
Nenhuma especifíca
Assertivas de Saída:
Se o Usuário está Autenticado
    Redireciona para a página principal
Senão
    É renderizada a página de login
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para a página de login.

    Return:
        render_template: Página login.html.
    """

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: signup()
Assertivas de Entrada:
Nenhuma pré-condição especifíca
Assertivas de Saída:
Se o usuário já está autenticado
    Retorna redirecionamento para a página principal
Senão
    É renderizada uma página de cadastro(signup)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Rota para a página de cadastro.

    Return:
        render_template: Página signup.html.
    """

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


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: logout()
Assertivas de Entrada:
Nenhuma Pré-Condição especifíca
Assertivas de Saída:
Se o usuário não está logado
    Retorna um redirecionamento para a página de login
Senão
    Retorna um redirecionamento para a página principal
    user.authenticated = False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@auth.route('/logout')
def logout():
    """
    Rota para realizar o logout.

    Return:
        redirect: Redireciona para a página inicial.
    """

    if not current_user.is_authenticated:
        flash('Please, authenticate to access this page.')
        return redirect(url_for('auth.login'))

    disconnect_user(current_user)
    logout_user()
    return redirect(url_for('main.index'))
