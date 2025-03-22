# CRUD com FastAPI e SQLite

Este projeto demonstra como implementar operações CRUD (Create, Read, Update, Delete) utilizando FastAPI com SQLite como banco de dados, criando uma API REST completa e bem estruturada.

## Visão Geral

Este projeto exemplifica a construção de uma API moderna para gerenciar tarefas (todo list), implementando todas as operações CRUD com FastAPI e SQLite. O código segue boas práticas de desenvolvimento, incluindo estrutura modular, validação de dados, documentação automática e manipulação de erros.

## Funcionalidades

- **Operações CRUD completas**: Criar, ler, atualizar e excluir recursos
- **Validação de dados**: Verificação automática de entradas usando Pydantic
- **ORM**: Abstração do banco de dados com SQLAlchemy
- **Documentação interativa**: Swagger UI/ReDoc geradas automaticamente
- **Estrutura modular**: Código organizado em módulos reutilizáveis
- **Manipulação de erros**: Respostas de erro padronizadas
- **Paginação**: Suporte para listar grandes conjuntos de dados
- **Design orientado a recursos**: API RESTful bem estruturada

## Tecnologias Utilizadas

- **FastAPI**: Framework web de alta performance para construção de APIs
- **SQLite**: Banco de dados embutido, leve e de fácil configuração
- **SQLAlchemy**: ORM (Object-Relational Mapping) para abstração do banco de dados
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI de alto desempenho
- **Python Type Hints**: Tipagem estática para melhor documentação e autocomplete

## Estrutura do Projeto

O projeto segue uma arquitetura organizada em camadas:

```
app9-crud-fastapi-sqlite/
├── app.py              # Arquivo com comentários detalhados 
├── tutorial.md         # Tutorial passo a passo de implementação
└── README.md           # Este arquivo (visão geral do projeto)
```

O tutorial propõe a seguinte estrutura para uma implementação real:

```
fastapi-sqlite-crud/
├── app/
│   ├── __init__.py
│   ├── main.py         # Ponto de entrada da aplicação
│   ├── database.py     # Configuração do banco de dados
│   ├── models/         # Modelos SQLAlchemy (tabelas)
│   ├── schemas/        # Schemas Pydantic (validação)
│   ├── crud/           # Operações de acesso ao banco
│   └── api/            # Endpoints da API
│       ├── endpoints/  # Rotas específicas por recurso
└── venv/               # Ambiente virtual
```

## Conceitos Abordados

1. **Arquitetura por Camadas**:
   - **Camada de API**: Rotas HTTP e manipulação de requisições
   - **Camada de Serviço**: Lógica de negócios
   - **Camada de Acesso a Dados**: Interação com banco de dados

2. **Padrões REST**:
   - Uso adequado de métodos HTTP (GET, POST, PUT, DELETE)
   - Respostas com códigos de status apropriados
   - Formatação consistente de respostas

3. **Injeção de Dependências**:
   - Uso do sistema de dependências do FastAPI para injetar a sessão do banco de dados

4. **Migrations e Gestão de Banco de Dados** (opcional):
   - Manutenção do esquema do banco usando Alembic

## Como Usar o Projeto

Este projeto educacional fornece:

1. Um arquivo `app.py` com comentários detalhados sobre a implementação
2. Um arquivo `tutorial.md` com instruções passo a passo
3. Este `README.md` com uma visão geral do projeto

Para implementar o projeto completo, siga o tutorial detalhado e utilize os conceitos explicados nos comentários.

## Aprendizados

Ao estudar este projeto, você adquirirá conhecimentos sobre:

- Implementação eficiente de APIs RESTful com FastAPI
- Integração de ORM com bancos de dados relacionais
- Validação e serialização de dados com Pydantic
- Estruturação de projetos escaláveis em Python
- Documentação automática de APIs
- Tratamento adequado de erros e exceções
- Teste de APIs

## Exemplo de Uso

Após implementar o projeto, você poderá executá-lo com:

```bash
uvicorn app.main:app --reload
```

E testar a API em:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Próximos Passos

Depois de dominar este projeto básico, você pode expandir com:

- Implementação de autenticação (JWT, OAuth2)
- Relacionamentos entre múltiplas tabelas
- Testes automatizados (pytest)
- Cache para melhorar performance
- Deploy em ambientes de produção (Docker, Kubernetes)
- Implementação de filas de tarefas assíncronas

## Licença

Este projeto é disponibilizado para fins educacionais. 