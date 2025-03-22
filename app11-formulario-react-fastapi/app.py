# Formulário no React enviando dados para o backend (FastAPI)
# Autor: Claude
# Data: Março/2025

# 1. INTRODUÇÃO E CONCEITOS BÁSICOS
# Este arquivo apresenta os conceitos fundamentais para criar um formulário no React
# que envia dados para um backend construído com FastAPI. O foco está na comunicação
# entre frontend e backend, validação de dados e tratamento de respostas.

# 2. CONFIGURAÇÃO DO AMBIENTE
# Para este projeto, precisamos das seguintes dependências:
# 
# Backend (FastAPI):
# - FastAPI: Framework web moderno para APIs em Python
# - Uvicorn: Servidor ASGI para executar a aplicação FastAPI
# - Pydantic: Validação de dados e configurações
# - python-multipart: Para processar dados de formulário
# 
# Instalação:
# pip install fastapi uvicorn pydantic python-multipart
#
# Frontend (React):
# - React: Biblioteca JavaScript para interfaces de usuário
# - Axios: Biblioteca para fazer requisições HTTP
# - React Hook Form: Biblioteca para gerenciar formulários
#
# Instalação:
# npx create-react-app frontend
# cd frontend
# npm install axios react-hook-form

# 3. ESTRUTURA DO PROJETO
# Este projeto seguirá a seguinte estrutura:
#
# app11-formulario-react-fastapi/
# ├── backend/                    # Código do servidor FastAPI
# │   ├── main.py                 # Aplicação FastAPI principal
# │   ├── models.py               # Modelos de dados (Pydantic)
# │   ├── requirements.txt        # Dependências do backend
# │   └── venv/                   # Ambiente virtual Python
# │
# └── frontend/                   # Código da aplicação React
#     ├── node_modules/           # Dependências do frontend (gerado pelo npm)
#     ├── public/                 # Arquivos estáticos públicos
#     ├── src/                    # Código-fonte do React
#     │   ├── components/         # Componentes React
#     │   ├── services/           # Serviços para comunicação com a API
#     │   ├── App.js              # Componente principal da aplicação
#     │   └── index.js            # Ponto de entrada do React
#     ├── package.json            # Configurações e dependências do npm
#     └── README.md               # Documentação do frontend

# 4. BACKEND COM FASTAPI
# O backend será responsável por receber e processar os dados enviados pelo formulário,
# realizar validações e retornar respostas adequadas.

"""
# backend/models.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

class UserForm(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str
    age: Optional[int] = Field(None, ge=18, le=120)
    message: str = Field(..., min_length=10, max_length=500)
    subscribe: bool = False
    
    @validator('phone')
    def phone_must_be_valid(cls, v):
        # Padrão simples para validar telefone: (99) 99999-9999 ou semelhante
        pattern = r'^\(?\d{2}\)?[\s-]?9?\d{4}[-\s]?\d{4}$'
        if not re.match(pattern, v):
            raise ValueError('Número de telefone inválido')
        return v

class ResponseMessage(BaseModel):
    message: str
    status: str
    form_id: Optional[str] = None
"""

"""
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import UserForm, ResponseMessage
import uuid

app = FastAPI(title="Formulário API", description="API para receber dados de formulários")

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origem do frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Em um sistema real, os dados seriam armazenados em um banco de dados
form_submissions = {}

@app.get("/")
async def read_root():
    return {"message": "API de Formulários com FastAPI"}

@app.post("/api/submit-form", response_model=ResponseMessage)
async def submit_form(form_data: UserForm):
    try:
        # Gerar um ID único para a submissão
        form_id = str(uuid.uuid4())
        
        # Armazenar os dados (em produção, seria em um banco de dados)
        form_submissions[form_id] = form_data.dict()
        
        # Retornar uma resposta de sucesso
        return ResponseMessage(
            message="Formulário recebido com sucesso!",
            status="success",
            form_id=form_id
        )
    except Exception as e:
        # Em caso de erro, retornar uma resposta adequada
        raise HTTPException(status_code=500, detail=f"Erro ao processar formulário: {str(e)}")

@app.get("/api/submissions/{form_id}")
async def get_submission(form_id: str):
    if form_id not in form_submissions:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    
    return form_submissions[form_id]

@app.get("/api/submissions")
async def get_all_submissions():
    return form_submissions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

# 5. FRONTEND COM REACT
# O frontend será responsável por criar um formulário de usuário, validar os campos,
# enviar os dados para o backend e exibir feedback ao usuário.

# 5.1 Serviço para comunicação com a API
# Vamos criar um serviço para encapsular as chamadas à API:

"""
// frontend/src/services/api.js
import axios from 'axios';

