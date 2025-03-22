# Tutorial: Criando uma Mini API REST com Flask

## Introdução

Neste tutorial, vamos criar uma API REST simples usando o framework Flask do Python. Uma API (Interface de Programação de Aplicação) permite que diferentes softwares se comuniquem entre si, e REST (Transferência de Estado Representacional) é uma arquitetura popular para construir APIs web.

## Pré-requisitos

- Python 3.x instalado
- Conhecimentos básicos de Python
- Entendimento básico de HTTP e JSON

## Passo 1: Configurar o Ambiente

Primeiro, vamos instalar o Flask:

```bash
pip install flask
```

## Passo 2: Criar a Estrutura do Projeto

Crie um arquivo chamado `api.py` que conterá nosso código:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)
```

## Passo 3: Definir o Modelo de Dados

Vamos criar uma lista para simular um banco de dados de produtos:

```python
# Simulação de um banco de dados usando uma lista de dicionários
produtos = [
    {'id': 1, 'nome': 'Notebook', 'preco': 3500.0, 'estoque': 10, 'categoria': 'Eletrônicos'},
    {'id': 2, 'nome': 'Smartphone', 'preco': 1800.0, 'estoque': 15, 'categoria': 'Eletrônicos'},
    {'id': 3, 'nome': 'Fones de Ouvido', 'preco': 150.0, 'estoque': 30, 'categoria': 'Acessórios'},
    {'id': 4, 'nome': 'Mochila', 'preco': 120.0, 'estoque': 20, 'categoria': 'Acessórios'},
    {'id': 5, 'nome': 'Livro Python', 'preco': 85.0, 'estoque': 50, 'categoria': 'Livros'}
]

# Próximo ID para novos produtos
proximo_id = 6
```

## Passo 4: Criar a Rota Raiz

Vamos criar uma rota para a raiz da API que exibe uma mensagem de boas-vindas:

```python
@app.route('/')
def index():
    return jsonify({
        'mensagem': 'Bem-vindo à API de Produtos',
        'endpoints': [
            '/api/produtos',
            '/api/produtos/<id>'
        ]
    })
```

## Passo 5: Implementar a Listagem de Produtos (GET /api/produtos)

```python
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    # Opcionalmente filtrar por categoria
    categoria = request.args.get('categoria')
    
    if categoria:
        produtos_filtrados = [p for p in produtos if p['categoria'] == categoria]
        return jsonify(produtos_filtrados)
    
    return jsonify(produtos)
