Para aplicar autenticação JWT (ou qualquer outra validação) especificamente em um Blueprint no Flask usando Orientação a Objetos, você pode utilizar o hook nativo **`before_request`** do próprio Blueprint.

Isso garante que **todas as requisições** direcionadas àquele Blueprint passem pelo middleware automaticamente, sem a necessidade de decorar método por método dentro do Controller.

---

### 1. Criando o Middleware (`auth_middleware.py`)

Crie uma classe responsável por extrair e validar o Token JWT do cabeçalho `Authorization`:

`src/middlewares/auth_middleware.py`

```python
import jwt
from flask import request, jsonify
from src.utils.config import Config

class AuthMiddleware:
    @staticmethod
    def verify_jwt():
        """
        Método chamado antes de qualquer requisição do Blueprint protegido.
        Se o token for inválido, interrompe o fluxo retornando JSON e HTTP Status.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token de autenticação não fornecido"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Formato do cabeçalho Authorization inválido. Use 'Bearer <token>'"}), 401

        token = parts[1]

        try:
            # Decodifica o token usando a chave secreta definida na configuração
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            # Injeta os dados do usuário no contexto global da requisição se precisar acessar no Controller
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

```

---

### 2. Vinculando o Middleware ao Blueprint (`estado_routes.py`)

No arquivo de rotas do módulo, registre a função `AuthMiddleware.verify_jwt` no hook `before_request` do Blueprint usando `bp.before_request(...)`:

`src/modules/estado/estado_routes.py`

```python
from flask import Blueprint
from src.modules.estado.estado_controller import EstadoController
from src.middlewares.auth_middleware import AuthMiddleware

class EstadoRoutes:
    @staticmethod
    def get_blueprint() -> Blueprint:
        bp = Blueprint('estados', __name__, url_prefix='/estados')

        # VINCULA O MIDDLEWARE APENAS A ESTE BLUEPRINT:
        # Qualquer rota que pertença a este Blueprint executará esta checagem antes do Controller
        bp.before_request(AuthMiddleware.verify_jwt)

        # Mapeamento do Controller
        estado_view = EstadoController.as_view('estado_api')

        bp.add_url_rule(
            '', 
            view_func=estado_view, 
            methods=['GET', 'POST']
        )
        
        bp.add_url_rule(
            '/<int:id>', 
            view_func=estado_view, 
            methods=['GET', 'PUT', 'DELETE']
        )

        return bp

```

---

### 3. Cenários Especiais: Exceções em Rotas do Mesmo Blueprint

Se o seu módulo possuir rotas públicas (por exemplo: um `GET /estados` público para listagem, mas `POST`, `PUT` e `DELETE` protegidos), você pode validar a rota/método dentro do middleware ou no próprio `before_request`:

```python
@staticmethod
def get_blueprint() -> Blueprint:
    bp = Blueprint('estados', __name__, url_prefix='/estados')

    # Exemplo: Proteger apenas operações de escrita no Blueprint
    @bp.before_request
    def check_auth_for_write_operations():
        if request.method in ['POST', 'PUT', 'DELETE']:
            return AuthMiddleware.verify_jwt()

    # Mapeamento de rotas continua igual...
    return bp

```

---

### Resumo do Fluxo

1. A requisição chega para `/api/v1/estados`.
2. O Flask identifica o Blueprint `estados`.
3. O evento `before_request` é disparado e executa `AuthMiddleware.verify_jwt()`.
4. **Token Inválido/Ausente:** Retorna `401 Unauthorized` imediatamente, sem chegar no Controller ou no Banco de Dados.
5. **Token Válido:** O fluxo prossegue para o método correspondente do `EstadoController`.