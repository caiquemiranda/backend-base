# Tutorial: Upload de Arquivos com Flask

Este tutorial irá guiá-lo na criação de um sistema completo de upload de arquivos usando Flask, com validação e gerenciamento dos arquivos enviados.

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
   pip install flask Pillow
   ```
   > Obs: Pillow é opcional, apenas se você for trabalhar com processamento de imagens.

## Passo 2: Estrutura de Diretórios

Crie a seguinte estrutura de diretórios:

```
app6-upload-arquivos-flask/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── upload_sucesso.html
│   ├── arquivos.html
│   └── visualizar.html
├── static/
│   └── style.css
└── uploads/
    # Este diretório armazenará os arquivos enviados
```

## Passo 3: Implementação Básica

### Arquivo Principal (app.py)

```python
import os
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Configuração
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limite

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'chave_secreta_para_mensagens_flash'  # Importante para flash messages

# Verifica se o diretório de uploads existe, senão cria
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Rota principal - exibe formulário de upload e lista de arquivos"""
    # Lista os arquivos no diretório de uploads
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Obtém metadados do arquivo
        size = os.path.getsize(file_path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        files.append({
            'name': filename,
            'size': size,
            'modified': mod_time,
            'url': url_for('download_file', filename=filename)
        })
    
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Rota para processar o upload de arquivos"""
    # Verifica se há arquivo na requisição
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Se o usuário não seleciona um arquivo, o navegador envia
    # um arquivo vazio sem nome
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))
    
    # Se o arquivo existe e tem extensão permitida
    if file and allowed_file(file.filename):
        # Garante um nome de arquivo seguro
        filename = secure_filename(file.filename)
        
        # Adiciona timestamp para evitar sobrescrita
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
        
        # Salva o arquivo no diretório de upload
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        flash(f'Arquivo {filename} enviado com sucesso!')
        return redirect(url_for('index'))
    else:
        flash('Tipo de arquivo não permitido')
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    """Rota para download/visualização de arquivo"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/arquivos')
def list_files():
    """Rota para listar todos os arquivos enviados"""
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Obtém metadados do arquivo
        size = os.path.getsize(file_path)
        size_kb = size / 1024  # Converte para KB
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        files.append({
            'name': filename,
            'size': f"{size_kb:.2f} KB",
            'modified': mod_time.strftime('%d/%m/%Y %H:%M'),
            'url': url_for('download_file', filename=filename),
            'delete_url': url_for('delete_file', filename=filename)
        })
    
    return render_template('arquivos.html', files=files)

@app.route('/excluir/<filename>')
def delete_file(filename):
    """Rota para excluir um arquivo"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Arquivo {filename} excluído com sucesso!')
    else:
        flash(f'Arquivo {filename} não encontrado')
    
    return redirect(url_for('list_files'))

@app.route('/visualizar/<filename>')
def view_file(filename):
    """Rota para visualizar arquivos (especialmente imagens)"""
    return render_template('visualizar.html', 
                          filename=filename, 
                          file_url=url_for('download_file', filename=filename))

if __name__ == '__main__':
    app.run(debug=True)
```

## Passo 4: Criando os Templates

### Template Base (templates/base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %} - Upload de Arquivos Flask</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{{ url_for('index') }}">Início</a></li>
                <li><a href="{{ url_for('list_files') }}">Lista de Arquivos</a></li>
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
        <p>Upload de Arquivos com Flask - Tutorial</p>
    </footer>
</body>
</html>
```

### Página Inicial (templates/index.html)

```html
{% extends 'base.html' %}

{% block title %}Início{% endblock %}

{% block content %}
    <h1>Upload de Arquivos</h1>
    
    <div class="upload-form">
        <form method="post" action="{{ url_for('upload_file') }}" enctype="multipart/form-data">
            <div class="form-group">
                <label for="file">Selecione um arquivo:</label>
                <input type="file" id="file" name="file" required>
                <p class="info">Tipos permitidos: .txt, .pdf, .png, .jpg, .jpeg, .gif (máx. 16MB)</p>
            </div>
            
            <div class="form-group">
                <button type="submit">Enviar Arquivo</button>
            </div>
        </form>
    </div>
    
    {% if files %}
        <h2>Arquivos recentes:</h2>
        <div class="files-list">
            <ul>
                {% for file in files %}
                    <li>
                        <a href="{{ file.url }}" target="_blank">{{ file.name }}</a>
                        <span class="file-info">{{ file.size }} bytes - {{ file.modified.strftime('%d/%m/%Y %H:%M') }}</span>
                    </li>
                {% endfor %}
            </ul>
            <p><a href="{{ url_for('list_files') }}" class="button">Ver todos os arquivos</a></p>
        </div>
    {% else %}
        <p>Nenhum arquivo enviado ainda.</p>
    {% endif %}
{% endblock %}
```

### Lista de Arquivos (templates/arquivos.html)

