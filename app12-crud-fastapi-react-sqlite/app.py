# CRUD Completo: Backend FastAPI + Frontend React + SQLite
# Autor: Claude
# Data: Março/2025

# 1. INTRODUÇÃO E CONCEITOS BÁSICOS
# Este arquivo apresenta os conceitos e implementação de um sistema CRUD completo
# (Create, Read, Update, Delete) utilizando FastAPI para o backend,
# React para o frontend e SQLite como banco de dados.

# 2. CONFIGURAÇÃO DO AMBIENTE
# Para este projeto, precisamos das seguintes dependências:
# 
# Backend (FastAPI):
# - FastAPI: Framework web para APIs em Python
# - Uvicorn: Servidor ASGI para executar a aplicação FastAPI
# - SQLAlchemy: ORM (Object-Relational Mapping) para banco de dados
# - Pydantic: Validação de dados e serialização
# - python-multipart: Processar dados de formulário
# - sqlite3: Banco de dados (já incluso no Python)
# 
# Instalação:
# pip install fastapi uvicorn sqlalchemy pydantic python-multipart
#
# Frontend (React):
# - React: Biblioteca JavaScript para interfaces
# - Axios: Cliente HTTP para requisições à API
# - React Router: Navegação entre páginas
# - React Hook Form: Gerenciamento de formulários
# - Material-UI (opcional): Componentes visuais prontos
#
# Instalação:
# npx create-react-app frontend
# cd frontend
# npm install axios react-router-dom react-hook-form @material-ui/core @material-ui/icons

# 3. ESTRUTURA DO PROJETO
# Este projeto seguirá a seguinte estrutura:
#
# app12-crud-fastapi-react-sqlite/
# ├── backend/                    # Código do servidor FastAPI
# │   ├── app/                    # Módulo da aplicação
# │   │   ├── __init__.py         # Inicializador
# │   │   ├── crud/               # Operações CRUD
# │   │   │   ├── __init__.py
# │   │   │   └── item.py         # Operações CRUD para itens
# │   │   ├── database.py         # Configuração do banco de dados
# │   │   ├── main.py             # Ponto de entrada da aplicação
# │   │   ├── models/             # Modelos SQLAlchemy
# │   │   │   ├── __init__.py
# │   │   │   └── item.py         # Modelo de Item no banco de dados
# │   │   └── schemas/            # Esquemas Pydantic
# │   │       ├── __init__.py
# │   │       └── item.py         # Esquemas para validação
# │   ├── requirements.txt        # Dependências do backend
# │   └── sqlite.db               # Banco de dados SQLite
# │
# └── frontend/                   # Código da aplicação React
#     ├── node_modules/           # Dependências (geradas pelo npm)
#     ├── public/                 # Arquivos estáticos
#     ├── src/                    # Código-fonte
#     │   ├── components/         # Componentes React
#     │   │   ├── ItemForm.js     # Formulário de criação/edição
#     │   │   ├── ItemList.js     # Lista de itens
#     │   │   └── NavBar.js       # Barra de navegação
#     │   ├── pages/              # Páginas da aplicação
#     │   │   ├── CreateItem.js   # Página de criação
#     │   │   ├── EditItem.js     # Página de edição
#     │   │   ├── Home.js         # Página inicial
#     │   │   └── ItemDetail.js   # Detalhes do item
#     │   ├── services/           # Serviços para comunicação com API
#     │   │   └── api.js          # Cliente Axios configurado
#     │   ├── App.js              # Componente principal
#     │   └── index.js            # Ponto de entrada
#     ├── package.json            # Dependências npm
#     └── README.md               # Documentação do frontend

# 4. BACKEND COM FASTAPI E SQLALCHEMY
# Vamos implementar um backend com FastAPI que gerencia um CRUD para itens genéricos.

# 4.1 Configuração do Banco de Dados (backend/app/database.py)
"""
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
"""

