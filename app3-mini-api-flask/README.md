# Mini API com Flask Básico

Este projeto implementa uma API REST simples usando Flask, demonstrando conceitos fundamentais de desenvolvimento de APIs web.

## Funcionalidades

- API REST completa para gerenciar produtos
- Implementação de endpoints CRUD (Create, Read, Update, Delete)
- Respostas em formato JSON
- Simulação de banco de dados usando estruturas Python

## Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | /api/produtos | Listar todos os produtos |
| GET | /api/produtos/:id | Obter detalhes de um produto específico |
| POST | /api/produtos | Adicionar um novo produto |
| PUT | /api/produtos/:id | Atualizar um produto existente |
| DELETE | /api/produtos/:id | Remover um produto |

## Estrutura do Projeto

- `api.por`: Implementação em Portugol (simulação)
- `api.py`: Implementação em Python usando Flask
- `tutorial.md`: Tutorial passo a passo para iniciantes

## Como Executar

### Versão Python

1. Instale as dependências:
   ```
   pip install flask
   ```

2. Execute o servidor:
   ```
   python api.py
   ```

3. Acesse a API no navegador ou usando ferramentas como Postman:
   ```
   http://localhost:5000/api/produtos
   ```

### Versão Portugol

1. Abra o arquivo `api.por` no Portugol Studio
2. Execute o programa para iniciar a simulação da API

## Modelo de Dados

Cada produto possui os seguintes campos:
- `id`: Identificador único (inteiro)
- `nome`: Nome do produto (string)
- `preco`: Preço unitário (float)
- `estoque`: Quantidade em estoque (inteiro)
- `categoria`: Categoria do produto (string)

## Testando a API

### Com Navegador

Apenas para requisições GET:
- Acesse `http://localhost:5000/api/produtos` para listar todos os produtos
- Acesse `http://localhost:5000/api/produtos/1` para ver o produto com ID 1

### Com cURL

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
  -d '{"nome":"Mouse sem fio","preco":80.0,"estoque":15,"categoria":"Acessórios"}' \
  http://localhost:5000/api/produtos/1

# Excluir um produto
curl -X DELETE http://localhost:5000/api/produtos/1
```

## Próximos Passos

- Adicionar autenticação (JWT ou OAuth)
- Implementar validação de dados mais robusta
- Conectar a um banco de dados real (SQLite, PostgreSQL, etc.)
- Adicionar documentação com Swagger/OpenAPI
- Implementar paginação para grandes conjuntos de dados 