# CRUD Completo com FastAPI, React e SQLite

Este projeto demonstra a implementação de um sistema CRUD (Create, Read, Update, Delete) completo usando FastAPI para o backend, React para o frontend e SQLite como banco de dados.

## Visão Geral

O projeto consiste em uma aplicação web para gerenciamento de itens, permitindo ao usuário:
- Visualizar uma lista de itens
- Ver detalhes de um item específico
- Criar novos itens
- Editar itens existentes
- Excluir itens
- Marcar itens como concluídos/pendentes

A aplicação implementa todas as operações CRUD e serve como um exemplo prático de como integrar tecnologias modernas para construir um sistema web completo.

## Funcionalidades

- **API REST completa**: Implementa todos os endpoints necessários para operações CRUD
- **ORM SQLAlchemy**: Abstração do banco de dados SQLite
- **Validação de dados**: Com Pydantic no backend e React Hook Form no frontend
- **Interface responsiva**: UI moderna com Material-UI
- **Roteamento no frontend**: Navegação fluida entre páginas
- **Gerenciamento de estado**: Manipulação eficiente de estado nos componentes React
- **Feedback de usuário**: Respostas visuais para ações, incluindo loading, sucesso e erro
- **Organização por prioridade**: Itens podem ser categorizados por nível de prioridade
- **Documentação automática**: API documentada automaticamente via Swagger UI

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e de alto desempenho para APIs
- **SQLAlchemy**: ORM (Object-Relational Mapping) para operações com banco de dados
- **Pydantic**: Validação de dados e serialização
- **SQLite**: Banco de dados leve e sem servidor
- **Uvicorn**: Servidor ASGI para execução da aplicação FastAPI

### Frontend
- **React**: Biblioteca JavaScript para construção de interfaces de usuário
- **React Router**: Navegação entre páginas
- **React Hook Form**: Gerenciamento e validação de formulários
- **Material-UI**: Framework de componentes React para design de interface
- **Axios**: Cliente HTTP para comunicação com a API

## Estrutura do Projeto

```
app12-crud-fastapi-react-sqlite/
├── app.py                   # Arquivo com comentários detalhados sobre a implementação
├── README.md                # Este arquivo
├── tutorial.md              # Tutorial passo a passo
├── backend/                 # Código do servidor FastAPI
│   ├── app/                 # Módulo da aplicação
│   │   ├── __init__.py
│   │   ├── crud/            # Funções de operações CRUD
│   │   ├── database.py      # Configuração do banco de dados
│   │   ├── main.py          # Aplicação FastAPI principal
│   │   ├── models/          # Modelos SQLAlchemy
│   │   └── schemas/         # Esquemas Pydantic
│   ├── requirements.txt     # Dependências do backend
│   └── sqlite.db            # Banco de dados SQLite
└── frontend/                # Código da aplicação React
    ├── public/              # Arquivos estáticos
    ├── src/                 # Código-fonte
    │   ├── components/      # Componentes React reutilizáveis
    │   ├── pages/           # Páginas da aplicação
    │   ├── services/        # Serviços para comunicação com API
    │   ├── App.js           # Componente principal
    │   └── index.js         # Ponto de entrada
    └── package.json         # Dependências do frontend
```

## Conteúdo do Projeto

Este projeto inclui três arquivos principais para documentação e aprendizagem:

1. **app.py**: Contém comentários detalhados que explicam os conceitos e implementações do projeto, servindo como um guia abrangente para entender o código.

2. **tutorial.md**: Um tutorial passo a passo que guia o leitor pela criação do projeto do zero, explicando cada parte do processo.

3. **README.md**: Este arquivo, que fornece uma visão geral do projeto, suas funcionalidades e tecnologias.

## Conceitos Abordados

- **Arquitetura REST**: Implementação de API RESTful com recursos e verbos HTTP
- **Padrão MVC**: Separação de modelos, visualizações e controladores
- **Validação em camadas**: Validação no frontend e backend
- **Operações CRUD**: Criação, leitura, atualização e exclusão de recursos
- **Single Page Application**: Navegação sem recarregamento de página
- **Componentização**: Separação da UI em componentes reutilizáveis
- **ORM**: Mapeamento objeto-relacional para interação com banco de dados
- **Async/Await**: Programação assíncrona moderna para lidar com operações de I/O

## Pré-requisitos

Para executar este projeto, você precisará:

- **Python 3.7+**
- **Node.js 12+**
- **npm ou yarn**
- **Editor de código** (VS Code, PyCharm, etc.)

## Como Executar

### Backend

```bash
# Navegar para o diretório do backend
cd backend

# Criar e ativar ambiente virtual (opcional, mas recomendado)
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python -m app.main
```

O servidor FastAPI estará disponível em `http://localhost:8000`, e a documentação da API estará em `http://localhost:8000/docs`.

### Frontend

```bash
# Navegar para o diretório do frontend
cd frontend

# Instalar dependências
npm install

# Iniciar o servidor de desenvolvimento
npm start
```

O aplicativo React estará disponível em `http://localhost:3000`.

## API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET    | /api/items/ | Listar todos os itens |
| GET    | /api/items/{item_id} | Obter um item específico |
| POST   | /api/items/ | Criar um novo item |
| PUT    | /api/items/{item_id} | Atualizar um item existente |
| DELETE | /api/items/{item_id} | Excluir um item |

## Modelo de Dados

**Item**
- `id`: Integer (Chave primária)
- `title`: String (Título do item)
- `description`: Text (Descrição opcional)
- `priority`: Integer (Prioridade de 1 a 5)
- `completed`: Boolean (Status de conclusão)
- `created_at`: DateTime (Data de criação)
- `updated_at`: DateTime (Data da última atualização)

## Próximos Passos

Ideias para expandir o projeto:

- **Autenticação de usuários**: Implementar login e registro
- **Filtros e ordenação**: Permitir filtragem e ordenação de itens
- **Paginação**: Adicionar suporte para conjuntos grandes de dados
- **Pesquisa**: Implementar funcionalidade de busca
- **Categorias/Tags**: Adicionar categorização de itens
- **Relatórios**: Gerar estatísticas e visualizações
- **Testes**: Adicionar testes unitários e de integração
- **CI/CD**: Configurar pipeline de integração e entrega contínua
- **Deployment**: Instruções para publicação em produção

## Uso como Template

Este projeto pode ser usado como ponto de partida para novos projetos. Para usar como template:

1. Clone o repositório
2. Personalize os modelos no backend para atender às suas necessidades
3. Adapte os componentes do frontend para sua interface desejada
4. Expanda as funcionalidades conforme necessário

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou correções.

## Licença

Este projeto é destinado a fins educacionais. 