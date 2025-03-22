#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ====================================================================
# MINI API COM FLASK BÁSICO
# ====================================================================

# Importar bibliotecas necessárias
# ----------------------------------------------------------------------
# flask: Framework web para Python
# flask_restful: Extensão para criar APIs RESTful com Flask
# jsonify: Para converter dados Python em JSON
# request: Para acessar dados da requisição
# datetime: Para manipular datas e horários


# Definir constantes e configurações
# ----------------------------------------------------------------------
# PORTA: Porta onde a API irá rodar (por exemplo, 5000)
# DEBUG: Modo de depuração para desenvolvimento (True/False)
# HOST: Endereço onde a API irá escutar (127.0.0.1 para localhost ou '0.0.0.0' para todas interfaces)


# Definir estrutura de dados para produtos
# ----------------------------------------------------------------------
# Criar uma classe ou dicionário para representar um produto com os campos:
# - id: identificador único
# - nome: nome do produto
# - preco: preço do produto
# - estoque: quantidade em estoque
# - categoria: categoria do produto


# Inicializar o banco de dados simulado
# ----------------------------------------------------------------------
# Criar uma lista de produtos para simular um banco de dados
# Adicionar alguns produtos iniciais para teste
# Definir variável para controlar o próximo ID


# Inicializar a aplicação Flask
# ----------------------------------------------------------------------
# Criar uma instância do Flask
# Configurar a aplicação (modo de depuração, etc.)
# Inicializar a extensão Flask-RESTful (opcional)


# Definir rota raiz
# ----------------------------------------------------------------------
# Criar uma rota para a raiz ("/") que retorna informações sobre a API
# Exemplo:
# @app.route('/')
# def index():
#     return jsonify({
#         'mensagem': 'Bem-vindo à API de Produtos',
#         'endpoints': ['/api/produtos', '/api/produtos/<id>']
#     })


# Implementar endpoints para produtos (todos)
# ----------------------------------------------------------------------
# Criar rota para /api/produtos que suporta:
# - GET: listar todos os produtos
# - POST: adicionar novo produto
#
# Para o método GET:
# - Retornar lista de todos os produtos ativos
# - Opcionalmente implementar filtragem por categoria
#
# Para o método POST:
# - Validar dados recebidos (todos os campos obrigatórios estão presentes?)
# - Adicionar o produto ao "banco de dados"
# - Retornar o produto criado com status 201 (Created)


# Implementar endpoints para produto específico (por ID)
# ----------------------------------------------------------------------
# Criar rota para /api/produtos/<id> que suporta:
# - GET: obter detalhes de um produto específico
# - PUT: atualizar um produto existente
# - DELETE: remover um produto
#
# Para o método GET:
# - Buscar o produto pelo ID
# - Se encontrado, retornar os detalhes
# - Se não encontrado, retornar erro 404
#
# Para o método PUT:
# - Buscar o produto pelo ID
# - Se encontrado, atualizar os campos com os dados recebidos
# - Retornar o produto atualizado
#
# Para o método DELETE:
# - Buscar o produto pelo ID
# - Se encontrado, removê-lo ou marcá-lo como inativo
# - Retornar status 204 (No Content)


# Implementar funções auxiliares
# ----------------------------------------------------------------------
# Função para buscar produto por ID
# Função para validar dados do produto
# Função para formatar resposta de erro


# Adicionar tratamento de erros
# ----------------------------------------------------------------------
# Implementar handlers para erros comuns (404, 500, etc.)
# Exemplo:
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({'erro': 'Recurso não encontrado'}), 404


# Iniciar o servidor
# ----------------------------------------------------------------------
# Verificar se o script está sendo executado diretamente
# Iniciar o servidor Flask com as configurações definidas


# Exemplo de implementação real:
#
# ```python
# from flask import Flask, jsonify, request
# 
# app = Flask(__name__)
# 
# # Simulação de banco de dados
# produtos = [
#     {'id': 1, 'nome': 'Notebook', 'preco': 3500.0, 'estoque': 10, 'categoria': 'Eletrônicos'},
#     {'id': 2, 'nome': 'Smartphone', 'preco': 1800.0, 'estoque': 15, 'categoria': 'Eletrônicos'},
#     {'id': 3, 'nome': 'Fones de Ouvido', 'preco': 150.0, 'estoque': 30, 'categoria': 'Acessórios'}
# ]
# proximo_id = 4
# 
# @app.route('/api/produtos', methods=['GET'])
# def listar_produtos():
#     return jsonify(produtos)
# 
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
# ```


# Testando a API:
# ----------------------------------------------------------------------
# Para testar a API, você pode usar:
# 1. Navegador web (apenas para rotas GET)
# 2. Ferramentas como Postman ou Insomnia
# 3. Curl via linha de comando
# 4. Biblioteca requests do Python
#
# Exemplos de testes com curl:
#
# # Listar todos os produtos
# curl http://localhost:5000/api/produtos
#
# # Obter um produto específico
# curl http://localhost:5000/api/produtos/1
#
# # Criar um novo produto
# curl -X POST -H "Content-Type: application/json" -d '{"nome":"Mouse","preco":50.0,"estoque":20,"categoria":"Acessórios"}' http://localhost:5000/api/produtos
#
# # Atualizar um produto
# curl -X PUT -H "Content-Type: application/json" -d '{"nome":"Mouse sem fio","preco":80.0,"estoque":15,"categoria":"Acessórios"}' http://localhost:5000/api/produtos/4
#
# # Excluir um produto
# curl -X DELETE http://localhost:5000/api/produtos/4 