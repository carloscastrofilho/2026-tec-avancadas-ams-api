# parte 1
from flask import Blueprint
from src.controllers.home_controller import HomeController
from src.controllers.user_controller import UserController
from src.controllers.roler_controller import RolerController

class Router:
    def __init__(self, app):
        """
        Recebe a instância do app Flask para registrar as rotas.
        """
        self.app = app
        
    def register(self):
        """
        Fábrica de rotas: Instancia os blueprints e mapeia os controllers.
        """
        
        # Criação de um Blueprint para agrupar rotas da API (ex: /api/v1)
        api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
        # Registro do HomeController
        # O método as_view() transforma a classe em uma view function que o Flask entende
        api_bp.add_url_rule(
            '/',
            view_func=HomeController.as_view('home_controller')
            )
        #parte 3
        # Adicione outros controllers aqui no futuro, ex:
        api_bp.add_url_rule('/users', view_func=UserController.as_view('user_controller'))
        
        api_bp.add_url_rule('/roles', view_func=RolerController.as_view('roler_controller'))
        # Finalmente, registra o blueprint no app principal
        self.app.register_blueprint(api_bp)