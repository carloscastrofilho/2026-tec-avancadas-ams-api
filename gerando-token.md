Resposta para a sua dúvida sobre o `before_request` no `router.py`: **Sim, perfeitamente!**

Se você aplicar o `before_request` no Blueprint pai `api_v1`, o Flask aplicará em cascata a verificação de autenticação para **todos os sub-blueprints** registrados nele (`/estados`, `/users`, etc.).

A única exceção será o módulo de **Auth/Login**, que precisa ser registrado **fora** do Blueprint protegido (ou em um Blueprint separado sem o hook) para permitir o acesso público.

---

### 1. Ajuste no `router.py` (Protegendo em cascata)

```python
from flask import Flask, Blueprint
from src.modules.auth.auth_routes import AuthRoutes
from src.modules.estado.estado_routes import EstadoRoutes
from src.middlewares.auth_middleware import AuthMiddleware

class Router:
    def __init__(self, app: Flask):
        self.app = app

    def register(self):
        # 1. Blueprint PÚBLICO (sem validação de token)
        public_v1 = Blueprint('public_v1', __name__, url_prefix='/api/v1')
        public_v1.register_blueprint(AuthRoutes.get_blueprint())
        self.app.register_blueprint(public_v1)

        # 2. Blueprint PROTEGIDO (com before_request global para todos os módulos filhos)
        protected_v1 = Blueprint('protected_v1', __name__, url_prefix='/api/v1')
        protected_v1.before_request(AuthMiddleware.verify_jwt)

        # Todos os módulos registrados aqui exigirão token em TODAS as rotas/métodos
        protected_v1.register_blueprint(EstadoRoutes.get_blueprint())
        # protected_v1.register_blueprint(UserRoutes.get_blueprint())

        self.app.register_blueprint(protected_v1)

```

---

### 2. Módulo de Auth: Gerando o Token JWT no Login

Abaixo está a implementação completa da geração de token JWT seguindo o padrão de camadas (Repository, Controller, Routes).

#### 2.1. Repositório de Usuário (`user_repository.py`)

Busca as credenciais do usuário e a hash da senha no banco de dados:

```python
from src.database.connection import Database
from typing import Optional, Dict

class UserRepository:
    def __init__(self):
        self.db = Database()

    def get_by_email(self, email: str) -> Optional[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, email, senha_hash FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            return user

```

#### 2.2. Controller de Autenticação (`auth_controller.py`)

Valida a senha com `bcrypt` e assina o token com expiração definida nas configurações:

```python
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify
from flask.views import MethodView
from src.modules.user.user_repository import UserRepository
from src.utils.config import Config

class AuthController(MethodView):
    def __init__(self):
        self.user_repository = UserRepository()

    def post(self):
        data = request.get_json() or {}
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        user = self.user_repository.get_by_email(email)
        if not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        # Validação da hash da senha
        if not bcrypt.checkpw(senha.encode('utf-8'), user['senha_hash'].encode('utf-8')):
            return jsonify({"error": "Credenciais inválidas"}), 401

        # Criação do Payload do JWT
        payload = {
            "sub": user['id'],
            "nome": user['nome'],
            "email": user['email'],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=Config.TOKEN_LIFETIME_MINUTES)
        }

        # Geração da assinatura do token
        token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

        return jsonify({
            "message": "Login realizado com sucesso",
            "token": token,
            "expires_in_minutes": Config.TOKEN_LIFETIME_MINUTES
        }), 200

```

#### 2.3. Rotas de Autenticação (`auth_routes.py`)

Mapeia o endpoint `/api/v1/auth/login`:

```python
from flask import Blueprint
from src.modules.auth.auth_controller import AuthController

class AuthRoutes:
    @staticmethod
    def get_blueprint() -> Blueprint:
        bp = Blueprint('auth', __name__, url_prefix='/auth')
        auth_view = AuthController.as_view('auth_api')

        bp.add_url_rule('/login', view_func=auth_view, methods=['POST'])

        return bp

```

---

### Resumo das URLs Finais

* **`POST /api/v1/auth/login`**: Púbico (sem `before_request`). Retorna o Bearer Token.
* **`GET /api/v1/estados`**: Protegido em cascata via `protected_v1.before_request`. Exige o cabeçalho `Authorization: Bearer <token>`.