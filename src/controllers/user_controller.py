# parte 1
from flask.views import MethodView
from flask import jsonify
import mysql.connector
from src.utils.config import Config



class UserController(MethodView):
    def __init__(self ):
        self.cfg = Config()
        
    def get_db_connection(self):
        return mysql.connector.connect(self.cfg().DB_CONFIG)
    """
    Controller responsável pelos endpoints da raiz da API.
    Cada método corresponde a um verbo HTTP.
    """
    def get(self):
        
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users), 200
        # return jsonify({
        # "status": "success",
        # "message": "listagem usuarios"
        # }), 200


    def post(self):
        # Aqui entraria a lógica de recebimento de dados (request.json)
        return jsonify({
        "status": "success",
        "message": "Usuario criado com sucesso"
        }), 201