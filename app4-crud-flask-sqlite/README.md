# CRUD com Flask e SQLite

Este projeto implementa um aplicativo CRUD (Create, Read, Update, Delete) completo usando Flask e SQLite, demonstrando como criar uma aplicação web com armazenamento persistente de dados.

## Funcionalidades

- Interface web para gerenciamento de produtos
- API REST completa para integração com outros sistemas
- Operações CRUD: Criar, Ler, Atualizar e Excluir produtos
- Armazenamento persistente de dados com SQLite
- Formulários para adicionar e editar produtos

## Tecnologias Utilizadas

- **Flask**: Framework web em Python para criar a aplicação
- **SQLite**: Banco de dados relacional leve para armazenamento de dados
- **HTML/CSS**: Para interface de usuário
- **Jinja2**: Sistema de templates usado pelo Flask

## Estrutura do Projeto

- `crud.py`: Aplicativo principal com todas as rotas e lógica
- `templates/`: Diretório contendo os templates HTML
  - `index.html`: Página de listagem de produtos
  - `form.html`: Formulário para adicionar/editar produtos
- `produtos.db`: Banco de dados SQLite (criado automaticamente)

## Endpoints da API

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | /api/produtos | Listar todos os produtos |
| GET | /api/produtos/:id | Obter detalhes de um produto específico |
| POST | /api/produtos | Adicionar um novo produto |
| PUT | /api/produtos/:id | Atualizar um produto existente |
| DELETE | /api/produtos/:id | Remover um produto |

## Rotas da Interface Web

| URL | Descrição |
|-----|-----------|
| / | Página inicial com lista de produtos |
| /produtos/novo | Formulário para adicionar novo produto |
| /produtos/editar/:id | Formulário para editar produto existente |
| /produtos/excluir/:id | Rota para excluir produto |

## Como Executar

1. Instale as dependências:
   ```bash
   pip install flask
   ```

2. Execute a aplicação:
   ```bash
   python crud.py
   ```

3. Acesse a aplicação em:
   ```
   http://localhost:5000
   ```

## Modelo de Dados

Cada produto possui os seguintes campos:
- `id`: Identificador único (inteiro, chave primária)
- `nome`: Nome do produto (texto)
- `preco`: Preço unitário (float)
- `estoque`: Quantidade em estoque (inteiro)
- `categoria`: Categoria do produto (texto)

## Testando a API

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
  -d '{"nome":"Mouse sem fio","preco":80.0}' \
  http://localhost:5000/api/produtos/1

# Excluir um produto
curl -X DELETE http://localhost:5000/api/produtos/1
```

## Diferencial deste Projeto

Este projeto demonstra como integrar:
1. Uma interface web amigável para usuários finais
2. Uma API REST para integração com outros sistemas
3. Persistência de dados com banco de dados relacional
4. Validação de dados nas operações CRUD 