# Tutorial: Autenticação Simples com Flask

Este tutorial irá guiá-lo na criação de um sistema de autenticação simples usando Flask.

## Pré-requisitos

Certifique-se de ter instalado:
- Python 3.x
- pip (gerenciador de pacotes Python)

## Passo 1: Configuração do Ambiente

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Instale as dependências:
   ```bash
   pip install flask werkzeug
   ```

## Passo 2: Estrutura de Diretórios

Crie a seguinte estrutura de diretórios:

```
app5-autenticacao-flask/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Passo 3: Implementação Básica

### Configuração da Aplicação (app.py)

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'  # Substitua por uma chave segura em produção

# Simulação de banco de dados de usuários (em produção, use um banco de dados real)
usuarios = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('senha123'),
        'nome': 'Administrador'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## Passo 4: Criação dos Templates

### Template Base (templates/base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %} - Autenticação Flask</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{{ url_for('index') }}">Início</a></li>
                {% if 'usuario_logado' in session %}
                    <li><a href="{{ url_for('dashboard') }}">Painel</a></li>
                    <li><a href="{{ url_for('logout') }}">Sair</a></li>
                {% else %}
                    <li><a href="{{ url_for('login') }}">Entrar</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>
    
    <main>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="mensagens">
                    {% for message in messages %}
                        <div class="mensagem">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>Autenticação Simples com Flask - Tutorial</p>
    </footer>
</body>
</html>
```

### Página Inicial (templates/index.html)

```html
{% extends 'base.html' %}

{% block title %}Início{% endblock %}

{% block content %}
    <h1>Bem-vindo ao Sistema de Autenticação</h1>
    
    {% if 'usuario_logado' in session %}
        <p>Você está logado como {{ session['usuario_logado'] }}.</p>
        <p><a href="{{ url_for('dashboard') }}">Acesse seu painel</a></p>
    {% else %}
        <p>Por favor, <a href="{{ url_for('login') }}">faça login</a> para acessar o sistema.</p>
    {% endif %}
{% endblock %}
```

### Página de Login (templates/login.html)

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
    <h1>Login</h1>
    
    <form method="post">
        <div class="form-group">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div class="form-group">
            <button type="submit">Entrar</button>
        </div>
    </form>
{% endblock %}
```

### Dashboard (templates/dashboard.html)

```html
{% extends 'base.html' %}

{% block title %}Painel{% endblock %}

{% block content %}
    <h1>Painel do Usuário</h1>
    
    <div class="card">
        <h2>Bem-vindo, {{ usuario.nome }}</h2>
        <p>Nome de usuário: {{ usuario.username }}</p>
    </div>
    
    <p><a href="{{ url_for('logout') }}">Sair</a></p>
{% endblock %}
```

## Passo 5: Adicionar Estilo CSS

### Arquivo CSS (static/style.css)

```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
}

header, footer {
    background: #333;
    color: white;
    padding: 1rem;
}

nav ul {
    list-style: none;
    display: flex;
    padding: 0;
}

nav ul li {
    margin-right: 1rem;
}

nav ul li a {
    color: white;
    text-decoration: none;
}

main {
    max-width: 800px;
    margin: 20px auto;
    padding: 0 20px;
}

.mensagens {
    margin-bottom: 1rem;
}

.mensagem {
    padding: 10px;
    background: #f8d7da;
    color: #721c24;
    border-radius: 3px;
    margin-bottom: 5px;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
}

button {
    background: #333;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
}

.card {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1rem;
    margin-bottom: 1rem;
}
```

## Passo 6: Implementação da Autenticação

Adicione as seguintes rotas ao arquivo app.py:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            session['usuario_logado'] = username
            flash('Login realizado com sucesso!')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_logado' not in session:
        flash('Por favor, faça login para acessar esta página.')
        return redirect(url_for('login'))
    
    usuario = usuarios[session['usuario_logado']]
    return render_template('dashboard.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Você saiu do sistema.')
    return redirect(url_for('index'))
```

## Passo 7: Proteção de Rotas com Decorador

Adicione um decorador para simplificar a proteção de rotas:

```python
from functools import wraps

def requer_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session:
            flash('Por favor, faça login para acessar esta página.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Exemplo de uso:
@app.route('/area_protegida')
@requer_login
def area_protegida():
    return render_template('area_protegida.html')
```

## Passo 8: Executando a Aplicação

Execute a aplicação usando o comando:

```bash
python app.py
```

Acesse http://127.0.0.1:5000/ no seu navegador para testar.

## Credenciais de Teste

- Usuário: admin
- Senha: senha123

## Observações de Segurança

Em um ambiente de produção:

1. Use uma chave secreta forte para app.secret_key
2. Armazene usuários em um banco de dados seguro
3. Implemente proteção contra ataques de força bruta
4. Considere usar Flask-Login para gerenciamento mais robusto de autenticação
5. Implemente HTTPS para proteger as credenciais durante a transmissão
6. Implemente recuperação de senha e outras funcionalidades essenciais

## Próximos Passos

- Implementar cadastro de usuários
- Adicionar níveis de permissão (admin, usuário comum, etc.)
- Implementar autenticação com JWT para APIs
- Integrar com OAuth para login via redes sociais 