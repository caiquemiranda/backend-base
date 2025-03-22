# Tutorial: Formulário em React com Backend FastAPI

Este tutorial mostra como criar um formulário em React que envia dados para um backend FastAPI, implementando validação em ambos os lados e feedback para o usuário.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Implementação do Backend (FastAPI)](#implementação-do-backend-fastapi)
4. [Implementação do Frontend (React)](#implementação-do-frontend-react)
5. [Executando e Testando a Aplicação](#executando-e-testando-a-aplicação)
6. [Resolução de Problemas Comuns](#resolução-de-problemas-comuns)
7. [Próximos Passos](#próximos-passos)

## Pré-requisitos

Para seguir este tutorial, você precisará ter instalado:

- Python 3.7 ou superior
- Node.js e npm (versão LTS recomendada)
- Editor de código (como VSCode, PyCharm, etc.)
- Conhecimentos básicos de:
  - Python e FastAPI
  - JavaScript/React
  - HTML e CSS

## Configuração do Ambiente

Vamos começar configurando a estrutura do projeto:

```bash
# Criar a estrutura do projeto
mkdir -p app11-formulario-react-fastapi/{backend,frontend}
cd app11-formulario-react-fastapi
```

### Configurando o Backend

```bash
# Entrar no diretório backend
cd backend

# Criar um ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instalar as dependências
pip install fastapi uvicorn pydantic[email] python-multipart

# Criar arquivo de requisitos
pip freeze > requirements.txt
```

### Configurando o Frontend

```bash
# Voltar para o diretório raiz do projeto
cd ..

# Criar uma aplicação React usando create-react-app
npx create-react-app frontend

# Entrar no diretório frontend
cd frontend

# Instalar as dependências necessárias
npm install axios react-hook-form
```

## Implementação do Backend (FastAPI)

Agora vamos implementar o backend com FastAPI, que será responsável por receber os dados do formulário, validá-los e retornar uma resposta.

### Passo 1: Criar os Modelos de Dados

Crie um arquivo chamado `models.py` no diretório `backend`:

```python
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
```

Este código define dois modelos Pydantic:
- `UserForm`: Define a estrutura dos dados do formulário que o backend irá receber, incluindo validações.
- `ResponseMessage`: Define a estrutura da resposta que o backend irá enviar.

### Passo 2: Criar a Aplicação FastAPI

Crie um arquivo chamado `main.py` no diretório `backend`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import UserForm, ResponseMessage
import uuid

# Inicializar a aplicação FastAPI
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

# Para execução direta do arquivo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

Este código cria uma API com FastAPI que:
- Configura CORS para permitir comunicação com o frontend
- Define um endpoint para receber os dados do formulário
- Implementa endpoints para consultar dados enviados
- Armazena os dados em memória (em um projeto real, você usaria um banco de dados)

## Implementação do Frontend (React)

Agora vamos implementar o frontend com React, que será responsável por criar o formulário, validar os dados e enviar para o backend.

### Passo 1: Configurar o Serviço de API

Crie uma pasta `services` dentro do diretório `frontend/src` e adicione um arquivo chamado `api.js`:

```bash
# Certifique-se de estar no diretório frontend
mkdir -p src/services
```

Adicione o seguinte código ao arquivo `src/services/api.js`:

```javascript
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
```

Este código configura o Axios para se comunicar com a API FastAPI e define funções para enviar e buscar dados.

### Passo 2: Criar o Componente de Formulário

Crie uma pasta `components` dentro do diretório `frontend/src` e adicione arquivos para o componente de formulário:

```bash
# Certifique-se de estar no diretório frontend
mkdir -p src/components
```

Primeiro, vamos criar o arquivo `src/components/UserForm.js`:

```javascript
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
```

Agora, vamos criar o arquivo CSS para estilizar o formulário em `src/components/UserForm.css`:

```css
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
```

### Passo 3: Atualizar o Componente App

Modifique o arquivo `src/App.js` para incluir o componente de formulário:

```javascript
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
```

E também atualize o arquivo `src/App.css`:

```css
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
```

## Executando e Testando a Aplicação

Agora vamos executar e testar a aplicação completa.

### Iniciando o Backend

Abra um terminal e siga estes passos:

```bash
# Certifique-se de estar no diretório backend
cd app11-formulario-react-fastapi/backend

# Ative o ambiente virtual (se ainda não estiver ativado)
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Execute o servidor FastAPI
uvicorn main:app --reload
```

O servidor FastAPI será iniciado em http://localhost:8000. Você pode acessar a documentação automática em http://localhost:8000/docs.

### Iniciando o Frontend

Abra outro terminal e siga estes passos:

```bash
# Certifique-se de estar no diretório frontend
cd app11-formulario-react-fastapi/frontend

# Execute o servidor de desenvolvimento React
npm start
```

O aplicativo React será iniciado em http://localhost:3000.

### Testando o Formulário

1. Abra o navegador e acesse http://localhost:3000
2. Preencha o formulário com dados válidos
3. Clique em "Enviar Formulário"
4. Você deve ver uma mensagem de sucesso com o ID do formulário
5. Para verificar os dados enviados, acesse http://localhost:8000/docs e teste o endpoint `/api/submissions` para ver todos os formulários enviados

## Resolução de Problemas Comuns

### Erro de CORS

Se você encontrar erros relacionados a CORS, verifique:

1. Se o middleware CORS está configurado corretamente no backend
2. Se a origem permitida corresponde exatamente à URL do frontend (`http://localhost:3000`)

### Erro de Validação

Se os dados não passarem na validação:

1. Verifique as mensagens de erro no frontend para entender o problema
2. Consulte os logs do backend para ver detalhes sobre a validação que falhou
3. Verifique se as regras de validação no frontend e backend estão consistentes

### Erro de Conexão

Se o frontend não conseguir se conectar ao backend:

1. Verifique se o servidor FastAPI está em execução
2. Verifique se as URLs no frontend estão apontando para o endereço correto do backend
3. Verifique se não há bloqueios de firewall impedindo a comunicação

## Próximos Passos

Após completar este tutorial básico, você pode expandir o projeto com:

### Persistência de Dados

Substituir o armazenamento em memória por um banco de dados:

```python
# Exemplo com SQLAlchemy e SQLite
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./forms.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FormModel(Base):
    __tablename__ = "forms"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    age = Column(Integer, nullable=True)
    message = Column(Text)
    subscribe = Column(Boolean, default=False)

# Criar tabelas
Base.metadata.create_all(bind=engine)
```

### Autenticação de Usuários

Adicionar login e proteção para rotas sensíveis:

```bash
# Instalar bibliotecas necessárias
pip install fastapi-users[sqlalchemy]
```

### Upload de Arquivos

Adicionar suporte para upload de arquivos ao formulário:

```python
# No backend
from fastapi import File, UploadFile

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Processar o arquivo
    contents = await file.read()
    # Salvar em algum lugar
    return {"filename": file.filename}
```

```javascript
// No frontend (adicionando suporte a arquivos)
const FileUpload = () => {
  const [file, setFile] = useState(null);
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };
  
  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post('http://localhost:8000/api/upload', formData);
      console.log(response.data);
    } catch (error) {
      console.error('Erro ao fazer upload:', error);
    }
  };
  
  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};
```

## Conclusão

Parabéns! Você implementou com sucesso um formulário em React que se comunica com um backend FastAPI. Este é um padrão comum em aplicações web modernas, onde o frontend é responsável pela interface e experiência do usuário, enquanto o backend processa, valida e armazena os dados.

As principais vantagens desta arquitetura são:

1. **Separação de responsabilidades**: Frontend e backend podem ser desenvolvidos e escalados independentemente
2. **Validação em camadas**: Tanto o frontend quanto o backend validam os dados, garantindo maior segurança
3. **Experiência de usuário melhorada**: Feedback instantâneo de validação no frontend
4. **API reutilizável**: O backend pode servir a múltiplos clientes (web, mobile, etc.)

Este conhecimento é fundamental para o desenvolvimento de aplicações web modernas e pode ser expandido para sistemas mais complexos, como um sistema de CRM, e-commerce, ou qualquer outra aplicação que envolva formulários e comunicação cliente-servidor.
