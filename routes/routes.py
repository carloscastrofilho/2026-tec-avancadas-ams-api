# routes/__init__.py
from flask import Flask
from .auth_routes import auth_bp
from .user_routes import users_bp
from .estados_routes import estados_bp

def register_routes(app: Flask):
    """
    Função central para registrar todos os Blueprints da aplicação.
    """
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(estados_bp, url_prefix='/api')