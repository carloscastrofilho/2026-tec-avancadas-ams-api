# parte 1
from flask.views import MethodView
from flask import jsonify

class HomeController(MethodView):
    """
    Controller responsável pelos endpoints da raiz da API.
    Cada método corresponde a um verbo HTTP.
    """
    def get(self):
        return jsonify({
        "status": "success",
        "message": "Bem-vindo a API Orientada a Objetos"
        }), 200


    def post(self):
        # Aqui entraria a lógica de recebimento de dados (request.json)
        return jsonify({
        "status": "success",
        "message": "Recurso criado com sucesso"
        }), 201