```

## Passo 6: Implementar a Busca de Produto por ID (GET /api/produtos/<id>)

```python
@app.route('/api/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    # Buscar o produto pelo ID
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if produto:
        return jsonify(produto)
    
    # Produto não encontrado
    return jsonify({'erro': 'Produto não encontrado'}), 404
```

## Passo 7: Implementar a Criação de Produto (POST /api/produtos)

```python
@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    global proximo_id
    
    # Obter dados da requisição
    dados = request.json
    
    # Validar campos obrigatórios
    if not dados or not all(campo in dados for campo in ['nome', 'preco', 'estoque', 'categoria']):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    # Criar novo produto
    novo_produto = {
        'id': proximo_id,
        'nome': dados['nome'],
        'preco': float(dados['preco']),
        'estoque': int(dados['estoque']),
        'categoria': dados['categoria']
    }
    
    # Adicionar à lista de produtos
    produtos.append(novo_produto)
    proximo_id += 1
    
    # Retornar o produto criado com status 201 (Created)
    return jsonify(novo_produto), 201
```

## Passo 8: Implementar a Atualização de Produto (PUT /api/produtos/<id>)

```python
@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    # Buscar o produto pelo ID
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Obter dados da requisição
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    # Atualizar campos do produto
    if 'nome' in dados:
        produto['nome'] = dados['nome']
    
    if 'preco' in dados:
        produto['preco'] = float(dados['preco'])
    
    if 'estoque' in dados:
        produto['estoque'] = int(dados['estoque'])
    
    if 'categoria' in dados:
        produto['categoria'] = dados['categoria']
    
    # Retornar o produto atualizado
    return jsonify(produto)
```

## Passo 9: Implementar a Exclusão de Produto (DELETE /api/produtos/<id>)

```python
@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    global produtos
    
    # Verificar se o produto existe
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Remover o produto da lista
    produtos = [p for p in produtos if p['id'] != id]
    
    # Retornar resposta sem conteúdo (204 No Content)
    return '', 204
```

## Passo 10: Implementar Tratamento de Erros

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500
```

## Passo 11: Iniciar o Servidor

```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Passo 12: Código Completo

Juntando todos os trechos, nosso arquivo `api.py` completo fica assim:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulação de um banco de dados usando uma lista de dicionários
produtos = [
    {'id': 1, 'nome': 'Notebook', 'preco': 3500.0, 'estoque': 10, 'categoria': 'Eletrônicos'},
    {'id': 2, 'nome': 'Smartphone', 'preco': 1800.0, 'estoque': 15, 'categoria': 'Eletrônicos'},
    {'id': 3, 'nome': 'Fones de Ouvido', 'preco': 150.0, 'estoque': 30, 'categoria': 'Acessórios'},
    {'id': 4, 'nome': 'Mochila', 'preco': 120.0, 'estoque': 20, 'categoria': 'Acessórios'},
    {'id': 5, 'nome': 'Livro Python', 'preco': 85.0, 'estoque': 50, 'categoria': 'Livros'}
]

# Próximo ID para novos produtos
proximo_id = 6

@app.route('/')
def index():
    return jsonify({
        'mensagem': 'Bem-vindo à API de Produtos',
        'endpoints': [
            '/api/produtos',
            '/api/produtos/<id>'
        ]
    })

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    # Opcionalmente filtrar por categoria
    categoria = request.args.get('categoria')
    
    if categoria:
        produtos_filtrados = [p for p in produtos if p['categoria'] == categoria]
        return jsonify(produtos_filtrados)
    
    return jsonify(produtos)

@app.route('/api/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    # Buscar o produto pelo ID
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if produto:
        return jsonify(produto)
    
    # Produto não encontrado
    return jsonify({'erro': 'Produto não encontrado'}), 404

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    global proximo_id
    
    # Obter dados da requisição
    dados = request.json
    
    # Validar campos obrigatórios
    if not dados or not all(campo in dados for campo in ['nome', 'preco', 'estoque', 'categoria']):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    # Criar novo produto
    novo_produto = {
        'id': proximo_id,
        'nome': dados['nome'],
        'preco': float(dados['preco']),
        'estoque': int(dados['estoque']),
        'categoria': dados['categoria']
    }
    
    # Adicionar à lista de produtos
    produtos.append(novo_produto)
    proximo_id += 1
    
    # Retornar o produto criado com status 201 (Created)
    return jsonify(novo_produto), 201

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    # Buscar o produto pelo ID
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Obter dados da requisição
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    # Atualizar campos do produto
    if 'nome' in dados:
        produto['nome'] = dados['nome']
    
    if 'preco' in dados:
        produto['preco'] = float(dados['preco'])
    
    if 'estoque' in dados:
        produto['estoque'] = int(dados['estoque'])
    
    if 'categoria' in dados:
        produto['categoria'] = dados['categoria']
    
    # Retornar o produto atualizado
    return jsonify(produto)

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    global produtos
    
    # Verificar se o produto existe
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Remover o produto da lista
    produtos = [p for p in produtos if p['id'] != id]
    
    # Retornar resposta sem conteúdo (204 No Content)
    return '', 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Passo 13: Executar a API

Salve o arquivo `api.py` e execute-o:

```bash
python api.py
```

Você verá uma saída indicando que o servidor está rodando, geralmente em `http://127.0.0.1:5000/`.

## Passo 14: Testar a API

### Usando o Navegador

Para rotas GET:
- Abra `http://127.0.0.1:5000/` para ver a mensagem de boas-vindas
- Abra `http://127.0.0.1:5000/api/produtos` para listar todos os produtos
- Abra `http://127.0.0.1:5000/api/produtos/1` para ver um produto específico
- Abra `http://127.0.0.1:5000/api/produtos?categoria=Eletrônicos` para filtrar por categoria

### Usando cURL

Para testar todos os métodos HTTP:

```bash
# Listar produtos
curl http://localhost:5000/api/produtos

# Obter produto específico
curl http://localhost:5000/api/produtos/1

# Adicionar produto
curl -X POST -H "Content-Type: application/json" \
  -d '{"nome":"Mouse","preco":50.0,"estoque":20,"categoria":"Acessórios"}' \
  http://localhost:5000/api/produtos

# Atualizar produto
curl -X PUT -H "Content-Type: application/json" \
  -d '{"nome":"Mouse sem fio","preco":80.0}' \
  http://localhost:5000/api/produtos/6

# Excluir produto
curl -X DELETE http://localhost:5000/api/produtos/6
```

## Explicação do Código

1. **Configuração inicial**:
   - Importamos as classes necessárias do Flask
   - Criamos uma instância da aplicação Flask

2. **Modelo de dados**:
   - Usamos uma lista de dicionários para simular um banco de dados
   - Cada produto tem uma estrutura definida (id, nome, preço, etc.)

3. **Roteamento**:
   - Definimos rotas para diferentes endpoints
   - Cada rota está associada a uma função específica

4. **Métodos HTTP**:
   - GET: Para buscar informações (listar produtos, obter produto)
   - POST: Para criar novos recursos (adicionar produto)
   - PUT: Para atualizar recursos existentes (atualizar produto)
   - DELETE: Para remover recursos (excluir produto)

5. **Respostas JSON**:
   - Todas as respostas são formatadas como JSON
   - Incluímos códigos de status HTTP apropriados

## Próximos Passos

Depois de concluir este tutorial básico, você pode aprimorar sua API:

1. **Conectar a um banco de dados real** (SQLite, MySQL, PostgreSQL)
2. **Adicionar autenticação** usando JWT ou Flask-Login
3. **Implementar validação mais robusta** dos dados de entrada
4. **Adicionar documentação** usando Swagger/OpenAPI
5. **Implementar paginação** para lidar com grandes conjuntos de dados
6. **Criar uma estrutura de projeto** mais organizada com blueprints

## Conclusão

Parabéns! Você criou uma API REST completa com Flask. Este é um excelente primeiro passo para entender como as APIs funcionam e como podem ser utilizadas para comunicação entre diferentes sistemas. 