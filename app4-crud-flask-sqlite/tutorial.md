# Tutorial: Criando um CRUD com Flask e SQLite

## Introdução

Neste tutorial, vamos criar um aplicativo CRUD (Create, Read, Update, Delete) completo usando Flask e SQLite. O aplicativo permitirá gerenciar produtos através de uma interface web e também fornecerá uma API REST para integração com outros sistemas.

## Pré-requisitos

- Python 3.x instalado
- Conhecimentos básicos de Python, HTML e SQL
- Entendimento básico de HTTP e APIs web

## Passo 1: Configurar o Ambiente

Primeiro, vamos instalar o Flask:

```bash
pip install flask
```

## Passo 2: Criar a Estrutura do Projeto

Vamos criar a seguinte estrutura de diretórios:

```
app4-crud-flask-sqlite/
  ├── crud.py
  ├── produtos.db (será criado automaticamente)
  └── templates/
      ├── index.html
      └── form.html
```

## Passo 3: Configurar o Aplicativo Flask e o Banco de Dados

Vamos criar o arquivo principal `crud.py` com a configuração do Flask e do SQLite:

```python
from flask import Flask, jsonify, request, render_template, redirect, url_for
import sqlite3
import os

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados
DB_PATH = "produtos.db"

# Função para criar a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Função para inicializar o banco de dados
def init_db():
    if os.path.exists(DB_PATH):
        print("Banco de dados já existe.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL,
        categoria TEXT NOT NULL
    )
    ''')
    
    produtos_exemplo = [
        ('Notebook', 3500.0, 10, 'Eletrônicos'),
        ('Smartphone', 1800.0, 15, 'Eletrônicos'),
        ('Fones de Ouvido', 150.0, 30, 'Acessórios'),
        ('Mochila', 120.0, 20, 'Acessórios'),
        ('Livro Python', 85.0, 50, 'Livros')
    ]
    
    cursor.executemany(
        'INSERT INTO produtos (nome, preco, estoque, categoria) VALUES (?, ?, ?, ?)',
        produtos_exemplo
    )
    
    conn.commit()
    conn.close()
    
    print("Banco de dados inicializado com sucesso!")
```

Aqui estamos:
1. Importando os módulos necessários
2. Inicializando o aplicativo Flask
3. Definindo o caminho do banco de dados SQLite
4. Criando funções auxiliares para conectar ao banco e inicializá-lo

## Passo 4: Criar as Rotas e Funções da API

Vamos adicionar as funções para a API REST que permitirão interagir com os produtos:

```python
# API - Listar todos os produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    categoria = request.args.get('categoria')
    conn = get_db_connection()
    
    if categoria:
        produtos = conn.execute(
            'SELECT * FROM produtos WHERE categoria = ?', 
            (categoria,)
        ).fetchall()
    else:
        produtos = conn.execute('SELECT * FROM produtos').fetchall()
    
    conn.close()
    
    return jsonify([dict(produto) for produto in produtos])

# API - Obter produto por ID
@app.route('/api/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    return jsonify(dict(produto))

# API - Adicionar novo produto
@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.json
    
    # Validar campos obrigatórios
    if not dados or not all(campo in dados for campo in ['nome', 'preco', 'estoque', 'categoria']):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO produtos (nome, preco, estoque, categoria) VALUES (?, ?, ?, ?)',
        (dados['nome'], float(dados['preco']), int(dados['estoque']), dados['categoria'])
    )
    
    produto_id = cursor.lastrowid
    conn.commit()
    
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(produto)), 201

# API - Atualizar produto existente
@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if produto is None:
        conn.close()
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    campos_atualizacao = []
    valores = []
    
    if 'nome' in dados:
        campos_atualizacao.append('nome = ?')
        valores.append(dados['nome'])
    
    if 'preco' in dados:
        campos_atualizacao.append('preco = ?')
        valores.append(float(dados['preco']))
    
    if 'estoque' in dados:
        campos_atualizacao.append('estoque = ?')
        valores.append(int(dados['estoque']))
    
    if 'categoria' in dados:
        campos_atualizacao.append('categoria = ?')
        valores.append(dados['categoria'])
    
    if not campos_atualizacao:
        conn.close()
        return jsonify({'erro': 'Nenhum campo para atualizar'}), 400
    
    valores.append(id)
    
    conn.execute(
        f'UPDATE produtos SET {", ".join(campos_atualizacao)} WHERE id = ?',
        valores
    )
    conn.commit()
    
    produto_atualizado = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify(dict(produto_atualizado))

# API - Excluir produto
@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if produto is None:
        conn.close()
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'mensagem': f'Produto {id} excluído com sucesso'})
```

Estas funções implementam os endpoints da API para:
- Listar todos os produtos (com opção de filtrar por categoria)
- Obter um produto específico por ID
- Adicionar um novo produto
- Atualizar um produto existente
- Excluir um produto

## Passo 5: Criar as Rotas e Funções da Interface Web

Agora, vamos adicionar as funções para a interface web:

```python
# Rota principal - página inicial
@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

# Rota para formulário de adicionar produto
@app.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        categoria = request.form['categoria']
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO produtos (nome, preco, estoque, categoria) VALUES (?, ?, ?, ?)',
            (nome, preco, estoque, categoria)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('form.html', titulo='Novo Produto', produto=None)

# Rota para formulário de editar produto
@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if produto is None:
        conn.close()
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        categoria = request.form['categoria']
        
        conn.execute(
            'UPDATE produtos SET nome = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?',
            (nome, preco, estoque, categoria, id)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('form.html', titulo='Editar Produto', produto=dict(produto))

# Rota para excluir produto (interface web)
@app.route('/produtos/excluir/<int:id>')
def excluir_produto_web(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))
```

Estas funções implementam:
- A página inicial que lista todos os produtos
- Um formulário para adicionar novos produtos
- Um formulário para editar produtos existentes
- Uma rota para excluir produtos

## Passo 6: Adicionar o Código para Iniciar o Aplicativo

Finalmente, adicionamos o código para inicializar o banco de dados e iniciar o servidor:

```python
# Ponto de entrada para execução do aplicativo
if __name__ == '__main__':
    # Inicializa o banco de dados se necessário
    init_db()
    
    # Inicia o servidor Flask
    app.run(debug=True)
```

## Passo 7: Criar os Templates HTML

### Template index.html

Crie o arquivo `templates/index.html` para mostrar a lista de produtos:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Produtos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Estilos omitidos para brevidade */
    </style>
</head>
<body>
    <h1>Gerenciador de Produtos</h1>
    
    <a href="{{ url_for('novo_produto') }}" class="btn">Adicionar Novo Produto</a>
    
    {% if produtos %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Preço</th>
                    <th>Estoque</th>
                    <th>Categoria</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for produto in produtos %}
                <tr>
                    <td>{{ produto.id }}</td>
                    <td>{{ produto.nome }}</td>
                    <td>R$ {{ "%.2f"|format(produto.preco) }}</td>
                    <td>{{ produto.estoque }}</td>
                    <td>{{ produto.categoria }}</td>
                    <td class="actions">
                        <a href="{{ url_for('editar_produto', id=produto.id) }}" class="btn btn-info">Editar</a>
                        <a href="{{ url_for('excluir_produto_web', id=produto.id) }}" 
                           class="btn btn-danger" 
                           onclick="return confirm('Tem certeza que deseja excluir este produto?');">
                            Excluir
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="empty-message">
            <p>Nenhum produto cadastrado.</p>
        </div>
    {% endif %}
</body>
</html>
```

### Template form.html

Crie o arquivo `templates/form.html` para adicionar e editar produtos:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }} - Gerenciador de Produtos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Estilos omitidos para brevidade */
    </style>
</head>
<body>
    <h1>{{ titulo }}</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="nome">Nome do Produto:</label>
            <input type="text" id="nome" name="nome" required
                   value="{% if produto %}{{ produto.nome }}{% endif %}">
        </div>
        
        <!-- Outros campos do formulário omitidos para brevidade -->
        
        <div class="actions">
            <button type="submit" class="btn">Salvar</button>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</body>
</html>
```

## Passo 8: Executar o Aplicativo

Para executar o aplicativo, basta rodar o arquivo `crud.py`:

```bash
python crud.py
```

O servidor Flask iniciará em modo de desenvolvimento e poderá ser acessado em `http://localhost:5000`.

## Testando o Aplicativo

### Interface Web

1. Acesse `http://localhost:5000` no navegador para ver a lista de produtos
2. Clique em "Adicionar Novo Produto" para criar um produto
3. Clique em "Editar" ao lado de um produto para modificá-lo
4. Clique em "Excluir" para remover um produto

### API REST

Você pode testar a API usando ferramentas como cURL, Postman ou até mesmo um navegador:

```bash
# Listar todos os produtos
curl http://localhost:5000/api/produtos

# Obter um produto específico
curl http://localhost:5000/api/produtos/1

# Criar um novo produto
curl -X POST -H "Content-Type: application/json" \
  -d '{"nome":"Mouse","preco":50.0,"estoque":20,"categoria":"Acessórios"}' \
  http://localhost:5000/api/produtos

# Atualizar um produto
curl -X PUT -H "Content-Type: application/json" \
  -d '{"nome":"Mouse sem fio","preco":80.0}' \
  http://localhost:5000/api/produtos/1

# Excluir um produto
curl -X DELETE http://localhost:5000/api/produtos/1
```

## Conclusão

Parabéns! Você criou um aplicativo CRUD completo com Flask e SQLite que fornece tanto uma interface web quanto uma API REST. Este é um bom ponto de partida para aplicativos web mais complexos.

## Próximos Passos

Algumas melhorias que você pode adicionar ao projeto:

1. Adicionar autenticação de usuários
2. Melhorar a validação de dados
3. Implementar paginação para grandes conjuntos de dados
4. Adicionar suporte para upload de imagens de produtos
5. Criar testes automatizados
6. Refatorar o código em uma estrutura modular (por exemplo, usando Blueprints do Flask)
7. Adicionar documentação de API com Swagger/OpenAPI 