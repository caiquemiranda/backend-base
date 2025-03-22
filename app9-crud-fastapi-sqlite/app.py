# CRUD com FastAPI e SQLite
# Este arquivo contém orientações detalhadas para implementar operações
# CRUD (Create, Read, Update, Delete) com FastAPI e SQLite.

# 1. Configuração e Dependências
# Para criar uma aplicação CRUD com FastAPI e SQLite, precisamos das seguintes dependências:
# - fastapi: O framework web base
# - uvicorn: Servidor ASGI para executar a aplicação
# - sqlalchemy: ORM para interação com o banco de dados
# - pydantic: Para validação de dados e serialização
# - sqlite3: Biblioteca integrada ao Python para SQLite (não requer instalação adicional)
#
# Instalação:
# pip install fastapi uvicorn sqlalchemy pydantic

# 2. Estrutura Básica do Projeto
# Uma boa estrutura para um projeto CRUD com FastAPI:
#
# app/
# ├── __init__.py
# ├── main.py              # Ponto de entrada da aplicação
# ├── database.py          # Configuração da conexão com o banco de dados
# ├── models/              # Modelos SQLAlchemy (definições das tabelas)
# │   ├── __init__.py
# │   └── item.py
# ├── schemas/             # Schemas Pydantic para validação de dados
# │   ├── __init__.py
# │   └── item.py
# ├── crud/                # Funções para operações CRUD
# │   ├── __init__.py
# │   └── item.py
# ├── api/                 # Rotas da API
# │   ├── __init__.py
# │   ├── api.py           # Configuração do router principal
# │   └── endpoints/       # Endpoints para cada recurso
# │       ├── __init__.py
# │       └── items.py
# └── tests/               # Testes da aplicação
#     ├── __init__.py
#     └── test_api.py

# 3. Configuração do Banco de Dados (database.py)
# Precisamos configurar a conexão com o SQLite usando SQLAlchemy:

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados SQLite
# O arquivo será criado automaticamente se não existir
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Cria o engine SQLAlchemy, configurado para SQLite
# connect_args={"check_same_thread": False} é necessário apenas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma sessão local para cada operação no banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que será herdada por todos os modelos
Base = declarative_base()

# Função que fornece uma sessão para cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

# 4. Modelos SQLAlchemy (models/item.py)
# Modelos definem a estrutura das tabelas no banco de dados:

"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from ..database import Base

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
"""

# 5. Schemas Pydantic (schemas/item.py)
# Schemas Pydantic são usados para validação de dados e serialização:

"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema base com atributos comuns
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema para criação de item - com campos requeridos
class ItemCreate(ItemBase):
    pass

# Schema para atualização de item - todos os campos são opcionais
class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema para resposta - inclui todos os campos retornados pela API
class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Configuração para converter o modelo SQLAlchemy para um dict
    class Config:
        orm_mode = True
"""

# 6. Operações CRUD (crud/item.py)
# Funções para manipular os dados no banco:

"""
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate

# Obter todos os itens
def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

# Obter um item específico pelo ID
def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

# Criar um novo item
def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Atualizar um item existente
def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        # Atualiza apenas os campos fornecidos
        update_data = item.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

# Excluir um item
def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
"""

# 7. Endpoints da API (api/endpoints/items.py)
# Rotas HTTP para as operações CRUD:

"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...crud import item as crud
from ...schemas.item import Item, ItemCreate, ItemUpdate
from ...database import get_db

router = APIRouter()

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    \"\"\"
    Recupera uma lista de itens.
    - **skip**: Quantidade de registros para pular (paginação)
    - **limit**: Limite de registros a retornar
    \"\"\"
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    \"\"\"
    Cria um novo item.
    - **item**: Dados do item a ser criado
    \"\"\"
    return crud.create_item(db=db, item=item)

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    \"\"\"
    Recupera um item específico pelo ID.
    - **item_id**: ID do item a ser recuperado
    \"\"\"
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    \"\"\"
    Atualiza um item existente.
    - **item_id**: ID do item a ser atualizado
    - **item**: Dados atualizados do item
    \"\"\"
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    \"\"\"
    Remove um item.
    - **item_id**: ID do item a ser removido
    \"\"\"
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
"""

# 8. Configuração das Rotas (api/api.py)
# Incluir todos os endpoints no router principal:

"""
from fastapi import APIRouter
from .endpoints import items

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
"""

# 9. Aplicação Principal (main.py)
# Ponto de entrada da aplicação:

"""
from fastapi import FastAPI
from .api.api import api_router
from .database import engine
from .models import item

# Cria as tabelas no banco de dados
item.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD Example",
    description="API de exemplo com operações CRUD usando FastAPI e SQLite",
    version="0.1.0",
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API CRUD com FastAPI e SQLite"}
"""

# 10. Executando a Aplicação
# Para rodar a aplicação, utilize o Uvicorn:
# uvicorn app.main:app --reload
# Isso inicia o servidor em http://localhost:8000

# 11. Documentação Automática
# FastAPI gera automaticamente documentação interativa:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc

# 12. Testes da API
# Para testar a API, podemos usar pytest:

"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base, get_db
from ..main import app

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    # Cria as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    yield  # Testes são executados aqui
    # Limpa o banco após os testes
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    # Sobrescreve a dependência para usar o banco de teste
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}

def test_create_item(client):
    response = client.post("/items/", json={"title": "Test Item", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert "id" in data
"""

# 13. Segurança (Opcional)
# Para adicionar autenticação, podemos usar:
# - OAuth2 com JWT
# - API Keys
# - HTTPBasic
# - HTTPBearer

"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuração para autenticação JWT
SECRET_KEY = "seu_segredo_super_seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Aqui você buscaria o usuário no banco de dados
    # user = get_user(username)
    # if user is None:
    #     raise credentials_exception
    # return user
"""

# 14. Validação Avançada com Pydantic
# Podemos adicionar validações mais complexas aos schemas:

"""
from pydantic import BaseModel, Field, validator
from typing import Optional

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('title')
    def title_must_not_contain_special_chars(cls, v):
        if '@' in v or '#' in v:
            raise ValueError('o título não pode conter caracteres especiais')
        return v
"""

# 15. Gerenciamento de Erros Personalizados
# Podemos criar manipuladores de exceções para padronizar as respostas de erro:

"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item com id {item_id} não encontrado"
        super().__init__(self.message)

@app.exception_handler(ItemNotFoundError)
async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )
"""

# 16. Migrações de Banco de Dados (Opcional)
# Para gerenciar alterações no schema do banco de dados, podemos usar Alembic:

"""
# Instalação: pip install alembic
# Inicialização: alembic init alembic

# Em alembic/env.py, configure a URL do banco de dados:
from app.database import SQLALCHEMY_DATABASE_URL
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# Criar uma migração:
# alembic revision --autogenerate -m "create items table"

# Aplicar a migração:
# alembic upgrade head
"""

# 17. Conclusão
# Neste arquivo, vimos como implementar um CRUD completo com FastAPI e SQLite:
# - Configuração da estrutura do projeto
# - Definição de modelos SQLAlchemy para o banco de dados
# - Validação de dados com Pydantic
# - Implementação de operações CRUD
# - Criação de endpoints RESTful
# - Documentação automática
# - Testes
# - Recursos avançados e segurança
#
# Esta estrutura pode ser facilmente adaptada para aplicações maiores ou
# para usar outros bancos de dados (PostgreSQL, MySQL, etc.). 