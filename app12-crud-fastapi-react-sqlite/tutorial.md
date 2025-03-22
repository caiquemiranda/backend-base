# Tutorial: CRUD Completo com FastAPI, React e SQLite

Este tutorial guiará você na criação de uma aplicação CRUD (Create, Read, Update, Delete) completa utilizando FastAPI no backend, React no frontend e SQLite como banco de dados.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Implementação do Backend](#implementação-do-backend)
   - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
   - [Modelos SQLAlchemy](#modelos-sqlalchemy)
   - [Esquemas Pydantic](#esquemas-pydantic)
   - [Operações CRUD](#operações-crud)
   - [API FastAPI](#api-fastapi)
4. [Implementação do Frontend](#implementação-do-frontend)
   - [Configuração do Projeto React](#configuração-do-projeto-react)
   - [Serviço de API](#serviço-de-api)
   - [Componentes React](#componentes-react)
   - [Páginas da Aplicação](#páginas-da-aplicação)
   - [Roteamento](#roteamento)
5. [Executando a Aplicação](#executando-a-aplicação)
6. [Próximos Passos](#próximos-passos)

## Pré-requisitos

- Python 3.7+
- Node.js e npm
- Editor de código (VS Code, PyCharm, etc.)
- Conhecimentos básicos de Python, React, SQL e REST APIs

## Configuração do Ambiente

Vamos começar criando a estrutura do projeto:

```bash
# Criar o diretório principal do projeto
mkdir -p app12-crud-fastapi-react-sqlite/{backend,frontend}
cd app12-crud-fastapi-react-sqlite
```

### Backend

```bash
cd backend

# Criar ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install fastapi uvicorn sqlalchemy pydantic python-multipart

# Criar arquivo de requisitos
pip freeze > requirements.txt

# Criar estrutura de diretórios
mkdir -p app/{models,schemas,crud}
touch app/__init__.py app/database.py app/main.py
touch app/models/__init__.py app/schemas/__init__.py app/crud/__init__.py
```

### Frontend

```bash
# Voltar para a raiz do projeto
cd ..

# Inicializar um projeto React
npx create-react-app frontend

# Entrar no diretório frontend e instalar dependências
cd frontend
npm install axios react-router-dom react-hook-form @material-ui/core @material-ui/icons @material-ui/lab

# Criar estrutura de diretórios
mkdir -p src/{components,pages,services}
```

## Implementação do Backend

### Configuração do Banco de Dados

Crie o arquivo `backend/app/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# Criar engine do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criar uma sessão local para interação com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos declarativos
Base = declarative_base()

# Função auxiliar para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Modelos SQLAlchemy

Crie o arquivo `backend/app/models/item.py`:

```python
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

Atualize o arquivo `backend/app/models/__init__.py`:

```python
from .item import Item
from ..database import Base
```

### Esquemas Pydantic

Crie o arquivo `backend/app/schemas/item.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Esquema base para Item
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Comprar leite")
    description: Optional[str] = Field(None, example="Comprar 2 litros de leite desnatado")
    priority: int = Field(1, ge=1, le=5, example=3)
    completed: bool = Field(False, example=False)

# Esquema para criação de Item
class ItemCreate(ItemBase):
    pass

# Esquema para atualização de Item
class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    completed: Optional[bool] = None

# Esquema para resposta completa do Item
class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
```

Atualize o arquivo `backend/app/schemas/__init__.py`:

```python
from .item import Item, ItemCreate, ItemUpdate
```

### Operações CRUD

Crie o arquivo `backend/app/crud/item.py`:

```python
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        return None
    
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        return False
    
    db.delete(db_item)
    db.commit()
    return True
```

Atualize o arquivo `backend/app/crud/__init__.py`:

```python
from .item import get_items, get_item, create_item, update_item, delete_item
```

### API FastAPI

Crie o arquivo `backend/app/main.py`:

```python
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, crud, schemas
from .database import engine, get_db

# Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(title="CRUD API", description="API RESTful para CRUD de itens com FastAPI")

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de CRUD com FastAPI e SQLAlchemy"}

@app.get("/api/items/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/api/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item

@app.post("/api/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.put("/api/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"detail": "Item excluído com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## Implementação do Frontend

### Configuração do Projeto React

O frontend já foi criado com `create-react-app`. Vamos criar os componentes e páginas necessários.

### Serviço de API

Crie o arquivo `frontend/src/services/api.js`:

```javascript
import axios from 'axios';

// Criar instância do Axios com configuração base
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Funções de API para itens
export const ItemService = {
  // Listar todos os itens
  getItems: async () => {
    const response = await api.get('/items/');
    return response.data;
  },
  
  // Obter um item específico por ID
  getItem: async (id) => {
    const response = await api.get(`/items/${id}`);
    return response.data;
  },
  
  // Criar um novo item
  createItem: async (itemData) => {
    const response = await api.post('/items/', itemData);
    return response.data;
  },
  
  // Atualizar um item existente
  updateItem: async (id, itemData) => {
    const response = await api.put(`/items/${id}`, itemData);
    return response.data;
  },
  
  // Excluir um item
  deleteItem: async (id) => {
    const response = await api.delete(`/items/${id}`);
    return response.data;
  }
};

export default api;
```

### Componentes React

Crie os componentes principais:

#### NavBar.js

Crie o arquivo `frontend/src/components/NavBar.js`:

```javascript
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  AppBar, Toolbar, Typography, Button, IconButton
} from '@material-ui/core';
import { Home as HomeIcon } from '@material-ui/icons';

const NavBar = () => {
  return (
    <AppBar position="static" color="primary" style={{ marginBottom: '2rem' }}>
      <Toolbar>
        <IconButton 
          edge="start" 
          color="inherit" 
          component={RouterLink} 
          to="/"
        >
          <HomeIcon />
        </IconButton>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          CRUD com FastAPI e React
        </Typography>
        <Button color="inherit" component={RouterLink} to="/">
          Itens
        </Button>
        <Button color="inherit" component={RouterLink} to="/create">
          Novo Item
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
```

#### ItemForm.js

Crie o arquivo `frontend/src/components/ItemForm.js`:

```javascript
import React from 'react';
import { useForm } from 'react-hook-form';
import { 
  Button, TextField, FormControl, FormControlLabel, 
  Checkbox, FormHelperText, Grid, MenuItem
} from '@material-ui/core';

const ItemForm = ({ item, onSubmit, isEditMode = false }) => {
  // Inicializar React Hook Form
  const { 
    register, 
    handleSubmit, 
    formState: { errors },
    reset
  } = useForm({
    defaultValues: item ? {
      title: item.title || '',
      description: item.description || '',
      priority: item.priority || 1,
      completed: item.completed || false
    } : {
      title: '',
      description: '',
      priority: 1,
      completed: false
    }
  });

  // Opções de prioridade
  const priorityOptions = [
    { value: 1, label: '1 - Baixa' },
    { value: 2, label: '2 - Normal' },
    { value: 3, label: '3 - Média' },
    { value: 4, label: '4 - Alta' },
    { value: 5, label: '5 - Urgente' }
  ];

  // Processar envio do formulário
  const processSubmit = (data) => {
    onSubmit(data);
    if (!isEditMode) {
      reset();
    }
  };

  return (
    <form onSubmit={handleSubmit(processSubmit)}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Título"
            variant="outlined"
            error={!!errors.title}
            helperText={errors.title ? errors.title.message : ''}
            {...register('title', { 
              required: 'Título é obrigatório',
              maxLength: {
                value: 100,
                message: 'O título não pode ter mais de 100 caracteres'
              }
            })}
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Descrição"
            variant="outlined"
            multiline
            rows={4}
            {...register('description')}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            select
            fullWidth
            label="Prioridade"
            variant="outlined"
            defaultValue={1}
            {...register('priority')}
          >
            {priorityOptions.map(option => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl error={!!errors.completed}>
            <FormControlLabel
              control={
                <Checkbox
                  color="primary"
                  {...register('completed')}
                />
              }
              label="Concluído"
            />
            {errors.completed && (
              <FormHelperText>{errors.completed.message}</FormHelperText>
            )}
          </FormControl>
        </Grid>
        
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
          >
            {isEditMode ? 'Atualizar' : 'Criar'} Item
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default ItemForm;
```

#### ItemList.js

Crie o arquivo `frontend/src/components/ItemList.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ItemService } from '../services/api';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
  Paper, Button, IconButton, Typography, Box, Chip 
} from '@material-ui/core';
import { 
  Delete as DeleteIcon, 
  Edit as EditIcon,
  CheckCircle as CheckIcon,
  RadioButtonUnchecked as UncheckedIcon
} from '@material-ui/icons';

const ItemList = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar itens ao montar o componente
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const data = await ItemService.getItems();
        setItems(data);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar itens');
        setLoading(false);
        console.error(err);
      }
    };

    fetchItems();
  }, []);

  // Função para excluir um item
  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este item?')) {
      try {
        await ItemService.deleteItem(id);
        setItems(items.filter(item => item.id !== id));
      } catch (err) {
        alert('Erro ao excluir item');
        console.error(err);
      }
    }
  };

  // Função para alternar o status de conclusão
  const handleToggleComplete = async (id, completed) => {
    try {
      const updatedItem = await ItemService.updateItem(id, { completed: !completed });
      setItems(items.map(item => item.id === id ? updatedItem : item));
    } catch (err) {
      alert('Erro ao atualizar item');
      console.error(err);
    }
  };

  if (loading) {
    return <Typography>Carregando...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">Lista de Itens</Typography>
        <Button 
          variant="contained" 
          color="primary" 
          component={Link} 
          to="/create"
        >
          Adicionar Novo Item
        </Button>
      </Box>
      
      {items.length === 0 ? (
        <Typography>Nenhum item encontrado. Comece adicionando um!</Typography>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell width="50px">Status</TableCell>
                <TableCell>Título</TableCell>
                <TableCell>Prioridade</TableCell>
                <TableCell>Criado em</TableCell>
                <TableCell width="120px">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>
                    <IconButton 
                      size="small" 
                      onClick={() => handleToggleComplete(item.id, item.completed)}
                    >
                      {item.completed ? 
                        <CheckIcon style={{ color: 'green' }} /> : 
                        <UncheckedIcon />}
                    </IconButton>
                  </TableCell>
                  <TableCell>
                    <Link to={`/items/${item.id}`} style={{ textDecoration: 'none' }}>
                      <Typography 
                        style={{ 
                          textDecoration: item.completed ? 'line-through' : 'none',
                          color: item.completed ? '#888' : 'inherit' 
                        }}
                      >
                        {item.title}
                      </Typography>
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Chip 
                      size="small" 
                      label={`P${item.priority}`} 
                      color={item.priority > 3 ? "secondary" : "default"}
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(item.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <IconButton 
                      size="small"
                      component={Link}
                      to={`/edit/${item.id}`}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton 
                      size="small"
                      onClick={() => handleDelete(item.id)}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default ItemList;
```

### Páginas da Aplicação

#### Home.js

Crie o arquivo `frontend/src/pages/Home.js`:

```javascript
import React from 'react';
import { Container, Typography, Box } from '@material-ui/core';
import ItemList from '../components/ItemList';

const Home = () => {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h4" component="h1" align="center" gutterBottom>
          Gerenciador de Itens
        </Typography>
        <Typography variant="subtitle1" align="center" paragraph>
          Sistema CRUD completo com FastAPI, React e SQLite
        </Typography>
        <ItemList />
      </Box>
    </Container>
  );
};

export default Home;
```

#### CreateItem.js

Crie o arquivo `frontend/src/pages/CreateItem.js`:

```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, Box } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import ItemForm from '../components/ItemForm';
import { ItemService } from '../services/api';

const CreateItem = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const handleSubmit = async (data) => {
    try {
      await ItemService.createItem(data);
      navigate('/');
    } catch (err) {
      setError('Erro ao criar item. Verifique os dados e tente novamente.');
      console.error(err);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper style={{ padding: '2rem' }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Adicionar Novo Item
        </Typography>
        
        {error && (
          <Box my={2}>
            <Alert severity="error">{error}</Alert>
          </Box>
        )}
        
        <ItemForm onSubmit={handleSubmit} />
      </Paper>
    </Container>
  );
};

export default CreateItem;
```

#### EditItem.js

Crie o arquivo `frontend/src/pages/EditItem.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, Box, CircularProgress } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import ItemForm from '../components/ItemForm';
import { ItemService } from '../services/api';

const EditItem = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar dados do item
  useEffect(() => {
    const fetchItem = async () => {
      try {
        const data = await ItemService.getItem(id);
        setItem(data);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar o item');
        setLoading(false);
        console.error(err);
      }
    };

    fetchItem();
  }, [id]);

  // Lidar com a atualização do item
  const handleSubmit = async (data) => {
    try {
      await ItemService.updateItem(id, data);
      navigate(`/items/${id}`);
    } catch (err) {
      setError('Erro ao atualizar item');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="md" style={{ textAlign: 'center', padding: '3rem' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !item) {
    return (
      <Container maxWidth="md">
        <Alert severity="error">
          {error || 'Item não encontrado'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Paper style={{ padding: '2rem' }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Editar Item
        </Typography>
        
        <ItemForm item={item} onSubmit={handleSubmit} isEditMode={true} />
      </Paper>
    </Container>
  );
};

export default EditItem;
```

#### ItemDetail.js

Crie o arquivo `frontend/src/pages/ItemDetail.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Container, Typography, Paper, Box, Button, Chip, Divider, 
  CircularProgress, Grid
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { 
  Edit as EditIcon, 
  Delete as DeleteIcon,
  CheckCircle as CheckIcon,
  RadioButtonUnchecked as UncheckedIcon
} from '@material-ui/icons';
import { ItemService } from '../services/api';

const ItemDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar dados do item
  useEffect(() => {
    const fetchItem = async () => {
      try {
        const data = await ItemService.getItem(id);
        setItem(data);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar item');
        setLoading(false);
        console.error(err);
      }
    };

    fetchItem();
  }, [id]);

  // Função para excluir o item
  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja excluir este item?')) {
      try {
        await ItemService.deleteItem(id);
        navigate('/');
      } catch (err) {
        setError('Erro ao excluir item');
        console.error(err);
      }
    }
  };

  // Função para alternar o status de conclusão
  const handleToggleComplete = async () => {
    try {
      const updatedItem = await ItemService.updateItem(id, { completed: !item.completed });
      setItem(updatedItem);
    } catch (err) {
      setError('Erro ao atualizar item');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="md" style={{ textAlign: 'center', padding: '3rem' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !item) {
    return (
      <Container maxWidth="md">
        <Alert severity="error">
          {error || 'Item não encontrado'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Paper style={{ padding: '2rem' }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="h4" gutterBottom>
              {item.title}
            </Typography>
            <Box display="flex" alignItems="center" mb={2}>
              <Chip 
                label={`Prioridade: ${item.priority}`} 
                color={item.priority > 3 ? "secondary" : "default"}
                style={{ marginRight: '1rem' }}
              />
              <Chip 
                icon={item.completed ? <CheckIcon /> : <UncheckedIcon />}
                label={item.completed ? "Concluído" : "Pendente"}
                color={item.completed ? "primary" : "default"}
                onClick={handleToggleComplete}
              />
            </Box>
          </Box>
          <Box>
            <Button 
              variant="outlined" 
              color="primary" 
              startIcon={<EditIcon />}
              component={Link}
              to={`/edit/${item.id}`}
              style={{ marginRight: '1rem' }}
            >
              Editar
            </Button>
            <Button 
              variant="outlined" 
              color="secondary" 
              startIcon={<DeleteIcon />}
              onClick={handleDelete}
            >
              Excluir
            </Button>
          </Box>
        </Box>
        
        <Divider style={{ margin: '1rem 0' }} />
        
        <Box my={3}>
          <Typography variant="h6" gutterBottom>
            Descrição
          </Typography>
          <Typography paragraph>
            {item.description || 'Nenhuma descrição fornecida.'}
          </Typography>
        </Box>
        
        <Box mt={4}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="textSecondary">
                Criado em: {new Date(item.created_at).toLocaleString()}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="textSecondary">
                Última atualização: {item.updated_at ? new Date(item.updated_at).toLocaleString() : 'N/A'}
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </Paper>
      
      <Box mt={2} display="flex" justifyContent="flex-start">
        <Button 
          variant="text" 
          color="primary"
          component={Link}
          to="/"
        >
          Voltar para a Lista
        </Button>
      </Box>
    </Container>
  );
};

export default ItemDetail;
```

### Roteamento

Atualize o arquivo `frontend/src/App.js`:

```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline, Container } from '@material-ui/core';

// Componentes
import NavBar from './components/NavBar';

// Páginas
import Home from './pages/Home';
import CreateItem from './pages/CreateItem';
import EditItem from './pages/EditItem';
import ItemDetail from './pages/ItemDetail';

// Criar tema
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <NavBar />
        <Container>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/create" element={<CreateItem />} />
            <Route path="/edit/:id" element={<EditItem />} />
            <Route path="/items/:id" element={<ItemDetail />} />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
}

export default App;
```

## Executando a Aplicação

Agora podemos executar nossa aplicação completa:

### Executando o Backend

```bash
# Navegar para o diretório do backend
cd backend

# Ativar o ambiente virtual (se necessário)
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Executar o servidor
python -m app.main
```

O servidor FastAPI será iniciado em `http://localhost:8000`. Você também pode acessar a documentação interativa da API em `http://localhost:8000/docs`.

### Executando o Frontend

Em um novo terminal:

```bash
# Navegar para o diretório frontend
cd frontend

# Iniciar o servidor de desenvolvimento React
npm start
```

O aplicativo React será iniciado em `http://localhost:3000`.

## Próximos Passos

Agora que você tem uma aplicação CRUD funcional, você pode considerar as seguintes melhorias:

1. **Autenticação e Autorização**: Adicionar login de usuários e controle de acesso
2. **Filtros e Ordenação**: Permitir que os usuários filtrem e ordenem a lista de itens
3. **Paginação**: Adicionar suporte para paginação em listas grandes
4. **Testes**: Implementar testes unitários e de integração
5. **Estado Global**: Usar Redux ou Context API para gerenciar o estado global
6. **Estilização Avançada**: Melhorar a UI com animações e temas personalizados
7. **Pesquisa**: Adicionar funcionalidade de pesquisa
8. **Categorias ou Tags**: Adicionar suporte para categorização de itens
9. **Dockerização**: Empacotar a aplicação em containers Docker
10. **Deployment**: Publicar a aplicação em um servidor de produção

Parabéns por concluir este tutorial! Você agora tem uma aplicação CRUD completa com FastAPI, React e SQLite que pode ser usada como base para projetos mais complexos. 