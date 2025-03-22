# Tutorial: API REST Estruturada com Flask e Blueprints

Este tutorial guiará você na criação de uma API REST bem estruturada usando Flask e o sistema de Blueprints para organizar o código em módulos.

## Pré-requisitos

Certifique-se de ter instalado:
- Python 3.x
- pip (gerenciador de pacotes Python)
- Conhecimentos básicos de HTTP e REST
- Familiaridade com Flask

## Passo 1: Configuração do Ambiente

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Instale as dependências necessárias:
   ```bash
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy python-dotenv
   ```

4. Crie um arquivo `.env` para variáveis de ambiente:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=sua_chave_secreta_aqui
   DATABASE_URI=sqlite:///app.db
   ```

## Passo 2: Estrutura de Diretórios

Crie a seguinte estrutura de diretórios:

```
app7-api-rest-flask-blueprints/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── products/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── error_handlers.py
│   └── schemas/
│       ├── __init__.py
│       └── user.py
├── run.py
├── .env
└── .gitignore
```

## Passo 3: Arquivo de Configuração

Crie o arquivo `app/config.py` para gerenciar configurações baseadas em ambiente:

```python
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

class Config:
    """Configurações base da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-secreta-padrao')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///dev.db')

class TestingConfig(Config):
    """Configurações para ambiente de teste"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    """Configurações para ambiente de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///prod.db')

# Dicionário para seleção de configuração baseada na variável FLASK_ENV
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Configuração padrão se nenhuma for especificada
default_config = config_by_name[os.environ.get('FLASK_ENV', 'development')]
```

## Passo 4: Inicialização da Aplicação

Crie o arquivo `app/__init__.py` para inicializar a aplicação usando o padrão Factory:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicialização das extensões
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_object=None):
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Carrega configurações
    from app.config import default_config
    app.config.from_object(config_object or default_config)
    
    # Inicializa extensões com a aplicação
    db.init_app(app)
    ma.init_app(app)
    
    # Registra blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Registra manipuladores de erro
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        """Rota para a raiz da aplicação"""
        return {
            'message': 'API REST com Flask e Blueprints',
            'status': 'online',
            'documentation': '/api/v1/docs'
        }
    
    return app
```

## Passo 5: Blueprints da API

Crie os blueprints para organizar a API:

1. Primeiro, crie o blueprint principal em `app/api/__init__.py`:

```python
from flask import Blueprint

# Blueprint principal da API
bp = Blueprint('api', __name__)

# Importa e registra blueprints específicos
from app.api.users import bp as users_bp
from app.api.products import bp as products_bp

bp.register_blueprint(users_bp, url_prefix='/users')
bp.register_blueprint(products_bp, url_prefix='/products')

# Rota para documentação da API
@bp.route('/docs')
def docs():
    """Endpoint para documentação da API"""
    return {
        'message': 'Documentação da API',
        'version': 'v1',
        'endpoints': [
            {'users': '/api/v1/users'},
            {'products': '/api/v1/products'}
        ]
    }
```

2. Crie o blueprint para usuários em `app/api/users/__init__.py`:

```python
from flask import Blueprint

bp = Blueprint('users', __name__)

from app.api.users import routes
```

3. Crie o blueprint para produtos em `app/api/products/__init__.py`:

```python
from flask import Blueprint

bp = Blueprint('products', __name__)

from app.api.products import routes
```

## Passo 6: Modelos de Dados

Crie os modelos para o banco de dados em `app/models/user.py`:

```python
from datetime import datetime
from app import db

class User(db.Model):
    """Modelo para usuários"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

Inicialize os modelos em `app/models/__init__.py`:

```python
from app.models.user import User
```

## Passo 7: Schemas para Serialização

Crie os schemas para serialização em `app/schemas/user.py`:

```python
from app import ma
from app.models.user import User
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemySchema):
    """Schema para serialização de usuários"""
    class Meta:
        model = User
    
    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True, validate=validate.Length(min=3, max=64))
    email = ma.auto_field(required=True, validate=validate.Email())
    is_active = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6))

