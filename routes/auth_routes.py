import jwt
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
from database import get_db_connection
from extensions import bcrypt
from config import Config

auth_bp = Blueprint('auth', __name__)

# parte 2
@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Credenciais obrigatórias'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (auth['username'],))
    # pega o valor do retorno da consulta
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and bcrypt.check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
             'user_id': user['id'],
            'exp': datetime.now(timezone.utc) + timedelta(minutes=Config.TOKEN_LIFETIME_MINUTES)
        }, Config.SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    
    return jsonify({'message': 'Usuário ou senha incorretos'}), 401
