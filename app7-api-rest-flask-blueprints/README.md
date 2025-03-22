# API REST com Flask e Blueprints

Este projeto demonstra como construir uma API REST organizada e escalável usando Flask e o sistema de Blueprints para modularização do código.

## Visão Geral

Este projeto implementa uma API RESTful em Python com Flask, organizada usando o padrão de Blueprints para separar diferentes recursos da API em módulos reutilizáveis e bem estruturados.

A API fornece endpoints para gerenciar usuários e produtos (simulados), demonstrando boas práticas de design, validação de dados, tratamento de erros e documentação.

## Funcionalidades

- **Sistema de Blueprints**: Organização modular de código para diferentes recursos da API
- **Operações CRUD completas**: Implementação de endpoints para Create, Read, Update, Delete
- **Validação de Dados**: Verificação de dados de entrada usando schemas
- **Tratamento de Erros Padronizado**: Sistema unificado de resposta para diferentes tipos de erros
- **Paginação, Filtros e Ordenação**: Recursos avançados para listar grandes conjuntos de dados
- **Autenticação JWT** (opcional): Sistema de autenticação seguro baseado em tokens
- **Documentação OpenAPI/Swagger** (opcional): Interface para visualizar e testar endpoints
- **Padrão Factory**: Configuração flexível baseada em diferentes ambientes

## Tecnologias Utilizadas

- **Flask**: Framework web leve e flexível
- **SQLAlchemy**: ORM para interação com banco de dados
- **Marshmallow**: Biblioteca para serialização/desserialização e validação
- **Flask-JWT-Extended** (opcional): Gerenciamento de tokens JWT
- **Flask-Swagger-UI** (opcional): Interface para documentação da API
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

## Estrutura do Projeto

```
app7-api-rest-flask-blueprints/
├── app/
│   ├── __init__.py           # Inicialização da aplicação (Factory Pattern)
│   ├── config.py             # Configurações para diferentes ambientes
│   ├── models/               # Modelos de dados
│   ├── api/                  # Organização dos endpoints da API
│   │   ├── __init__.py       # Blueprint principal da API
│   │   ├── users/            # Endpoints relacionados a usuários
│   │   └── products/         # Endpoints relacionados a produtos
│   ├── utils/                # Funções utilitárias
│   └── schemas/              # Schemas para validação e serialização
├── run.py                    # Script para execução da aplicação
├── .env                      # Variáveis de ambiente
└── .gitignore                # Arquivos a serem ignorados pelo Git
```

## Instalação e Execução

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure as variáveis de ambiente (ou crie um arquivo `.env`)
6. Execute a aplicação:
   ```bash
   python run.py
   ```

## Uso da API

### Endpoints Básicos

- `GET /api/v1/users`: Lista todos os usuários
- `GET /api/v1/users/<id>`: Obtém um usuário específico
- `POST /api/v1/users`: Cria um novo usuário
- `PUT /api/v1/users/<id>`: Atualiza um usuário existente
- `DELETE /api/v1/users/<id>`: Remove um usuário

### Autenticação (se implementada)

- `POST /api/v1/auth/login`: Autenticação de usuário
- `GET /api/v1/auth/me`: Informações do usuário autenticado

## Conceitos Abordados

- **Arquitetura Orientada a Recursos**: Organização da API em torno de recursos
- **Padrões REST**: Uso correto de métodos HTTP e códigos de status
- **Versionamento de API**: Estrutura para suportar múltiplas versões
- **Serialização/Desserialização**: Conversão entre objetos Python e formatos de transferência
- **Tratamento de Erros**: Respostas padronizadas para diferentes tipos de erro
- **Segurança**: Proteção de rotas e validação de entradas

## Segurança

Este projeto implementa várias medidas de segurança:
- Validação de dados de entrada
- Hashing de senhas
- Autenticação via tokens (opcional)
- Manipulação segura de exceções

## Aprendizados

Ao estudar e implementar este projeto, você aprenderá:
- Como estruturar APIs Flask para aplicações de médio/grande porte
- Organização modular de código com blueprints
- Técnicas de validação de dados de entrada
- Implementação de autenticação segura
- Documentação de API

## Próximos Passos

Ideias para expandir o projeto:
- Testes automatizados
- Sistema de permissões (RBAC)
- Implementação de cache
- Logging avançado
- Deploy em ambiente de produção

## Autor e Licença

Projeto desenvolvido para fins educacionais.
Licenciado sob MIT. 