# Tutorial: Implementando um CRUD com FastAPI e SQLite

Neste tutorial, vamos construir uma API REST completa com operações CRUD (Create, Read, Update, Delete) usando FastAPI e SQLite como banco de dados. Implementaremos uma aplicação de lista de tarefas, um exemplo perfeito para entender os conceitos CRUD.

## Pré-requisitos

Para seguir este tutorial, você precisa ter:

- Python 3.6+ instalado
- Conhecimento básico de Python
- Familiaridade com conceitos REST
- Conhecimento básico de SQL (útil, mas não obrigatório)

## Parte 1: Configuração do Ambiente

### Passo 1: Criar a Estrutura do Projeto

Primeiro, vamos criar um diretório para nosso projeto e configurar o ambiente virtual:

```bash
# Criar o diretório do projeto
mkdir fastapi-sqlite-crud
cd fastapi-sqlite-crud

# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate
```

### Passo 2: Instalar as Dependências

Agora, vamos instalar as bibliotecas necessárias:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

- **FastAPI**: Framework web para construção de APIs
- **Uvicorn**: Servidor ASGI para executar a aplicação
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interagir com o banco de dados
- **Pydantic**: Biblioteca para validação de dados e serialização

### Passo 3: Criar a Estrutura de Diretórios

Vamos criar a estrutura de diretórios para nosso projeto:

```bash
mkdir -p app/api/endpoints app/crud app/models app/schemas
touch app/__init__.py app/api/__init__.py app/api/endpoints/__init__.py
touch app/crud/__init__.py app/models/__init__.py app/schemas/__init__.py
touch app/database.py app/main.py
```

A estrutura final deve ser assim:

```
fastapi-sqlite-crud/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── database.py
│   └── main.py
├── venv/
└── .env
```

## Parte 2: Configuração do Banco de Dados

### Passo 4: Configurar a Conexão com o SQLite

Vamos configurar a conexão com o banco de dados SQLite. Edite o arquivo `app/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados SQLite
# Criará um arquivo chamado sql_app.db na raiz do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Criação do engine do SQLAlchemy
# O argumento connect_args é específico para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criar uma sessão local para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para criar modelos SQLAlchemy
Base = declarative_base()

# Função de dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Passo 5: Criar o Modelo da Tarefa

Agora, vamos definir o modelo SQLAlchemy para nossas tarefas. Edite o arquivo `app/models/task.py`:

```python
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from ..database import Base

class Task(Base):
    """Modelo SQLAlchemy para a tabela de tarefas"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

Atualize o arquivo `app/models/__init__.py` para expor o modelo:

```python
from .task import Task
```

## Parte 3: Schemas Pydantic

### Passo 6: Criar Schemas para Validação

Os schemas Pydantic serão usados para validação de dados e serialização. Edite o arquivo `app/schemas/task.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    """Schema base para atributos comuns da tarefa"""
    title: str = Field(..., min_length=1, max_length=100, title="Título da tarefa")
    description: Optional[str] = Field(None, max_length=1000, title="Descrição da tarefa")
    completed: bool = Field(False, title="Status de conclusão")

class TaskCreate(TaskBase):
    """Schema para criação de tarefa - apenas com campos necessários"""
    pass

class TaskUpdate(BaseModel):
    """Schema para atualização de tarefa - todos os campos são opcionais"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class Task(TaskBase):
    """Schema para resposta - inclui campos gerados pelo banco"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Configuração para trabalhar com ORM"""
        orm_mode = True
```

Atualize o arquivo `app/schemas/__init__.py` para expor os schemas:

```python
from .task import Task, TaskCreate, TaskUpdate
```

## Parte 4: Operações CRUD

### Passo 7: Implementar Funções CRUD

Agora vamos criar as funções para realizar operações CRUD no banco de dados. Edite o arquivo `app/crud/task.py`:

```python
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """Retorna uma lista de tarefas"""
    return db.query(Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Retorna uma tarefa pelo ID"""
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate) -> Task:
    """Cria uma nova tarefa"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
    """Atualiza uma tarefa existente"""
    db_task = get_task(db, task_id)
    if db_task:
        # Atualiza apenas os campos fornecidos
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    """Remove uma tarefa"""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
```

Atualize o arquivo `app/crud/__init__.py`:

```python
from .task import get_tasks, get_task, create_task, update_task, delete_task
```

## Parte 5: Endpoints da API

### Passo 8: Implementar Rotas da API

Vamos criar os endpoints da API para cada operação CRUD. Edite o arquivo `app/api/endpoints/tasks.py`:

```python
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...crud import get_tasks, get_task, create_task, update_task, delete_task
from ...schemas import Task, TaskCreate, TaskUpdate
from ...database import get_db

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Recupera todas as tarefas.
    
    - **skip**: Quantidade de registros para pular (paginação)
    - **limit**: Limite de registros a retornar
    """
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Cria uma nova tarefa.
    
    - **task**: Dados da tarefa a ser criada
    """
    return create_task(db=db, task=task)

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Recupera uma tarefa específica pelo ID.
    
    - **task_id**: ID da tarefa a ser recuperada
    """
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_task

@router.put("/{task_id}", response_model=Task)
def update_task_endpoint(
    task_id: int, 
    task_in: TaskUpdate, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Atualiza uma tarefa existente.
    
    - **task_id**: ID da tarefa a ser atualizada
    - **task_in**: Dados atualizados da tarefa
    """
    db_task = update_task(db, task_id=task_id, task=task_in)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int, 
    db: Session = Depends(get_db)
) -> None:
    """
    Remove uma tarefa.
    
    - **task_id**: ID da tarefa a ser removida
    """
    success = delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return None