```html
{% extends 'base.html' %}

{% block title %}Lista de Arquivos{% endblock %}

{% block content %}
    <h1>Arquivos Enviados</h1>
    
    {% if files %}
        <div class="files-table">
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Tamanho</th>
                        <th>Modificado</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for file in files %}
                        <tr>
                            <td>{{ file.name }}</td>
                            <td>{{ file.size }}</td>
                            <td>{{ file.modified }}</td>
                            <td>
                                <a href="{{ file.url }}" class="button download" target="_blank">Baixar</a>
                                {% if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) %}
                                    <a href="{{ url_for('view_file', filename=file.name) }}" class="button view">Visualizar</a>
                                {% endif %}
                                <a href="{{ file.delete_url }}" class="button delete" onclick="return confirm('Tem certeza que deseja excluir este arquivo?')">Excluir</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <p>Nenhum arquivo enviado ainda.</p>
    {% endif %}
    
    <p><a href="{{ url_for('index') }}" class="button">Enviar novo arquivo</a></p>
{% endblock %}
```

### Visualizar Arquivo (templates/visualizar.html)

```html
{% extends 'base.html' %}

{% block title %}Visualizar {{ filename }}{% endblock %}

{% block content %}
    <h1>Visualizando: {{ filename }}</h1>
    
    <div class="file-viewer">
        {% if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) %}
            <img src="{{ file_url }}" alt="{{ filename }}">
        {% elif filename.lower().endswith('.txt') %}
            <iframe src="{{ file_url }}" width="100%" height="500px"></iframe>
        {% elif filename.lower().endswith('.pdf') %}
            <embed src="{{ file_url }}" type="application/pdf" width="100%" height="600px">
        {% else %}
            <p>Este tipo de arquivo não pode ser visualizado diretamente.</p>
            <a href="{{ file_url }}" class="button download">Baixar o arquivo</a>
        {% endif %}
    </div>
    
    <div class="actions">
        <a href="{{ file_url }}" class="button download" download>Baixar</a>
        <a href="{{ url_for('list_files') }}" class="button">Voltar para lista</a>
    </div>
{% endblock %}
```

### Página de Sucesso (templates/upload_sucesso.html)

```html
{% extends 'base.html' %}

{% block title %}Upload Concluído{% endblock %}

{% block content %}
    <h1>Upload Concluído com Sucesso!</h1>
    
    <div class="success-card">
        <p>Seu arquivo foi enviado e está disponível agora.</p>
        <p class="file-info">
            <strong>Nome:</strong> {{ filename }}<br>
            <strong>Tamanho:</strong> {{ filesize }} KB<br>
            <strong>Enviado em:</strong> {{ upload_time }}
        </p>
        
        <div class="actions">
            <a href="{{ file_url }}" class="button download" target="_blank">Baixar o arquivo</a>
            <a href="{{ url_for('index') }}" class="button">Enviar outro arquivo</a>
            <a href="{{ url_for('list_files') }}" class="button">Ver todos os arquivos</a>
        </div>
    </div>
{% endblock %}
```

## Passo 5: Estilização com CSS

### Arquivo CSS (static/style.css)

```css
/* Reset básico */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    padding-bottom: 60px; /* Espaço para o footer */
}

header, footer {
    background-color: #333;
    color: white;
    padding: 1rem;
}

footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
}

nav ul {
    list-style: none;
    display: flex;
}

nav ul li {
    margin-right: 20px;
}

nav ul li a {
    color: white;
    text-decoration: none;
}

nav ul li a:hover {
    text-decoration: underline;
}

main {
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
    background-color: white;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1, h2 {
    margin-bottom: 20px;
    color: #333;
}

/* Mensagens Flash */
.mensagens {
    margin-bottom: 20px;
}

.mensagem {
    padding: 10px;
    background-color: #d4edda;
    color: #155724;
    border-radius: 3px;
    margin-bottom: 10px;
}

/* Formulário de Upload */
.upload-form {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 5px;
    border: 1px solid #ddd;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="file"] {
    display: block;
    margin-bottom: 10px;
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
}

.info {
    font-size: 0.85em;
    color: #666;
    margin-top: 5px;
}

button, .button {
    display: inline-block;
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    text-decoration: none;
    font-size: 16px;
}

button:hover, .button:hover {
    background-color: #45a049;
}

/* Lista de Arquivos */
.files-list ul {
    list-style: none;
    margin-bottom: 20px;
}

.files-list li {
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.files-list li:last-child {
    border-bottom: none;
}

.file-info {
    display: block;
    font-size: 0.85em;
    color: #666;
    margin-top: 3px;
}

/* Tabela de Arquivos */
.files-table {
    width: 100%;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table th, table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

table th {
    background-color: #f2f2f2;
}

/* Botões de ação */
.button.download {
    background-color: #2196F3;
}

.button.download:hover {
    background-color: #0b7dda;
}

.button.view {
    background-color: #9c27b0;
}

.button.view:hover {
    background-color: #7B1FA2;
}

.button.delete {
    background-color: #f44336;
}

.button.delete:hover {
    background-color: #d32f2f;
}

/* Visualizador de arquivos */
.file-viewer {
    margin: 20px 0;
    text-align: center;
}

.file-viewer img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 3px;
}

.actions {
    margin-top: 20px;
}

/* Cartão de sucesso */
.success-card {
    padding: 20px;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    margin-bottom: 20px;
}

.success-card .file-info {
    margin: 15px 0;
    color: #155724;
}

/* Responsividade */
@media (max-width: 768px) {
    main {
        padding: 15px;
    }
    
    .button {
        display: block;
        width: 100%;
        margin-bottom: 10px;
        text-align: center;
    }
    
    table th, table td {
        padding: 8px 5px;
    }
}
```