# Inicializa schemas para uso em toda a aplicação
user_schema = UserSchema()
users_schema = UserSchema(many=True)
```

Inicialize os schemas em `app/schemas/__init__.py`:

```python
from app.schemas.user import user_schema, users_schema
```

## Passo 8: Rotas da API

Implemente as rotas para usuários em `app/api/users/routes.py`:

```python
from flask import request, jsonify
from app import db
from app.api.users import bp
from app.models.user import User
from app.schemas import user_schema, users_schema
from werkzeug.security import generate_password_hash

@bp.route('/', methods=['GET'])
def get_users():
    """Retorna lista de usuários"""
    users = User.query.all()
    return jsonify({
        'success': True,
        'data': users_schema.dump(users),
        'total': len(users)
    }), 200

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    """Retorna um usuário específico pelo ID"""
    user = User.query.get_or_404(id, description=f"Usuário com ID {id} não encontrado")
    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    }), 200

@bp.route('/', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    # Valida dados recebidos com o schema
    errors = user_schema.validate(request.json)
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    # Verifica se usuário já existe
    if User.query.filter_by(username=request.json['username']).first():
        return jsonify({
            'success': False,
            'message': 'Este nome de usuário já está em uso'
        }), 400
    
    if User.query.filter_by(email=request.json['email']).first():
        return jsonify({
            'success': False,
            'message': 'Este email já está em uso'
        }), 400
    
    # Cria novo usuário
    user = User(
        username=request.json['username'],
        email=request.json['email'],
        password_hash=generate_password_hash(request.json['password'])
    )
    
    # Salva no banco de dados
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Usuário criado com sucesso',
        'data': user_schema.dump(user)
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    """Atualiza um usuário existente"""
    user = User.query.get_or_404(id, description=f"Usuário com ID {id} não encontrado")
    
    data = request.json
    
    # Atualiza apenas os campos fornecidos
    if 'username' in data:
        # Verifica se o novo username já existe para outro usuário
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != id:
            return jsonify({
                'success': False,
                'message': 'Este nome de usuário já está em uso'
            }), 400
        user.username = data['username']
    
    if 'email' in data:
        # Verifica se o novo email já existe para outro usuário
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != id:
            return jsonify({
                'success': False,
                'message': 'Este email já está em uso'
            }), 400
        user.email = data['email']
    
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    
    # Salva as alterações
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Usuário atualizado com sucesso',
        'data': user_schema.dump(user)
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Exclui um usuário"""
    user = User.query.get_or_404(id, description=f"Usuário com ID {id} não encontrado")
    
    # Exclui o usuário
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Usuário com ID {id} excluído com sucesso'
    }), 200
```

Implemente as rotas para produtos em `app/api/products/routes.py`:

```python
from flask import jsonify
from app.api.products import bp

@bp.route('/', methods=['GET'])
def get_products():
    """Lista todos os produtos"""
    # Simulação de dados - em um caso real, consultaria o banco de dados
    products = [
        {'id': 1, 'name': 'Produto 1', 'price': 19.99},
        {'id': 2, 'name': 'Produto 2', 'price': 29.99},
        {'id': 3, 'name': 'Produto 3', 'price': 39.99}
    ]
    
    return jsonify({
        'success': True,
        'data': products,
        'total': len(products)
    }), 200

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    """Retorna um produto específico"""
    # Simulação - em um caso real, consultaria o banco de dados
    products = {
        1: {'id': 1, 'name': 'Produto 1', 'price': 19.99},
        2: {'id': 2, 'name': 'Produto 2', 'price': 29.99},
        3: {'id': 3, 'name': 'Produto 3', 'price': 39.99}
    }
    
    if id not in products:
        return jsonify({
            'success': False,
            'message': f'Produto com ID {id} não encontrado'
        }), 404
    
    return jsonify({
        'success': True,
        'data': products[id]
    }), 200
```

## Passo 9: Manipuladores de Erro

Crie os manipuladores de erro em `app/utils/error_handlers.py`:

```python
from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    """Registra manipuladores de erro para a aplicação"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Manipulador para erro 404"""
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': str(error) or 'O recurso solicitado não foi encontrado.'
        }), 404
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Manipulador para erro 400"""
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error) or 'Requisição inválida.'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Manipulador para erro 401"""
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': str(error) or 'Autenticação necessária.'
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Manipulador para erro 403"""
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': str(error) or 'Você não tem permissão para acessar este recurso.'
        }), 403
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Manipulador para erro 500"""
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'Ocorreu um erro interno no servidor.'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Manipulador genérico para exceções HTTP"""
        return jsonify({
            'success': False,
            'error': error.name,
            'message': error.description
        }), error.code
    
    @app.errorhandler(SQLAlchemyError)
    def handle_db_exception(error):
        """Manipulador para erros de banco de dados"""
        return jsonify({
            'success': False,
            'error': 'Database Error',
            'message': str(error)
        }), 500
```

## Passo 10: Script de Execução

Crie o arquivo `run.py` na raiz do projeto:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

## Passo 11: Arquivo .gitignore

Crie um arquivo `.gitignore` para evitar commits de arquivos desnecessários:

```
# Ambiente virtual
venv/
.env

# Arquivos Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
*.egg

# Banco de dados SQLite
*.db
*.sqlite3

# Logs e arquivos temporários
*.log
*.tmp
.DS_Store

# Diretórios gerados
instance/
```

## Passo 12: Teste da API

Para testar sua API, execute o script principal:

```bash
python run.py
```

Acesse `http://localhost:5000/` para verificar se a API está funcionando.

Você pode testar os endpoints com ferramentas como:
- cURL
- Postman
- Insomnia
- Extensão REST Client para VS Code

### Exemplos de requisições:

#### Listar todos os usuários:
```bash
curl -X GET http://localhost:5000/api/v1/users/
```

#### Obter um usuário específico:
```bash
curl -X GET http://localhost:5000/api/v1/users/1
```

#### Criar um novo usuário:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "novousuario", "email": "usuario@exemplo.com", "password": "senha123"}'
```

#### Atualizar um usuário:
```bash
curl -X PUT http://localhost:5000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username": "usuarioatualizado"}'
```

#### Excluir um usuário:
```bash
curl -X DELETE http://localhost:5000/api/v1/users/1
```

## Passo 13: Implementação de Autenticação (Opcional)

Para adicionar autenticação com JWT, primeiro instale as dependências:

```bash
pip install flask-jwt-extended
```

Atualize a inicialização da aplicação em `app/__init__.py`:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

# Inicialização das extensões
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_object=None):
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Carrega configurações
    from app.config import default_config
    app.config.from_object(config_object or default_config)
    
    # Inicializa extensões com a aplicação
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
    # Registra blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Registra manipuladores de erro
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        """Rota para a raiz da aplicação"""
        return {
            'message': 'API REST com Flask e Blueprints',
            'status': 'online',
            'documentation': '/api/v1/docs'
        }
    
    return app
```

Crie um módulo para autenticação em `app/api/auth/__init__.py`:

```python
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.api.auth import routes
```

E implemente as rotas em `app/api/auth/routes.py`:

```python
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.api.auth import bp
from werkzeug.security import check_password_hash
from datetime import timedelta

@bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticação de usuários"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Requisição deve ser JSON"}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"success": False, "message": "Usuário e senha são obrigatórios"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Credenciais inválidas"}), 401
    
    # Cria token JWT de acesso
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        "success": True,
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    """Retorna informações do usuário autenticado"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404
    
    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200