// Configuração base do Axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Enviar dados do formulário para o backend
export const submitForm = async (formData) => {
  try {
    const response = await api.post('/submit-form', formData);
    return response.data;
  } catch (error) {
    // Em caso de erro, formatar uma resposta amigável
    const errorMessage = error.response?.data?.detail || error.message || 'Erro ao enviar formulário';
    throw new Error(errorMessage);
  }
};

// Buscar submissão específica
export const getSubmission = async (formId) => {
  const response = await api.get(`/submissions/${formId}`);
  return response.data;
};

// Buscar todas as submissões
export const getAllSubmissions = async () => {
  const response = await api.get('/submissions');
  return response.data;
};

export default api;
"""

# 5.2 Componente de Formulário
# Vamos criar um componente React para o formulário usando React Hook Form:

"""
// frontend/src/components/UserForm.js
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { submitForm } from '../services/api';
import './UserForm.css';

const UserForm = () => {
  // Estado para controlar o envio e mensagens
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);
  
  // Configuração do React Hook Form
  const { 
    register, 
    handleSubmit, 
    formState: { errors },
    reset 
  } = useForm();
  
  // Função para lidar com o envio do formulário
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setSubmissionResult(null);
    
    try {
      const result = await submitForm(data);
      setSubmissionResult({
        type: 'success',
        message: result.message,
        formId: result.form_id
      });
      
      // Resetar o formulário após o envio bem-sucedido
      reset();
    } catch (error) {
      setSubmissionResult({
        type: 'error',
        message: error.message
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="form-container">
      <h2>Formulário de Contato</h2>
      
      {/* Mensagem de sucesso ou erro */}
      {submissionResult && (
        <div className={`notification ${submissionResult.type}`}>
          <p>{submissionResult.message}</p>
          {submissionResult.formId && (
            <p>ID do formulário: {submissionResult.formId}</p>
          )}
        </div>
      )}
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group">
          <label htmlFor="name">Nome Completo</label>
          <input
            id="name"
            {...register('name', { 
              required: 'Nome é obrigatório', 
              minLength: { value: 3, message: 'Nome deve ter pelo menos 3 caracteres' }
            })}
          />
          {errors.name && <span className="error">{errors.name.message}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            type="email"
            {...register('email', { 
              required: 'E-mail é obrigatório',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'E-mail inválido'
              }
            })}
          />
          {errors.email && <span className="error">{errors.email.message}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="phone">Telefone</label>
          <input
            id="phone"
            {...register('phone', { 
              required: 'Telefone é obrigatório',
              pattern: {
                value: /^\(?\d{2}\)?[\s-]?9?\d{4}[-\s]?\d{4}$/,
                message: 'Telefone inválido. Use o formato (99) 99999-9999'
              }
            })}
            placeholder="(99) 99999-9999"
          />
          {errors.phone && <span className="error">{errors.phone.message}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="age">Idade (opcional)</label>
          <input
            id="age"
            type="number"
            {...register('age', { 
              min: { value: 18, message: 'Você deve ter pelo menos 18 anos' },
              max: { value: 120, message: 'Idade inválida' }
            })}
          />
          {errors.age && <span className="error">{errors.age.message}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="message">Mensagem</label>
          <textarea
            id="message"
            {...register('message', { 
              required: 'Mensagem é obrigatória',
              minLength: { value: 10, message: 'Mensagem deve ter pelo menos 10 caracteres' }
            })}
            rows="5"
          ></textarea>
          {errors.message && <span className="error">{errors.message.message}</span>}
        </div>
        
        <div className="form-group checkbox">
          <input
            id="subscribe"
            type="checkbox"
            {...register('subscribe')}
          />
          <label htmlFor="subscribe">Desejo receber novidades por e-mail</label>
        </div>
        
        <button 
          type="submit" 
          className="submit-button" 
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Enviando...' : 'Enviar Formulário'}
        </button>
      </form>
    </div>
  );
};

export default UserForm;
"""

# 5.3 Estilo para o Formulário
# Vamos adicionar estilos CSS para o formulário:

"""
/* frontend/src/components/UserForm.css */
.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 5px rgba(74, 144, 226, 0.3);
}

.checkbox {
  display: flex;
  align-items: center;
}

.checkbox input {
  width: auto;
  margin-right: 10px;
}

.checkbox label {
  margin-bottom: 0;
}

.error {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
  display: block;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #3a7cc5;
}

.submit-button:disabled {
  background-color: #a0c3e8;
  cursor: not-allowed;
}

.notification {
  padding: 10px 15px;
  margin-bottom: 20px;
  border-radius: 4px;
}

.notification.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.notification.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
"""

# 5.4 Componente Principal da Aplicação
# Atualizamos o App.js para usar nosso formulário:

"""
// frontend/src/App.js
import React from 'react';
import UserForm from './components/UserForm';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Formulário React com FastAPI</h1>
        <p>Exemplo de integração entre React e FastAPI</p>
      </header>
      
      <main className="app-content">
        <UserForm />
      </main>
      
      <footer className="app-footer">
        <p>Demonstração de formulário React enviando dados para FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
"""

# 5.5 Estilo para o App Principal
# Vamos adicionar estilos CSS para o aplicativo principal:

"""
/* frontend/src/App.css */
.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.app-header h1 {
  margin-bottom: 10px;
  color: #333;
}

.app-header p {
  color: #666;
}

.app-content {
  margin-bottom: 30px;
}

.app-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
  color: #666;
  font-size: 0.9em;
}
"""

# 6. EXECUÇÃO DO PROJETO
# Para executar o projeto, você precisa iniciar tanto o backend quanto o frontend:
#
# Backend (pasta backend):
# cd backend
# python -m uvicorn main:app --reload
# Isso iniciará o servidor FastAPI em http://localhost:8000
#
# Frontend (pasta frontend):
# cd frontend
# npm start
# Isso iniciará o servidor de desenvolvimento do React em http://localhost:3000

# 7. COMUNICAÇÃO ENTRE FRONTEND E BACKEND
# 
# 7.1. Entendendo o Fluxo de Dados
# - O usuário preenche o formulário no frontend React
# - React Hook Form valida os dados no frontend
# - Axios envia os dados para a API FastAPI via POST
# - FastAPI valida novamente os dados usando Pydantic
# - O backend processa os dados e retorna uma resposta
# - O frontend exibe mensagens de sucesso ou erro

# 8. VALIDAÇÃO DE DADOS
# 
# 8.1. Validação no Frontend (React Hook Form)
# - Validação instantânea durante a digitação
# - Feedback visual imediato para o usuário
# - Evita envio de dados inválidos
#
# 8.2. Validação no Backend (Pydantic)
# - Garante a integridade dos dados mesmo se a validação frontend for burlada
# - Tipos de dados corretos (strings, números, booleanos)
# - Regras de negócio (comprimento mínimo, formato de e-mail, etc.)

# 9. BOAS PRÁTICAS
# 
# 9.1. Segurança
# - Validação rigorosa no backend
# - Sanitização de dados para evitar injeções
# - Proteger rotas sensíveis (se aplicável)
#
# 9.2. Experiência do Usuário
# - Feedback claro sobre erros de validação
# - Indicação de campos obrigatórios
# - Feedback sobre o status de envio (loading, sucesso, erro)
#
# 9.3. Código Limpo
# - Separação de responsabilidades (components, services)
# - Manipuladores de erros adequados
# - Tipagem clara (TypeScript no frontend ou Python type hints)

# 10. MELHORIAS FUTURAS
# 
# 10.1. Autenticação e Autorização
# - Implementar login/registro de usuários
# - Proteger rotas com JWT ou OAuth
# - Perfis de usuário para ver seus formulários enviados
#
# 10.2. Persistência de Dados
# - Conectar a um banco de dados (PostgreSQL, MongoDB)
# - Implementar ORM (SQLAlchemy) no backend
#
# 10.3. Funcionalidades Adicionais
# - Upload de arquivos com o formulário
# - Envio de confirmação por e-mail
# - Dashboard administrativo para gerenciar submissões
# - Paginação para listar muitas submissões

# 11. CONSIDERAÇÕES PARA PRODUÇÃO
# 
# 11.1. Configuração do Servidor
# - Usar Gunicorn ou Uvicorn em produção
# - Configurar proxy reverso (Nginx)
# - Configurar HTTPS para comunicação segura
#
# 11.2. Otimizações
# - Build otimizado do React para produção
# - Minificação de assets
# - Lazy loading para componentes pesados

# 12. CONCLUSÃO
# Este projeto demonstra como integrar um formulário React com um backend FastAPI.
# A combinação de React com FastAPI oferece:
# - Frontend responsivo e interativo com validação em tempo real
# - Backend rápido, tipado e com documentação automática
# - Arquitetura escalável para futuras expansões
#
# Usando essas tecnologias juntas, você pode criar aplicações web modernas
# com excelente experiência do usuário e uma API robusta. 