from flask import Flask
from src.utils.config import Config
from src.controllers.estado_controller import EstadoAPI

class Api:
    # atributo de classe
    version = "0.0.0"
    
    # constructor
    def __init__(self ):
        #atributos
        ## publico
        ## privado
         # atributos privados
        self.__app_name = "teste 2"
        
        ## protegido
        self.__port = 3000
        self.__debug = True     
        # configuracoes
        self.cfg = Config()
        
        # instância do flask
        self.app = Flask(self.cfg.APP_NAME)
        self._register_routes()
        
    def _register_routes(self):
        # Mapeamento do Class-Based View
        estado_view = EstadoAPI.as_view('estado_api')
                
        # Rota para coleção (GET all, POST)
        self.app.add_url_rule(
            '/api/estados', 
            view_func=estado_view, 
            methods=['GET', 'POST']
        )
        
        # Rota para item específico (GET id, PUT, DELETE)
        self.app.add_url_rule(
            '/api/estados/<int:id>', 
            view_func=estado_view, 
            methods=['GET', 'PUT', 'DELETE']
        )
  
        
    # metodos
    def run(self):  
        self.__app_name = self.cfg.APP_NAME
        self.__port = self.cfg.APP_PORT
        self.__debug = self.cfg.APP_DEBUG  
        self.app.run(host='0.0.0.0', port=self.__port, debug=self.__debug)
        
    ## leitura
    ## gravacao
    # método de instância
    def get_project_name(self):
        return self.__app_name

    # método estático
    @staticmethod
    def framework():
        return "Flask Framework"

    # método de classe
    @classmethod
    def get_version(self):
        return self.version