# Tutorial: Introdução ao FastAPI - Hello World e Rotas

Este tutorial irá guiá-lo através dos conceitos básicos do FastAPI, um framework moderno e de alto desempenho para construção de APIs com Python. Aprenderemos desde a instalação até a criação de diferentes tipos de rotas.

## O que é FastAPI?

FastAPI é um framework web para criação de APIs com Python, baseado em standards modernos como:

- **OpenAPI** para criação de APIs
- **JSON Schema** para validação de dados
- **OAuth 2.0** para autenticação
- **Pydantic** para validação de dados

O FastAPI se destaca por ser extremamente rápido (comparável ao NodeJS e Go), ter tipagem forte, validação automática de dados e gerar documentação interativa sem esforço adicional.

## Pré-requisitos

Para seguir este tutorial, você precisará de:

- Python 3.6+ instalado
- Conhecimento básico de Python
- Familiaridade com conceitos de APIs RESTful é útil, mas não obrigatório

## Passo 1: Configuração do Ambiente

Primeiro, crie um ambiente virtual para o projeto:

```bash
# Crie o diretório do projeto (se ainda não existir)
mkdir fastapi-hello-world
cd fastapi-hello-world

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

Agora, instale o FastAPI e o Uvicorn (um servidor ASGI de alto desempenho):

```bash
pip install fastapi uvicorn
```

## Passo 2: Criando sua Primeira Aplicação FastAPI

Vamos criar um arquivo chamado `main.py` com uma aplicação Hello World básica:

```python
from fastapi import FastAPI

# Cria uma instância do aplicativo FastAPI
app = FastAPI()

# Define uma rota para o caminho raiz ('/')
@app.get("/")
def read_root():
    return {"Hello": "World"}
```

Este código simples:
1. Importa o FastAPI
2. Cria uma instância da aplicação
3. Define uma função que será executada quando alguém acessar a rota raiz com um método GET
4. Retorna um objeto JSON `{"Hello": "World"}`

## Passo 3: Executando a Aplicação

Para executar a aplicação, use o servidor Uvicorn:

```bash
uvicorn main:app --reload
```

Aqui:
- `main` é o nome do arquivo Python (main.py)
- `app` é o objeto criado dentro do arquivo
- `--reload` permite que o servidor reinicie automaticamente quando você altera o código

Você deverá ver uma saída como esta:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Abra seu navegador e acesse `http://127.0.0.1:8000`. Você verá a resposta JSON `{"Hello": "World"}`.

## Passo 4: Documentação Automática

Uma das características mais poderosas do FastAPI é a documentação automática. Acesse:

- `http://127.0.0.1:8000/docs` para ver a interface Swagger UI
- `http://127.0.0.1:8000/redoc` para ver a interface ReDoc

Estes endpoints são gerados automaticamente e proporcionam documentação interativa para sua API. À medida que adicionamos mais rotas e recursos, a documentação será atualizada automaticamente.

## Passo 5: Adicionando Parâmetros de Caminho (Path Parameters)

Vamos expandir nossa aplicação para entender como trabalhar com parâmetros de caminho. Adicione o seguinte código ao `main.py`:

```python
# Rota com um parâmetro de caminho
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

Reinicie o servidor (ou ele reiniciará automaticamente se você usou `--reload`) e acesse `http://127.0.0.1:8000/items/5`. Você verá a resposta JSON `{"item_id": 5}`.

Observe como usamos a anotação de tipo `int` para o parâmetro `item_id`. Isso faz com que o FastAPI:

1. Converta o parâmetro para inteiro (se possível)
2. Valide que é realmente um inteiro
3. Documente o tipo na documentação OpenAPI
4. Forneça autocomplete em editores de código

Se você tentar acessar `http://127.0.0.1:8000/items/abc`, receberá um erro de validação, pois "abc" não pode ser convertido para um inteiro.

## Passo 6: Parâmetros de Consulta (Query Parameters)

Além dos parâmetros de caminho, as APIs frequentemente usam parâmetros de consulta. Vamos adicionar uma rota que os utiliza:

```python
@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10):
    # Em uma aplicação real, aqui você buscaria dados no banco de dados
    fake_products = [{"id": i, "name": f"Product {i}"} for i in range(skip, skip + limit)]
    return fake_products
```

Agora você pode acessar:
- `http://127.0.0.1:8000/products/` para obter os primeiros 10 produtos
- `http://127.0.0.1:8000/products/?skip=20` para pular os primeiros 20
- `http://127.0.0.1:8000/products/?skip=20&limit=5` para obter 5 produtos começando do 20º

Os parâmetros de consulta são opcionais e têm valores padrão, ao contrário dos parâmetros de caminho.

## Passo 7: Combinando Parâmetros de Caminho e Consulta

Vamos criar uma rota que combine ambos os tipos de parâmetros:

