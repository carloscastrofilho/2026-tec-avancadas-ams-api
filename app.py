import os
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_temporaria_muito_fraca')
TOKEN_LIFETIME_MINUTES = int(os.getenv('TOKEN_LIFETIME_MINUTES', 30))

# Configuração do Banco de Dados MySQL
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'fatecteste')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Middleware para proteger rotas (Verificação do JWT)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token ausente!, Nao autorizado.'}), 401
        try:
            # Removendo o prefixo "Bearer " se existir
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401
        return f(*args, **kwargs)
    return decorated

# --- ROTA DE AUTH (LOGIN) ---
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Credenciais obrigatórias'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (auth['username'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
            'user_id': user['id'],    
            'exp': datetime.now(timezone.utc) + timedelta(minutes=TOKEN_LIFETIME_MINUTES)            
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'token': token})

    return jsonify({'message': 'Usuário ou senha incorretos'}), 401

# --- CRUD DE USUÁRIOS ---

# CREATE (Registro)
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (data['username'], hashed_password))
        conn.commit()
        return jsonify({'message': 'Usuário criado com sucesso!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

# READ (Protegido)
@app.route('/user', methods=['GET'])
@token_required
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# GETBYID (Protegido)
@app.route('/user/<int:id>', methods=['GET'])
@token_required
def getbyid_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (id,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)
    

# DELETE (Protegido)
@app.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuário removido!'})

# CREATE (Registro)
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", 
                       (data['username'], hashed_password, id))
        conn.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()
        
if __name__ == '__main__':
    # Rodando na porta 3500 conforme solicitado
    app.run(port=3500, debug=True)