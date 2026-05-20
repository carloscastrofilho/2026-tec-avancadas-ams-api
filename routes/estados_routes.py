# parte1
from flask import Blueprint, request, jsonify
from database import get_db_connection
from extensions import bcrypt
from middlewares.auth_middleware import token_required
from controllers.estadoControllers import Create, GetAll, Delete, Put, GetById

# usando blueprint para injetar a rota users
estados_bp = Blueprint('estados', __name__)

@estados_bp.route('/estados', methods=['POST'])
def post():
   return Create()

@estados_bp.route('/estados', methods=['GET'])
#@token_required
def getAll():
    return GetAll()

@estados_bp.route('/estados/<int:id>', methods=['DELETE'])
# @token_required
def Apagar(id):
    return Delete(id)

@estados_bp.route('/estados/<int:id>', methods=['PUT'])
def Update(id):
    return Put(id)
    
@estados_bp.route('/estados/<int:id>', methods=['GET'])
#@token_required
def getByid(id):
    return GetById(id)    
