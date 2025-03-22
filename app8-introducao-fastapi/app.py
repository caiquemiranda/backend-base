# Introdução ao FastAPI: Hello World e Rotas
# Este arquivo contém orientações detalhadas para iniciar com FastAPI,
# um framework moderno para desenvolvimento de APIs com Python.

# 1. O que é FastAPI?
# FastAPI é um framework web moderno e rápido para construção de APIs com Python 3.6+
# baseado em padrões abertos como:
# - OpenAPI (anteriormente conhecido como Swagger) para criação de APIs
# - JSON Schema para validação de dados
# - OAuth 2.0 para autenticação
# - Pydantic para validação de dados e serialização
# 
# Principais vantagens:
# - Altíssimo desempenho (um dos frameworks Python mais rápidos disponíveis)
# - Tipagem forte e validação automática de dados
# - Documentação interativa automática (Swagger UI e ReDoc)
# - Menor risco de erros devido à validação automática
# - Editor completion (devido às type hints)

# 2. Instalação do FastAPI
# Para começar, você precisa instalar o FastAPI e um servidor ASGI como o Uvicorn:
# pip install fastapi uvicorn
#
# O Uvicorn é um servidor ASGI de alto desempenho, necessário para executar aplicações FastAPI

# 3. Hello World com FastAPI
# O exemplo mais simples possível é:
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
# Este código:
# - Importa e cria uma instância do FastAPI
# - Define uma função que lida com requisições GET para o caminho "/"
# - Retorna um dicionário que será automaticamente convertido para JSON

# 4. Executando a aplicação
# Para executar a aplicação, você usa o Uvicorn:
# uvicorn app:app --reload
# 
# Onde:
# - O primeiro "app" refere-se ao nome do arquivo Python (app.py)
# - O segundo "app" refere-se ao objeto criado dentro do arquivo (app = FastAPI())
# - --reload permite que o servidor reinicie automaticamente quando há alterações no código

# 5. Documentação Automática
# Uma das melhores características do FastAPI é a documentação automática.
# Ao executar sua aplicação, você pode acessar:
# - /docs: Interface Swagger UI (http://localhost:8000/docs)
# - /redoc: Interface ReDoc alternativa (http://localhost:8000/redoc)
#
# Estas interfaces são geradas automaticamente e documentam todas as suas rotas,
# parâmetros, tipos de retorno e muito mais.

# 6. Criando Rotas Básicas
# O FastAPI usa decoradores para definir rotas, semelhante ao Flask:

"""
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
"""

# Decoradores para diferentes métodos HTTP:
# - @app.get() para requisições GET
# - @app.post() para requisições POST
# - @app.put() para requisições PUT
# - @app.delete() para requisições DELETE
# - etc.

# 7. Parâmetros de Caminho (Path Parameters)
# FastAPI permite definir parâmetros de caminho (path) com tipagem:

"""
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
"""

# A tipagem não apenas fornece validação automática, mas também:
# - Converte o parâmetro para o tipo correto (se possível)
# - Documenta o tipo na API
# - Fornece suporte a autocompletion em editores

# 8. Parâmetros de Consulta (Query Parameters)
# Parâmetros de consulta são aqueles que aparecem após o ? na URL:

"""
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
"""

# Ao acessar /items/?skip=20&limit=30, os parâmetros serão:
# - skip = 20
# - limit = 30

# 9. Combinando Parâmetros de Caminho e Consulta

"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
"""

# Acessando /items/5?q=teste, teremos:
# - item_id = 5 (parâmetro de caminho)
# - q = "teste" (parâmetro de consulta)

# 10. Corpo da Requisição (Request Body)
# Para métodos como POST, PUT, você geralmente precisa enviar dados no corpo da requisição.
# FastAPI usa o Pydantic para definir e validar os modelos de dados:

"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return item
"""

# O FastAPI vai:
# - Ler o corpo da requisição como JSON
# - Converter para o tipo apropriado
# - Validar os dados
# - Documentar com JSON Schema
# - Fornecer editores de completion

# 11. Parâmetros Opcionais
# Você pode definir parâmetros opcionais usando valores padrão ou tipagem Optional:

"""
from typing import Optional

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
"""

# 12. Múltiplos Parâmetros no Corpo
# Você pode ter múltiplos parâmetros do tipo Pydantic:

"""
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}
"""

# 13. Validação de Dados
# FastAPI e Pydantic oferecem várias formas de validação:

"""
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    is_offer: bool = False
"""

# Validações comuns incluem:
# - min_length/max_length para strings
# - gt (maior que), lt (menor que) para números
# - regex para padrões de string
# - E muitas outras

# 14. Respostas HTTP Personalizadas
# Você pode personalizar as respostas HTTP:

"""
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
"""

# 15. Headers e Cookies
# Você pode acessar e definir headers e cookies:

"""
from fastapi import FastAPI, Header, Cookie

@app.get("/items/")
def read_items(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/cookies/")
def read_cookies(ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}
"""

# 16. Rotas com Arquivos
# Você pode receber e enviar arquivos:

"""
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
"""

# 17. Agrupando Rotas
# Para aplicações maiores, você pode organizar rotas usando APIRouter:

"""
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/users/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

app.include_router(router, prefix="/api/v1")
"""

# 18. Middleware
# Middleware permite processar requisições antes que cheguem às rotas:

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

# 19. Dependências e Injeção de Dependências
# FastAPI tem um poderoso sistema de injeção de dependências:

"""
from fastapi import Depends, FastAPI

app = FastAPI()

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons
"""

# 20. Conclusão
# FastAPI é um framework poderoso, rápido e fácil de usar para construir APIs.
# Características como tipagem forte, validação automática e documentação
# interativa fazem dele uma excelente escolha para projetos modernos.
# 
# Para aprender mais, consulte a documentação oficial em: https://fastapi.tiangolo.com/ 