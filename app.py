from flask import Flask
from config import Config
from flask_cors import CORS
from extensions import bcrypt
from routes.routes import register_routes

app = Flask(__name__)

# parte 2
# O padrão CORS(app) libera para todas as origens (útil em desenvolvimento)
CORS(app)

app.config['SECRET_KEY'] = Config.SECRET_KEY

bcrypt.init_app(app)

# parte 3
# Registro das rotas
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=Config.PORT_API, debug=True)