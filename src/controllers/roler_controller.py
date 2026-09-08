# parte 1
from flask.views import MethodView
from flask import jsonify

class RolerController(MethodView):
    """
    Controller responsável pelos endpoints da raiz da API.
    Cada método corresponde a um verbo HTTP.
    """
    def get(self):
        return jsonify({
        "status": "success",
        "message": "listagem regras"
        }), 200


    def post(self):
        # Aqui entraria a lógica de recebimento de dados (request.json)
        return jsonify({
        "status": "success",
        "message": "Registro criado com sucesso"
        }), 201
        
    def put(self):
            # Aqui entraria a lógica de recebimento de dados (request.json)
            return jsonify({
            "status": "success",
            "message": "Registro ALTERADO com sucesso"
            }), 201
                
    def delete(self):
            # Aqui entraria a lógica de recebimento de dados (request.json)
            return jsonify({
            "status": "success",
            "message": "Registro APAGADO com sucesso"
            }), 201        