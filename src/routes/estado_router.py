from flask import Blueprint
from src.controllers.estado_controller import EstadoController

class EstadoRoutes:
    @staticmethod
    def get_blueprint() -> Blueprint:
        # Cria o blueprint exclusivo do módulo
        bp = Blueprint('estados', __name__, url_prefix='/estados')
        
        # Mapeia as views
        estado_view = EstadoController.as_view('estado_api')
        
        # Rotas da coleção
        bp.add_url_rule(
            '', 
            view_func=estado_view, 
            methods=['GET', 'POST']
        )
        
        # Rotas do item por ID
        bp.add_url_rule(
            '/<int:id>', 
            view_func=estado_view, 
            methods=['GET', 'PUT', 'DELETE']
        )
        
        return bp