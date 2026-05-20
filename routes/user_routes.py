# parte1
from flask import Blueprint, request, jsonify
from database import get_db_connection
from extensions import bcrypt
from middlewares.auth_middleware import token_required

# usando blueprint para injetar a rota users
users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( "INSERT INTO users (username, password ) VALUES (%s, %s)",
        (data['username'], hashed_password,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuário criado'}), 201

@users_bp.route('/users', methods=['GET'])
#@token_required
def getAll():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@users_bp.route('/users/<int:id>', methods=['DELETE'])
# @token_required
def Delete(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM users WHERE id = %s",[id],)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users), 401

@users_bp.route('/users/<int:id>', methods=['PUT'])
def put(id):
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( "UPDATE users SET username = %s , password = %s WHERE id = %s",
           (data['username'], hashed_password,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'registro atualizado'}), 203

@users_bp.route('/users/<int:id>', methods=['GET'])
#@token_required
def getByid(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s",[id],)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users) , 206