```

### Passo 9: Configurar o Router da API

Crie um arquivo `app/api/api.py` para configurar o router principal:

```python
from fastapi import APIRouter
from .endpoints import tasks

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
```

## Parte 6: Configuração da Aplicação Principal

### Passo 10: Criar o Arquivo Principal

Finalmente, vamos criar o ponto de entrada da aplicação. Edite o arquivo `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api import api_router
from .database import engine
from .models import task

# Cria as tabelas no banco de dados
task.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskAPI",
    description="API para gerenciamento de tarefas com FastAPI e SQLite",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(api_router)

@app.get("/")
def read_root():
    """Endpoint raiz da aplicação"""
    return {
        "message": "Bem-vindo à API de Tarefas!",
        "docs": "/docs",
        "endpoints": {
            "tasks": "/tasks"
        }
    }
```

## Parte 7: Executar e Testar a Aplicação

### Passo 11: Iniciar o Servidor

Agora que temos todos os componentes prontos, vamos iniciar o servidor:

```bash
uvicorn app.main:app --reload
```

Isso iniciará o servidor em `http://localhost:8000`.

### Passo 12: Explorar a Documentação Automática

FastAPI gera automaticamente documentação interativa. Acesse:

- `http://localhost:8000/docs` - Interface Swagger UI
- `http://localhost:8000/redoc` - Interface ReDoc

### Passo 13: Testar a API

Vamos testar as operações CRUD usando o Swagger UI ou com ferramentas como `curl` ou Postman:

**1. Criar uma nova tarefa (Create)**

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Aprender FastAPI",
  "description": "Completar o tutorial de FastAPI com SQLite",
  "completed": false
}'
```

**2. Listar todas as tarefas (Read)**

```bash
curl -X 'GET' 'http://localhost:8000/tasks/'
```

**3. Obter uma tarefa específica (Read)**

```bash
curl -X 'GET' 'http://localhost:8000/tasks/1'
```

**4. Atualizar uma tarefa (Update)**

```bash
curl -X 'PUT' \
  'http://localhost:8000/tasks/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "completed": true
}'
```

**5. Excluir uma tarefa (Delete)**

```bash
curl -X 'DELETE' 'http://localhost:8000/tasks/1'
```

## Recursos Adicionais

### Melhorias Opcionais

1. **Implementar Autenticação e Autorização**

Você pode adicionar segurança à sua API implementando autenticação JWT:

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

2. **Adicionar Migrations com Alembic**

Para gerenciar alterações no esquema do banco de dados:

```bash
pip install alembic
alembic init alembic
```

3. **Adicionar Validação Personalizada**

Você pode adicionar validações personalizadas aos schemas Pydantic:

```python
from pydantic import validator

class TaskCreate(TaskBase):
    @validator('title')
    def title_must_not_contain_special_chars(cls, v):
        if '@' in v or '#' in v:
            raise ValueError('O título não pode conter caracteres especiais')
        return v
```

4. **Implementar Paginação Avançada**

```python
from fastapi import Query

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    tasks = get_tasks(db, skip, limit)
    return tasks
```

5. **Adicionar Campos de Busca**

```python
@router.get("/search/", response_model=List[Task])
def search_tasks(
    db: Session = Depends(get_db),
    query: str = Query(None, min_length=1),
    completed: Optional[bool] = None
):
    query_obj = db.query(Task)
    
    if query:
        query_obj = query_obj.filter(Task.title.contains(query) | Task.description.contains(query))
    
    if completed is not None:
        query_obj = query_obj.filter(Task.completed == completed)
    
    return query_obj.all()
```

## Conclusão

Parabéns! Você implementou com sucesso uma API RESTful completa com operações CRUD usando FastAPI e SQLite. Este projeto serve como base para aplicações mais complexas.

Neste tutorial, você aprendeu:

1. Como configurar um projeto FastAPI com SQLAlchemy e SQLite
2. Como criar modelos de banco de dados usando SQLAlchemy
3. Como implementar schemas de validação com Pydantic
4. Como criar operações CRUD básicas
5. Como estruturar uma aplicação FastAPI em módulos
6. Como documentar sua API automaticamente

O código desenvolvido neste tutorial segue boas práticas e é um bom ponto de partida para aplicações mais complexas. Sinta-se à vontade para expandir esta base com novas funcionalidades e aprimoramentos.

Feliz codificação! 