```

Registre o blueprint no arquivo `app/api/__init__.py`:

```python
from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api.users import bp as users_bp
from app.api.products import bp as products_bp
from app.api.auth import bp as auth_bp

bp.register_blueprint(users_bp, url_prefix='/users')
bp.register_blueprint(products_bp, url_prefix='/products')
bp.register_blueprint(auth_bp, url_prefix='/auth')
```

Para proteger rotas com autenticação, adicione o decorador `@jwt_required()`:

```python
from flask_jwt_extended import jwt_required

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    # Implementação da função...
```

## Passo 14: Paginação, Filtros e Ordenação

Para implementar paginação, modifique o método `get_users()` em `app/api/users/routes.py`:

```python
@bp.route('/', methods=['GET'])
def get_users():
    """Retorna lista de usuários com paginação, filtros e ordenação"""
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limite o número máximo de itens por página
    per_page = min(per_page, 100)
    
    # Filtros
    username_filter = request.args.get('username', '')
    
    # Ordenação
    sort_by = request.args.get('sort_by', 'id')
    sort_dir = request.args.get('sort_dir', 'asc')
    
    # Construir query
    query = User.query
    
    # Aplicar filtros
    if username_filter:
        query = query.filter(User.username.ilike(f'%{username_filter}%'))
    
    # Aplicar ordenação
    if sort_dir == 'asc':
        query = query.order_by(getattr(User, sort_by))
    else:
        query = query.order_by(getattr(User, sort_by).desc())
    
    # Executar consulta paginada
    paginated_users = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': users_schema.dump(paginated_users.items),
        'pagination': {
            'total_items': paginated_users.total,
            'total_pages': paginated_users.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': paginated_users.has_next,
            'has_prev': paginated_users.has_prev,
            'next_page': paginated_users.next_num,
            'prev_page': paginated_users.prev_num
        }
    }), 200
