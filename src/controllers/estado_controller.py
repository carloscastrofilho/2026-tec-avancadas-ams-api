from flask import request, jsonify
from flask.views import MethodView
from src.repositories.estado_repository import EstadoRepository
from src.models.estado_model import Estado

class EstadoController(MethodView):
    def __init__(self):
        self.repository = EstadoRepository()
        self.model = Estado

    def get(self, id=None, estado=None):
        
        if estado:
            estado = self.repository.get_by_estado(estado)
            if not estado:
                return jsonify({"error": "Registro não encontrado"}), 404
            return jsonify(estado.to_dict()), 200    
        
        if id :
            estado = self.repository.get_by_id(id)
            if not estado:
               return jsonify({"error": "Registro não encontrado"}), 404
            return jsonify(estado.to_dict()), 200    
            
        estados = self.repository.get_all()
        return jsonify([e.to_dict() for e in estados]), 200
        
        

    def post(self):
        
        data = request.get_json()
        
        if not data or 'estado' not in data or 'uf' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        novo_estado = self.model.from_dict(data)
        novo_id = self.repository.create(novo_estado)
        novo_estado.id = novo_id
        return jsonify(novo_estado.to_dict()), 201

    def put(self, id):
        data = request.get_json()
        estado = self.model.from_dict(data)
        updated = self.repository.update(id, estado)
        if not updated:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro atualizado com sucesso"}), 200

    def delete(self, id):
        deleted = self.repository.delete(id)
        if not deleted:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro removido com sucesso"}), 200