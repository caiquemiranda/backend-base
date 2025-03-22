# Tutorial: Comunicação entre Backend (Flask) e Frontend (React)

Este tutorial mostra como implementar uma aplicação web completa com uma API REST em Flask e um frontend em React, estabelecendo comunicação eficiente entre os dois.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Implementação do Backend (Flask)](#implementação-do-backend-flask)
4. [Implementação do Frontend (React)](#implementação-do-frontend-react)
5. [Executando a Aplicação](#executando-a-aplicação)
6. [Resolvendo Problemas Comuns](#resolvendo-problemas-comuns)
7. [Próximos Passos](#próximos-passos)

## Pré-requisitos

Para seguir este tutorial, você precisará ter instalado:

- Python 3.6 ou superior
- Node.js e npm (versão LTS recomendada)
- Editor de código (como VSCode, Sublime Text, etc.)
- Conhecimento básico de JavaScript, React e Python

## Configuração do Ambiente

Vamos começar configurando a estrutura do projeto:

```bash
# Criar a estrutura do projeto
mkdir -p app10-comunicacao-flask-react/{backend,frontend}
cd app10-comunicacao-flask-react
```

### Configurando o Backend

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
pip install flask flask-cors flask-restful

# Criar arquivo de requisitos
pip freeze > requirements.txt
```

### Configurando o Frontend

```bash
# Voltar ao diretório raiz
cd ..

# Criar aplicação React
npx create-react-app frontend

# Entrar no diretório do frontend
cd frontend

# Instalar Axios para requisições HTTP
npm install axios
```

## Implementação do Backend (Flask)

Vamos criar uma API REST simples usando Flask que gerencia uma lista de tarefas.

### Passo 1: Criar o arquivo principal da API

Crie um arquivo `app.py` no diretório `backend/`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Habilitando CORS para todas as rotas
CORS(app)

# Dados de exemplo (em um projeto real, usaríamos um banco de dados)
tasks = [
    {"id": 1, "title": "Aprender Flask", "completed": True},
    {"id": 2, "title": "Aprender React", "completed": False},
    {"id": 3, "title": "Integrar Flask com React", "completed": False}
]

# Rota principal
@app.route('/')
def home():
    return jsonify({"message": "API de Tarefas"})

# Rota para obter todas as tarefas
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Rota para obter uma tarefa específica
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404

# Rota para criar uma nova tarefa
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Dados inválidos"}), 400
    
    # Em um projeto real, gere IDs de maneira segura e persistente
    task_id = max(task["id"] for task in tasks) + 1
    task = {
        "id": task_id,
        "title": request.json["title"],
        "completed": request.json.get("completed", False)
    }
    tasks.append(task)
    return jsonify(task), 201

# Rota para atualizar uma tarefa existente
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    if not request.json:
        return jsonify({"error": "Dados inválidos"}), 400
    
    task["title"] = request.json.get("title", task["title"])
    task["completed"] = request.json.get("completed", task["completed"])
    return jsonify(task)

# Rota para excluir uma tarefa
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    tasks.remove(task)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Passo 2: Testar a API

Inicie o servidor Flask:

```bash
# No diretório backend/
python app.py
```

Teste a API usando um navegador ou ferramentas como Postman, cURL ou HTTPie:

```bash
# Obter todas as tarefas
curl http://localhost:5000/api/tasks

# Criar uma nova tarefa
curl -X POST -H "Content-Type: application/json" -d '{"title":"Nova Tarefa"}' http://localhost:5000/api/tasks

# Atualizar uma tarefa
curl -X PUT -H "Content-Type: application/json" -d '{"completed":true}' http://localhost:5000/api/tasks/1

# Excluir uma tarefa
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Implementação do Frontend (React)

Agora, vamos criar o frontend com React para consumir nossa API Flask.

### Passo 1: Configurar o serviço de API

Crie um diretório `services` dentro de `frontend/src/` e crie um arquivo `api.js`:

```bash
mkdir -p frontend/src/services
```

Adicione o seguinte código ao arquivo `frontend/src/services/api.js`:

```javascript
import axios from 'axios';

// Configuração base do Axios
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Funções para interagir com a API
export const getTasks = async () => {
  const response = await api.get('/tasks');
  return response.data;
};

export const getTask = async (id) => {
  const response = await api.get(`/tasks/${id}`);
  return response.data;
};

export const createTask = async (task) => {
  const response = await api.post('/tasks', task);
  return response.data;
};

export const updateTask = async (id, task) => {
  const response = await api.put(`/tasks/${id}`, task);
  return response.data;
};

export const deleteTask = async (id) => {
  const response = await api.delete(`/tasks/${id}`);
  return response.data;
};

export default api;
```

### Passo 2: Criar os componentes React

Crie um diretório `components` dentro de `frontend/src/`:

```bash
mkdir -p frontend/src/components
```

#### Componente TaskList

Crie o arquivo `frontend/src/components/TaskList.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { getTasks, deleteTask, updateTask } from '../services/api';

const TaskList = ({ onTaskSelected, onTaskDeleted }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar tarefas quando o componente montar
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const data = await getTasks();
        setTasks(data);
        setError(null);
      } catch (err) {
        setError('Erro ao carregar tarefas: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  // Alternar o status de uma tarefa
  const toggleTaskStatus = async (taskId) => {
    try {
      const task = tasks.find(t => t.id === taskId);
      const updatedTask = {
        ...task,
        completed: !task.completed
      };
      
      const result = await updateTask(taskId, updatedTask);
      setTasks(tasks.map(t => t.id === taskId ? result : t));
    } catch (err) {
      setError('Erro ao atualizar tarefa: ' + err.message);
    }
  };

  // Remover uma tarefa
  const handleDelete = async (taskId) => {
    try {
      await deleteTask(taskId);
      setTasks(tasks.filter(t => t.id !== taskId));
      if (onTaskDeleted) onTaskDeleted();
    } catch (err) {
      setError('Erro ao excluir tarefa: ' + err.message);
    }
  };

  if (loading) return <div>Carregando tarefas...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="task-list">
      <h2>Tarefas</h2>
      {tasks.length === 0 ? (
        <p>Nenhuma tarefa encontrada.</p>
      ) : (
        <ul>
          {tasks.map(task => (
            <li key={task.id} className={task.completed ? 'completed' : ''}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTaskStatus(task.id)}
              />
              <span onClick={() => onTaskSelected && onTaskSelected(task)}>
                {task.title}
              </span>
              <button onClick={() => handleDelete(task.id)}>Excluir</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;
```

#### Componente TaskForm

Crie o arquivo `frontend/src/components/TaskForm.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { createTask, updateTask } from '../services/api';

const TaskForm = ({ task, onTaskSaved }) => {
  const [title, setTitle] = useState('');
  const [completed, setCompleted] = useState(false);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  // Se receber uma tarefa como prop, preencher o formulário para edição
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setCompleted(task.completed);
      setIsEditing(true);
    } else {
      resetForm();
    }
  }, [task]);

  const resetForm = () => {
    setTitle('');
    setCompleted(false);
    setIsEditing(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError('O título da tarefa é obrigatório');
      return;
    }

    try {
      let result;
      
      if (isEditing && task) {
        // Atualizar tarefa existente
        result = await updateTask(task.id, { title, completed });
      } else {
        // Criar nova tarefa
        result = await createTask({ title, completed });
      }
      
      resetForm();
      if (onTaskSaved) onTaskSaved(result);
    } catch (err) {
      setError('Erro ao salvar tarefa: ' + err.message);
    }
  };

  return (
    <div className="task-form">
      <h2>{isEditing ? 'Editar Tarefa' : 'Nova Tarefa'}</h2>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Título</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Digite o título da tarefa"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="completed">
            <input
              type="checkbox"
              id="completed"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
            />
            Concluída
          </label>
        </div>
        
        <div className="form-actions">
          <button type="submit">
            {isEditing ? 'Atualizar' : 'Adicionar'}
          </button>
          {isEditing && (
            <button type="button" onClick={resetForm}>
              Cancelar
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TaskForm;
```

### Passo 3: Atualizar o componente App principal

Substitua o conteúdo de `frontend/src/App.js`:

```javascript
import React, { useState } from 'react';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import './App.css';

function App() {
  const [selectedTask, setSelectedTask] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTaskSelected = (task) => {
    setSelectedTask(task);
  };

  const handleTaskSaved = () => {
    setSelectedTask(null);
    // Forçar a atualização da lista de tarefas
    setRefreshKey(oldKey => oldKey + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Gerenciador de Tarefas</h1>
        <p>Aplicação de exemplo com Flask + React</p>
      </header>
      
      <main className="app-content">
        <div className="form-container">
          <TaskForm 
            task={selectedTask} 
            onTaskSaved={handleTaskSaved} 
          />
        </div>
        
        <div className="list-container">
          <TaskList 
            key={refreshKey}
            onTaskSelected={handleTaskSelected}
            onTaskDeleted={() => setRefreshKey(oldKey => oldKey + 1)}
          />
        </div>
      </main>
      
      <footer className="app-footer">
        <p>Demonstração de comunicação entre Flask (backend) e React (frontend)</p>
      </footer>
    </div>
  );
}

export default App;
```

### Passo 4: Adicionar estilos CSS

Substitua o conteúdo de `frontend/src/App.css`:

```css
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.app-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.form-container,
.list-container {
  flex: 1;
  min-width: 300px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.task-form h2,
.task-list h2 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.task-list ul {
  list-style: none;
  padding: 0;
}

.task-list li {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 8px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.task-list li.completed span {
  text-decoration: line-through;
  color: #888;
}

.task-list li span {
  flex-grow: 1;
  margin: 0 10px;
  cursor: pointer;
}

.task-list li button {
  background-color: #f44336;
}

.task-list li button:hover {
  background-color: #d32f2f;
}

.error {
  color: #f44336;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #ffebee;
  border-radius: 4px;
}

.app-footer {
  margin-top: 30px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
  color: #666;
  font-size: 0.9em;
}
```

## Executando a Aplicação

Para executar a aplicação completa, você precisa iniciar tanto o backend quanto o frontend.

### Iniciando o Backend

```bash
# No diretório backend/
# Ative o ambiente virtual primeiro, se ainda não estiver ativado
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Execute o servidor Flask
python app.py
```

O servidor Flask será iniciado em http://localhost:5000.

### Iniciando o Frontend

Em uma nova janela de terminal:

```bash
# No diretório frontend/
npm start
```

O servidor de desenvolvimento do React será iniciado em http://localhost:3000.

### Testando a Aplicação

Abra http://localhost:3000 no seu navegador para interagir com a aplicação. Você deve ver:

1. Um formulário para adicionar tarefas
2. Uma lista das tarefas atuais
3. Opções para marcar tarefas como concluídas, editar ou excluir tarefas

## Resolvendo Problemas Comuns

### Erro de CORS

Se você encontrar erros de CORS, verifique se o Flask-CORS está configurado corretamente no backend:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas
```

### Alternativa usando Proxy

Outra forma de resolver problemas de CORS durante o desenvolvimento é configurar um proxy no React. Para isso, adicione a seguinte linha ao `package.json` no diretório `frontend/`:

```json
"proxy": "http://localhost:5000"
```

Em seguida, atualize o serviço de API para usar caminhos relativos:

```javascript
const api = axios.create({
  baseURL: '/api',  // Sem o domínio completo
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Erro de Conexão Recusada

Se o frontend não conseguir se conectar ao backend, verifique:

1. Se o servidor Flask está em execução
2. Se a porta 5000 está livre (não está sendo usada por outro processo)
3. Se a URL da API no frontend está correta

## Próximos Passos

Após implementar esta aplicação básica, você pode expandir com:

### Persistência de Dados

Substitua o array em memória por um banco de dados real:

```python
# Com SQLAlchemy e SQLite
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }
```

### Autenticação de Usuários

Adicione autenticação JWT para proteger a API:

```bash
# Instalar bibliotecas necessárias
pip install flask-jwt-extended
```

```python
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'chave-secreta-super-segura'  # Use uma chave segura em produção
jwt = JWTManager(app)

# Rota para login
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Verificar credenciais (em um sistema real, consulte banco de dados)
    if username != 'admin' or password != 'senha123':
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    # Criar token JWT
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Proteger rotas com JWT
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    # Código existente...
```

### Melhorias no Frontend

1. **Adicione Rotas para Navegação:**

```bash
npm install react-router-dom
```

2. **Implemente Gestão de Estado Global:**

```bash
npm install redux react-redux @reduxjs/toolkit
```

3. **Melhore a UI com uma Biblioteca de Componentes:**

```bash
npm install @mui/material @emotion/react @emotion/styled
# ou
npm install react-bootstrap bootstrap
```

## Conclusão

Parabéns! Você implementou com sucesso uma aplicação web completa que demonstra a comunicação entre um backend Flask e um frontend React. Esta aplicação serve como base para projetos mais complexos e pode ser expandida em várias direções.

Lembre-se de que boas práticas de desenvolvimento incluem:

- Manter o código organizado e modular
- Implementar tratamento adequado de erros
- Validar dados em ambas as pontas (frontend e backend)
- Proteger endpoints sensíveis
- Usar variáveis de ambiente para configurações

Feliz codificação! 