## Passo 6: Upload de Múltiplos Arquivos (Extensão)

Para permitir upload de múltiplos arquivos, faça as seguintes alterações:

### Modificar o formulário (templates/index.html)

```html
<!-- Substitua o input de arquivo no index.html para permitir seleção múltipla -->
<div class="form-group">
    <label for="file">Selecione um ou mais arquivos:</label>
    <input type="file" id="file" name="file" multiple required>
    <p class="info">Tipos permitidos: .txt, .pdf, .png, .jpg, .jpeg, .gif (máx. 16MB)</p>
</div>
```

### Modificar a rota de upload (app.py)

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    """Rota para processar o upload de arquivos múltiplos"""
    # Verifica se há arquivo na requisição
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('index'))
    
    # Captura arquivos múltiplos
    files = request.files.getlist('file')
    
    # Verifica se algum arquivo foi selecionado
    if not files or files[0].filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))
    
    successful_uploads = 0
    for file in files:
        # Verifica extensão para cada arquivo
        if file and allowed_file(file.filename):
            # Garante um nome de arquivo seguro
            filename = secure_filename(file.filename)
            
            # Adiciona timestamp para evitar sobrescrita
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            
            # Salva o arquivo no diretório de upload
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            successful_uploads += 1
        else:
            flash(f'Arquivo "{file.filename}" tem tipo não permitido e foi ignorado')
    
    if successful_uploads > 0:
        flash(f'{successful_uploads} arquivo(s) enviado(s) com sucesso!')
    
    return redirect(url_for('index'))
```

## Passo 7: Processamento de Imagens (Opcional)

Se você instalou Pillow, pode adicionar processamento de imagens:

```python
from PIL import Image

# Adicione esta função ao app.py
def create_thumbnail(file_path, max_size=(200, 200)):
    """Cria uma miniatura para imagens"""
    # Obtém diretório e nome base do arquivo
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    thumb_filename = f"{name}_thumb{ext}"
    thumb_path = os.path.join(directory, thumb_filename)
    
    # Abre e redimensiona a imagem
    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size)
            img.save(thumb_path)
        return thumb_filename
    except Exception as e:
        print(f"Erro ao criar thumbnail: {e}")
        return None

# Modifique a função upload_file para processar imagens após o upload
# Dentro do bloco if para arquivos permitidos:
if file and allowed_file(file.filename):
    # ... código existente ...
    
    # Se for uma imagem, criar thumbnail
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        thumb_filename = create_thumbnail(file_path)
        if thumb_filename:
            # Você pode adicionar o caminho da miniatura ao banco de dados ou usar conforme necessário
            pass
```

## Passo 8: Executando a Aplicação

Execute o aplicativo com:

```bash
python app.py
```

Acesse http://127.0.0.1:5000/ no seu navegador para testar.

## Considerações de Segurança

1. **Validação de Arquivos**: Sempre verifique o tipo real do arquivo além da extensão.

2. **Limite de Tamanho**: Defina um tamanho máximo para prevenir ataques DoS.

3. **Nomes de Arquivo Seguros**: Use `secure_filename` para prevenir ataques de path traversal.

4. **Diretório de Upload**: Armazene arquivos fora da árvore pública, se possível.

5. **Varredura de Vírus**: Considere implementar varredura de malware em ambiente de produção.

## Expansões Possíveis

- **Autenticação de Usuários**: Restringir uploads para usuários autenticados.
- **Banco de Dados**: Armazenar metadados dos arquivos em um banco de dados.
- **Categorização**: Permitir categorizar arquivos por tipo ou finalidade.
- **Pesquisa**: Implementar busca nos arquivos enviados.
- **API REST**: Criar endpoints para upload via API.
- **Armazenamento em Nuvem**: Integrar com serviços como AWS S3 ou Google Cloud Storage.

---

Este tutorial abordou os fundamentos para criar um sistema de upload de arquivos completo com Flask. Você pode expandir essas funcionalidades de acordo com suas necessidades específicas. 