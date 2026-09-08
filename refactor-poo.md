---
marp: true
---
## Refatoramento para sala de aula 02/09/2026

* Para evoluir a aplicação procedural para Orientação a Objetos (POO) com bons padrões de projeto (Design Patterns), a estrutura recomendada separa as responsabilidades em camadas claras: 
**Database Manager** (Singleton para o Connection Pool);
**Repository Pattern** (abstração de acesso a dados);
**Class-Based Views / Controllers** (camada da API);

---

### Arquitetura Proposta

```bash
src/
├── database/
│   └── connection.py       # Database Connection Pool (Singleton Pattern)
├── models/
│   └── estado_model.py     # Entidade (Objeto de Dominio)
├── repositories/
│   └── estado_repository.py# Repository Pattern (Queries / SQL)
├── controllers/
│   └── estado_controller.py# Class-Based View (Flask.views.MethodView)
└── api.py                  # Inicializacao e rotas

```

---

### 1. Conexão e Connection Pool (Singleton Pattern)

* O padrão **Singleton** garante que exista apenas uma instância do gerenciador de pool de conexões ativo durante o ciclo de vida do servidor (usando `mysql.connector.pooling`):

`src/database/connection.py`

```python
import mysql.connector.pooling
from contextlib import contextmanager
from src.utils.config import Config

class Database:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        self._pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            pool_reset_session=True,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

    @contextmanager
    def get_connection(self):
        """Context Manager para obter e devolver conexoes do pool com seguranca."""
        connection = self._pool.get_connection()
        try:
            yield connection
        finally:
            connection.close()  # Retorna a conexao para o pool

```

---

### 2. Entidade de Domínio (Modelo)

Representa a tabela `estados` como um objeto Python com encapsulamento e conversão simples para JSON:

`src/models/estado_model.py`

```python
class Estado:
    def __init__(self, id: int = None, estado: str = "", uf: str = ""):
        self.id = id
        self.estado = estado
        self.uf = uf

    def to_dict(self):
        return {
            "id": self.id,
            "estado": self.estado,
            "uf": self.uf
        }

    @staticmethod
    def from_dict(data: dict):
        return Estado(
            id=data.get("id"),
            estado=data.get("estado"),
            uf=data.get("uf")
        )

```

---

### 3. Repositório (Repository Pattern)

O **Repository Pattern** isola completamente o código SQL das rotas da API. Se você trocar o driver de banco ou alterar o SQL no futuro, a API continuará intacta.

`src/repositories/estado_repository.py`

```python
from src.database.connection import Database
from src.models.estado_model import Estado
from typing import List, Optional

class EstadoRepository:
    def __init__(self):
        self.db = Database()

    def get_all(self) -> List[Estado]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, estado, uf FROM estados")
            rows = cursor.fetchall()
            cursor.close()
            return [Estado.from_dict(row) for row in rows]

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, estado, uf FROM estados WHERE id = %s", (id_estado,))
            row = cursor.fetchone()
            cursor.close()
            return Estado.from_dict(row) if row else None

    def create(self, estado: Estado) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO estados (estado, uf) VALUES (%s, %s)"
            cursor.execute(query, (estado.estado, estado.uf))
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id

    def update(self, id_estado: int, estado: Estado) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "UPDATE estados SET estado = %s, uf = %s WHERE id = %s"
            cursor.execute(query, (estado.estado, estado.uf, id_estado))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0

    def delete(self, id_estado: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estados WHERE id = %s", (id_estado,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0

```

---

### 4. Controller orientado a rotas com Class-Based Views

O Flask possui a classe `MethodView` perfeita para vincular verbos HTTP (`GET`, `POST`, `PUT`, `DELETE`) diretamente a métodos da classe:

`src/controllers/estado_controller.py`

```python
from flask import request, jsonify
from flask.views import MethodView
from src.repositories.estado_repository import EstadoRepository
from src.models.estado_model import Estado

class EstadoAPI(MethodView):
    def __init__(self):
        self.repository = EstadoRepository()

    def get(self, id=None):
        if id is None:
            estados = self.repository.get_all()
            return jsonify([e.to_dict() for e in estados]), 200
        
        estado = self.repository.get_by_id(id)
        if not estado:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify(estado.to_dict()), 200

    def post(self):
        data = request.get_json()
        if not data or 'estado' not in data or 'uf' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        novo_estado = Estado.from_dict(data)
        novo_id = self.repository.create(novo_estado)
        novo_estado.id = novo_id
        return jsonify(novo_estado.to_dict()), 201

    def put(self, id):
        data = request.get_json()
        estado = Estado.from_dict(data)
        updated = self.repository.update(id, estado)
        if not updated:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro atualizado com sucesso"}), 200

    def delete(self, id):
        deleted = self.repository.delete(id)
        if not deleted:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify({"message": "Registro removido com sucesso"}), 200

```

---

### 5. Registro na classe principal `Api`

Para integrar o `MethodView` ao Flask, registra-se as rotas mapeadas na classe da API:

`src/api.py`

```python
from flask import Flask
from src.utils.config import Config
from src.controllers.estado_controller import EstadoAPI

class Api:
    def __init__(self):
        self.cfg = Config()
        self.app = Flask(self.cfg.APP_NAME)
        self._register_routes()

    def _register_routes(self):
        # Mapeamento do Class-Based View
        estado_view = EstadoAPI.as_view('estado_api')
        
        # Rota para coleção (GET all, POST)
        self.app.add_url_rule(
            '/api/estados', 
            view_func=estado_view, 
            methods=['GET', 'POST']
        )
        
        # Rota para item específico (GET id, PUT, DELETE)
        self.app.add_url_rule(
            '/api/estados/<int:id>', 
            view_func=estado_view, 
            methods=['GET', 'PUT', 'DELETE']
        )

    def run(self):
        self.app.run(
            host='0.0.0.0', 
            port=self.cfg.APP_PORT, 
            debug=self.cfg.APP_DEBUG
        )

```

---

### Principais Ganhos com essa Estrutura

* **Conexões Eficientes:** O uso de *context managers* (`with db.get_connection()`) garante a devolução automática da conexão ao Pool ao final de cada requisição.
* **Inversão e Separação de Controle:** Cada classe possui uma única responsabilidade (SRP - *Single Responsibility Principle*).
* **Consistência nos Retornos:** Tratamento explícito dos status HTTP adequados (`200 OK`, `201 Created`, `404 Not Found`, `400 Bad Request`).
* **Testabilidade:** Fica mais simples aplicar testes unitários com *mocks* injetando um repositório fictício no controller.

---
Banco de dados

database3:

```sql
CREATE DATABASE apitest;

CREATE TABLE estados (
	id int not null AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(60) NULL,
    uf VARCHAR(2) NULL
);
```