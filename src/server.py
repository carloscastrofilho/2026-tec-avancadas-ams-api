from flask import Flask
from flask_cors import CORS

def server_app():
    """Fábrica de aplicação (Application Factory)"""
    app = Flask(__name__)
    
    #app.config.from_object(Config)
    #app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    CORS(app)
    
    #bcrypyt.init_app(app);    
    
    # rotas / view
    #routesApp(app)
    
    return app

if __name__ == '__main__':
    app = server_app()
    app.run(host='0.0.0.0', port=3600, debug=True)