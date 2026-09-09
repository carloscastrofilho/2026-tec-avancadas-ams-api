from flask import Flask, Blueprint
from src.routes.estado_router import EstadoRoutes
# Importe os outros módulos conforme for criando:
# from src.modules.user.user_routes import UserRoutes

class Router:
    def __init__(self, app: Flask):
        self.app = app

    def register(self):
        
        # Blueprint pai para versionamento da API
        api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

        # Registra os Blueprints dos módulos dentro do Blueprint v1
        api_v1.register_blueprint(EstadoRoutes.get_blueprint())
        
        # api_v1.register_blueprint(UserRoutes.get_blueprint())

        # Registra o pacote v1 na aplicação Flask principal
        self.app.register_blueprint(api_v1)