```

## Passo 15: Documentação com Swagger/OpenAPI (Opcional)

Para adicionar documentação interativa, instale a extensão:

```bash
pip install flask-swagger-ui
```

Crie um arquivo `app/static/swagger.json` para definir a especificação OpenAPI:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "API REST Flask e Blueprints",
    "description": "Documentação da API REST com Flask e Blueprints",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "/api/v1",
      "description": "Servidor principal"
    }
  ],
  "paths": {
    "/users": {
      "get": {
        "summary": "Lista todos os usuários",
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "description": "Número da página",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 1
            }
          },
          {
            "name": "per_page",
            "in": "query",
            "description": "Itens por página",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 10
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Lista de usuários retornada com sucesso"
          }
        }
      },
      "post": {
        "summary": "Cria um novo usuário",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "type": "string"
                  },
                  "email": {
                    "type": "string"
                  },
                  "password": {
                    "type": "string"
                  }
                },
                "required": ["username", "email", "password"]
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Usuário criado com sucesso"
          },
          "400": {
            "description": "Dados inválidos"
          }
        }
      }
    }
  }
}
```

Atualize `app/__init__.py` para incluir o Swagger UI:

```python
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_object=None):
    # Código existente...
    
    # Configura Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API REST Flask e Blueprints"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Resto do código...
```

## Conclusão

Você criou uma API REST bem estruturada com Flask e Blueprints! Esta arquitetura é escalável e fácil de manter, ideal para aplicações de médio a grande porte.

Principais aspectos implementados:
- Estrutura organizada com padrões de projeto reconhecidos
- Sistema de blueprints para modularização
- Serialização e validação de dados
- Manipulação de erros padronizada
- Técnicas de autenticação (opcional)
- Paginação, filtros e ordenação (opcional)
- Documentação interativa (opcional)

Próximos passos possíveis:
- Adicionar testes automatizados
- Implementar cache para melhorar performance
- Integrar com sistemas de CI/CD
- Expandir a documentação
- Adicionar autorizações baseadas em papéis

---

Este tutorial forneceu uma base sólida para criar APIs REST com Flask. Você pode estender estas técnicas para desenvolver aplicações mais complexas conforme necessário. 