"""__init__"""

from flask import Flask
from flask_login import LoginManager
from .db import db, User
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Função: create_app()
Assertivas de Entrada:
Nenhuma pré-condição especifíca
Assertivas de Saída:
A função cria um objeto da aplicação Flask.
Configura a chave secreta (SECRET_KEY) da aplicação.
Configura a URI do banco de dados (SQLALCHEMY_DATABASE_URI) para usar o SQLite com o arquivo db.sqlite.
Inicializa o banco de dados (db) associando-o à aplicação Flask e cria todas as tabelas necessárias com db.create_all().
Inicializa o LoginManager para gerenciar a autenticação de usuários.
Define a rota de login (login_view) para a view auth.login do blueprint auth.
Implementa a função load_user para o LoginManager, que carrega um objeto User com base no user_id.
Registra os blueprints auth e main na aplicação Flask.
Retorna o objeto da aplicação Flask criado.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_app():
    """
    Cria a aplicação Flask.

    Return:
        app: Objeto da aplicação Flask.
    """

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
