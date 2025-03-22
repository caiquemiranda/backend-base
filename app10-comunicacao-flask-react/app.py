# Comunicação entre Backend (Flask) e Frontend (React)
# Autor: Claude
# Data: Março/2025

# 1. INTRODUÇÃO E CONCEITOS BÁSICOS
# Este arquivo apresenta os conceitos fundamentais para estabelecer comunicação
# entre uma API REST construída com Flask (backend) e uma aplicação React (frontend).
# A comunicação é baseada em requisições HTTP e respostas JSON.

# 2. CONFIGURAÇÃO DO AMBIENTE
# Para este projeto, precisamos das seguintes dependências:
# 
# Backend (Flask):
# - Flask: Framework web para Python
# - Flask-CORS: Para habilitar CORS (Cross-Origin Resource Sharing)
# - Flask-RESTful: Para facilitar a criação de APIs REST
# 
# Instalação:
# pip install flask flask-cors flask-restful
#
# Frontend (React):
# - Node.js e npm: Para gerenciar pacotes e executar o React
# - React: Biblioteca JavaScript para interfaces de usuário
# - Axios: Biblioteca para fazer requisições HTTP
#
# Instalação:
# npx create-react-app frontend
# cd frontend
# npm install axios

# 3. ESTRUTURA DO PROJETO
# Este projeto seguirá a seguinte estrutura:
#
# app10-comunicacao-flask-react/
# ├── backend/                    # Código do servidor Flask
# │   ├── app.py                  # Aplicação Flask principal
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

# 4. BACKEND COM FLASK
# O backend será responsável por fornecer uma API REST que o frontend consumirá.
# Vamos implementar operações básicas e configurar o CORS para permitir requisições
# do frontend.

"""
# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Habilitando CORS para todas as rotas - em produção, você deve restringir as origens
CORS(app)

# Dados de exemplo (em um projeto real, usaríamos um banco de dados)
tasks = [
    {"id": 1, "title": "Aprender Flask", "completed": True},
    {"id": 2, "title": "Aprender React", "completed": False},
    {"id": 3, "title": "Integrar Flask com React", "completed": False}
]

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
"""

# 5. FRONTEND COM REACT
# O frontend será uma aplicação React que se comunica com o backend para
# exibir, criar, atualizar e excluir tarefas. Vamos usar o Axios para fazer
# as requisições HTTP.

# 5.1 Configuração do serviço de API
# Primeiro, vamos criar um serviço para encapsular a comunicação com a API:

"""
// frontend/src/services/api.js
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
"""

# 5.2 Componente para listar tarefas
# Agora, vamos criar um componente para exibir a lista de tarefas:

"""
// frontend/src/components/TaskList.js
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
"""

# 5.3 Componente para criar/editar tarefas
# Agora, vamos criar um componente para adicionar ou editar tarefas:

"""
// frontend/src/components/TaskForm.js
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
"""

# 5.4 Componente principal da aplicação
# Finalmente, vamos criar o componente principal que integra os outros componentes:

"""
// frontend/src/App.js
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
"""

# 6. ESTILOS CSS BÁSICOS
# Para melhorar a aparência da aplicação, vamos adicionar alguns estilos básicos:

"""
/* frontend/src/App.css */
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
"""

# 7. EXECUÇÃO DO PROJETO
# Para executar o projeto, você precisa iniciar tanto o backend quanto o frontend:
#
# Backend (pasta backend):
# python app.py
# Isso iniciará o servidor Flask em http://localhost:5000
#
# Frontend (pasta frontend):
# npm start
# Isso iniciará o servidor de desenvolvimento do React em http://localhost:3000

# 8. DESAFIOS COMUNS E SOLUÇÕES
# 
# 8.1. CORS (Cross-Origin Resource Sharing)
# O problema mais comum ao integrar Flask e React é o CORS. O navegador bloqueia
# requisições de uma origem para outra por questões de segurança. Para resolver isso,
# usamos Flask-CORS conforme mostrado no exemplo do backend.
#
# 8.2. Proxy para Desenvolvimento
# Uma alternativa ao CORS é configurar um proxy no frontend. Para isso, adicione ao
# arquivo package.json do React:
#
# "proxy": "http://localhost:5000",
#
# Isso permite que você faça requisições sem a necessidade de especificar o domínio
# completo, por exemplo:
# fetch('/api/tasks') em vez de fetch('http://localhost:5000/api/tasks')
#
# 8.3. Gestão de Estado no React
# Em aplicações maiores, considere usar Redux ou Context API para gerenciar o estado
# global da aplicação.
#
# 8.4. Autenticação
# Para adicionar autenticação, você pode usar JWT (JSON Web Tokens) ou OAuth2.
# O backend gera tokens que o frontend armazena e envia em requisições subsequentes.

# 9. BOAS PRÁTICAS
# 
# 9.1. Separação de Responsabilidades
# - Backend: Lógica de negócios, acesso a dados, autenticação
# - Frontend: Interface de usuário, validação client-side, gerenciamento de estado
#
# 9.2. Tratamento de Erros
# - No backend: Retorne códigos de status HTTP apropriados
# - No frontend: Capture e exiba erros de forma amigável ao usuário
#
# 9.3. Validação em Ambas as Pontas
# - Sempre valide os dados no backend (obrigatório)
# - Também valide no frontend para melhorar a experiência do usuário
#
# 9.4. Organização do Código
# - Use uma estrutura de diretórios lógica tanto no backend quanto no frontend
# - Separe componentes, serviços e utilitários em arquivos diferentes
#
# 9.5. Variáveis de Ambiente
# - Use variáveis de ambiente para configurações (URLs, chaves de API, etc.)
# - No Flask: python-dotenv
# - No React: arquivo .env (com prefixo REACT_APP_)

# 10. PRÓXIMOS PASSOS
# 
# 10.1. Implementação de Autenticação
# - Adicionar login/registro de usuários
# - Proteger rotas no backend com JWT
# - Adicionar páginas de login/registro no frontend
#
# 10.2. Persistência de Dados
# - Substituir o array em memória por um banco de dados (SQLite, PostgreSQL, MongoDB)
# - Adicionar relacionamentos entre entidades (ex: tarefas pertencentes a usuários)
#
# 10.3. Funcionalidades Avançadas
# - Filtros e ordenação de tarefas
# - Sistema de categorias ou etiquetas
# - Upload de anexos
# - Notificações em tempo real
#
# 10.4. Deploy
# - Backend: Heroku, AWS, Google Cloud, etc.
# - Frontend: Netlify, Vercel, GitHub Pages, etc.
# - Configuração para produção (variáveis de ambiente, otimizações, etc.)

# 11. CONCLUSÃO
# Este projeto demonstra a comunicação básica entre um backend Flask e um frontend React.
# Através de requisições HTTP e respostas JSON, estabelecemos uma arquitetura cliente-servidor
# que permite a criação de aplicações web modernas e escaláveis.
# 
# Lembre-se de que este é apenas um ponto de partida. À medida que sua aplicação cresce,
# você pode adicionar mais funcionalidades, refatorar o código e adotar padrões mais
# avançados para atender às necessidades específicas do seu projeto. 