```python
@app.get("/users/{user_id}/items/")
def read_user_items(user_id: int, skip: int = 0, limit: int = 10):
    # Aqui você normalmente buscaria itens do usuário no banco de dados
    fake_items = [
        {"item_id": i, "owner": user_id, "name": f"Item {i}"} 
        for i in range(skip, skip + limit)
    ]
    return fake_items
```

Esta rota permite buscar os itens de um usuário específico, com paginação. Por exemplo:
- `http://127.0.0.1:8000/users/123/items/?skip=10&limit=5`

## Passo 8: Trabalhando com Dados do Corpo da Requisição (Request Body)

Para métodos como POST e PUT, normalmente precisamos enviar dados no corpo da requisição. O FastAPI usa o Pydantic para validar esses dados:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define o modelo Pydantic para validação de dados
class Item(BaseModel):
    name: str
    description: str = None  # Campo opcional
    price: float
    tax: float = None  # Campo opcional

# Rota que aceita um corpo de requisição
@app.post("/items/")
def create_item(item: Item):
    # Cria um novo dicionário com os dados do item
    # e um campo calculado para o preço com imposto
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

Para testar esta rota, você precisará enviar uma requisição POST. Você pode usar o Swagger UI em `/docs` para fazer isso facilmente.

## Passo 9: Parâmetros Opcionais com Tipagem Moderna

Python 3.10+ suporta sintaxe de tipagem mais moderna. Vamos usar `Union` e `None` para parâmetros opcionais:

```python
from typing import Union

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

Em versões mais recentes do Python, você também pode usar a sintaxe `|`:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

## Passo 10: Tratamento de Erros

FastAPI permite lançar exceções HTTP para indicar erros:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def read_user(user_id: int):
    # Simula uma verificação de usuário
    if user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "name": f"User {user_id}"}
```

Se você acessar `/users/0`, receberá um erro 404 com a mensagem "User not found".

## Passo 11: Marcando a Resposta com Códigos de Status

Você pode especificar o código de status HTTP para uma resposta:

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    # Em uma aplicação real, você inseriria os dados no banco
    return {"name": name}
```

O endpoint `/items/` agora retornará um status 201 Created em vez do padrão 200 OK.

## Passo 12: Adicionando Metadados à Aplicação

Você pode adicionar metadados à sua aplicação, o que melhora a documentação:

```python
app = FastAPI(
    title="Minha API Incrível",
    description="Esta API faz coisas incríveis",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
```

## Passo 13: Organizando Código em Arquivos Separados

À medida que sua aplicação cresce, é bom organizá-la em arquivos separados. Vamos criar a seguinte estrutura:

```
myapp/
├── __init__.py
├── main.py
├── models.py
└── routers/
    ├── __init__.py
    ├── items.py
    └── users.py
```

Em `models.py`:
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
```

Em `routers/items.py`:
```python
from fastapi import APIRouter, HTTPException
from ..models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_items():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

@router.post("/")
def create_item(item: Item):
    return item
```

Em `main.py`:
```python
from fastapi import FastAPI
from .routers import items, users

app = FastAPI(title="My API")

app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Passo 14: Testando a Aplicação Completa

Vamos revisar a aplicação completa que exploramos neste tutorial:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Union

app = FastAPI(
    title="FastAPI Hello World",
    description="Uma API de introdução ao FastAPI",
    version="0.1.0",
)

# Modelo Pydantic para validação de dados
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

# Rota raiz
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Rota com parâmetro de caminho
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Rota com parâmetros de consulta
@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10):
    fake_products = [{"id": i, "name": f"Product {i}"} for i in range(skip, skip + limit)]
    return fake_products

# Rota combinando parâmetros de caminho e consulta
@app.get("/users/{user_id}/items/")
def read_user_items(user_id: int, skip: int = 0, limit: int = 10):
    fake_items = [
        {"item_id": i, "owner": user_id, "name": f"Item {i}"} 
        for i in range(skip, skip + limit)
    ]
    return fake_items

# Rota POST com corpo de requisição
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Rota com tratamento de erro
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "name": f"User {user_id}"}
```

Para executar esta aplicação:

```bash
uvicorn main:app --reload
```

## Conclusão

Neste tutorial, você aprendeu os conceitos básicos do FastAPI:

1. **Criação de uma aplicação FastAPI**
2. **Definição de rotas com diferentes métodos HTTP**
3. **Uso de parâmetros de caminho e consulta**
4. **Validação de dados com Pydantic**
5. **Tratamento de erros**
6. **Uso da documentação interativa**
7. **Organização de código para projetos maiores**

O FastAPI oferece muitos outros recursos avançados como:
- Autenticação e autorização
- WebSockets
- Dependências e injeção de dependências
- Background tasks
- E muito mais

A documentação oficial é excepcionalmente boa e vale a pena explorar para aprender mais sobre esses tópicos avançados.

## Próximos Passos

- Experimente criar uma API CRUD completa
- Integre com um banco de dados (SQLAlchemy, MongoDB, etc.)
- Implemente autenticação e autorização
- Deploy sua aplicação FastAPI em um servidor ou serviço de nuvem

Feliz codificação com FastAPI! 