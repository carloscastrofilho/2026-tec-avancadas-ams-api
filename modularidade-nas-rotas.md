Organizar a aplicação com **um Blueprint por entidade/módulo** traz modularidade, facilita a manutenção e evita arquivos de rotas gigantescos.

Para estruturar assim em POO, cada módulo pode ter seu próprio arquivo de rotas com uma classe ou função responsável por registrar a entidade e exportar seu Blueprint.

---

### Estrutura de Pastas Sugerida

```text
src/
├── modules/
│   ├── estado/
│   │   ├── estado_controller.py
│   │   ├── estado_model.py
│   │   ├── estado_repository.py
│   │   └── estado_routes.py    # Blueprint exclusivo do módulo Estado
│   └── user/
│       ├── user_controller.py
│       └── user_routes.py      # Blueprint exclusivo do módulo User
└── routes/
    └── router.py               # Registrará todos os Blueprints no App

```

---

### 1. Criando o Blueprint do Módulo (`estado_routes.py`)

Em vez de centralizar tudo, o próprio módulo gerencia seu mapeamento de URLs.

`src/modules/estado/estado_routes.py`

```python
from flask import Blueprint
from src.modules.estado.estado_controller import EstadoController

class EstadoRoutes:
    @staticmethod
    def get_blueprint() -> Blueprint:
        # Cria o blueprint exclusivo do módulo
        bp = Blueprint('estados', __name__, url_prefix='/estados')
        
        # Mapeia as views
        estado_view = EstadoController.as_view('estado_api')
        
        # Rotas da coleção
        bp.add_url_rule(
            '', 
            view_func=estado_view, 
            methods=['GET', 'POST']
        )
        
        # Rotas do item por ID
        bp.add_url_rule(
            '/<int:id>', 
            view_func=estado_view, 
            methods=['GET', 'PUT', 'DELETE']
        )
        
        return bp

```

---

### 2. Centralizador de Rotas (`router.py`)

A classe `Router` passa a ter uma responsabilidade simples: agrupar os Blueprints sob um prefixo comum (ex: `/api/v1`) e registrá-los na aplicação Flask.

`src/routes/router.py`

```python
from flask import Flask, Blueprint
from src.modules.estado.estado_routes import EstadoRoutes
# Importe os outros módulos conforme for criando:
# from src.modules.user.user_routes import UserRoutes

class Router:
    def __init__(self, app: Flask):
        self.app = app

    def register(self):
        # Blueprint pai para versionamento da API
        api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

        # Registra os Blueprints dos módulos dentro do Blueprint v1
        api_v1.register_blueprint(EstadoRoutes.get_blueprint())
        # api_v1.register_blueprint(UserRoutes.get_blueprint())

        # Registra o pacote v1 na aplicação Flask principal
        self.app.register_blueprint(api_v1)

```

---

### Resultado das URLs Geradas

Com o encadeamento de prefixos (`/api/v1` + `/estados`), as rotas ficam estruturadas da seguinte forma:

* **GET / POST:** `/api/v1/estados`
* **GET / PUT / DELETE:** `/api/v1/estados/<id>`

---

### Vantagens do Modelo Modular

* **Independência:** Mudar uma rota de `User` não impacta em nada o arquivo de `Estado`.
* **Encapsulamento:** Tudo que diz respeito a *Estado* (Controller, Model, Repository e Routes) fica dentro da mesma pasta do módulo.
* **Escalabilidade:** Para adicionar um novo módulo (ex: `cidades`), basta criar a pasta do módulo com seu `cidades_routes.py` e incluir uma linha no `Router`.