from flask import request, jsonify
from flask.views import MethodView
from src.repositories.user_repository import UserRepository
from src.models.user_model import User

class UserController(MethodView):
    def __init__(self):
        self.repository = UserRepository()
        self.model = User

    def get(self, id=None):
        
        if id is None:
            reponse = self.repository.get_all()
            return jsonify([e.to_dict() for e in reponse]), 200
        
        responseData = self.repository.get_by_id(id)
        if not responseData:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify(responseData.to_dict()), 200

    def post(self):
        
        data = request.get_json()
        if not data or 'namefull' not in data or 'login' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        novo_User = self.model.from_dict(data)
        novo_id = self.repository.create(novo_User)
        novo_User.id = novo_id
        return jsonify(novo_User.to_dict()), 201

    def put(self, id):
        data = request.get_json()
        User = self.model.from_dict(data)
        updated = self.repository.update(id, User)
        if not updated:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro atualizado com sucesso"}), 200

    def delete(self, id):
        deleted = self.repository.delete(id)
        if not deleted:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro removido com sucesso"}), 200