# 4.2 Modelos SQLAlchemy (backend/app/models/item.py)
"""
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
"""

# 4.3 Esquemas Pydantic (backend/app/schemas/item.py)
"""
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
"""

# 4.4 Operações CRUD (backend/app/crud/item.py)
"""
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
"""

# 4.5 Aplicação Principal (backend/app/main.py)
"""
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
"""

# 5. FRONTEND COM REACT
# Vamos implementar o frontend da aplicação com React para interagir com nossa API.

# 5.1 Serviço API (frontend/src/services/api.js)
"""
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
"""

# 5.2 Componentes React
# 5.2.1 Componente Lista de Itens (frontend/src/components/ItemList.js)
"""
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

  // Exibir mensagem de carregamento
  if (loading) {
    return <Typography>Carregando...</Typography>;
  }

  // Exibir mensagem de erro
  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  // Renderizar tabela de itens
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
"""

# 5.2.2 Componente Formulário de Item (frontend/src/components/ItemForm.js)
"""
import React from 'react';
import { useForm } from 'react-hook-form';
import { 
  Button, TextField, FormControl, FormControlLabel, 
  Checkbox, FormHelperText, Grid, Typography, MenuItem
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
"""

# 5.2.3 Barra de Navegação (frontend/src/components/NavBar.js)
"""
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
"""

# 5.3 Páginas da Aplicação
# 5.3.1 Página Inicial (frontend/src/pages/Home.js)
"""
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
"""

# 5.3.2 Página de Criação de Item (frontend/src/pages/CreateItem.js)
"""
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
"""

# 5.3.3 Página de Edição de Item (frontend/src/pages/EditItem.js)
"""
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
"""

# 5.3.4 Página de Detalhes do Item (frontend/src/pages/ItemDetail.js)
"""
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
"""

# 5.4 Configuração das Rotas e App Principal (frontend/src/App.js)
"""
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
"""

# 6. EXECUTANDO O PROJETO
# Para executar o projeto completo:

# 6.1 Executando o Backend
# Navegue até a pasta backend e execute:
# cd backend
# pip install -r requirements.txt
# python -m app.main

# 6.2 Executando o Frontend
# Navegue até a pasta frontend e execute:
# cd frontend
# npm install
# npm start

# 7. BOAS PRÁTICAS IMPLEMENTADAS NESTE PROJETO

# 7.1 Organização do Código
# - Estrutura de diretórios organizada por funcionalidade
# - Separação clara entre backend e frontend
# - Uso de padrões arquiteturais (MVC no backend)

# 7.2 Segurança
# - Validação de dados com Pydantic
# - Tratamento de erros apropriado
# - Sanitização de entradas do usuário

# 7.3 Manutenibilidade
# - Código modular e reutilizável
# - Nomes de variáveis e funções significativos
# - Comentários explicativos

# 7.4 Experiência do Usuário
# - Interface responsiva
# - Feedback visual sobre ações (loading, erros, sucesso)
# - Confirmações para ações destrutivas

# 8. MELHORIAS FUTURAS POSSÍVEIS

# 8.1 Funcionalidades Adicionais
# - Autenticação de usuários
# - Filtros e ordenação da lista de itens
# - Paginação para grandes conjuntos de dados
# - Upload de imagens ou arquivos
# - Tags ou categorias para itens

# 8.2 Melhorias Técnicas
# - Testes unitários e de integração
# - Estado global com Redux ou Context API
# - PWA (Progressive Web App)
# - Docker para facilitar implantação
# - CI/CD para entrega contínua

# 9. CONCLUSÃO
# Este projeto demonstra a implementação completa de um CRUD (Create, Read, Update, Delete)
# usando FastAPI para o backend, React para o frontend e SQLite como banco de dados.
# A combinação dessas tecnologias permite criar aplicações web modernas, eficientes e
# escaláveis, com uma excelente experiência para o desenvolvedor e para o usuário final. 