# APP5 - Autenticação Simples com Flask

## Visão Geral

Este projeto demonstra como implementar um sistema de autenticação simples usando Flask, um microframework web para Python. O sistema inclui funcionalidades de login, logout e acesso a áreas protegidas.

## Funcionalidades

- Login de usuários
- Sessões de usuário
- Proteção de rotas para usuários autenticados
- Logout
- Hash seguro de senhas
- Sistema de mensagens flash para feedback ao usuário

## Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **Werkzeug**: Biblioteca para hash de senhas
- **Jinja2**: Engine de templates (integrada ao Flask)
- **HTML/CSS**: Frontend

## Estrutura do Projeto

```
app5-autenticacao-flask/
├── app.py                 # Arquivo principal com comentários explicativos
├── tutorial.md            # Instruções passo a passo detalhadas
├── README.md              # Este arquivo
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial
│   ├── login.html         # Página de login
│   └── dashboard.html     # Painel do usuário (área protegida)
└── static/                # Arquivos estáticos
    └── style.css          # Estilos CSS
```

## Como Executar

1. Certifique-se de ter Python 3.x instalado
2. Siga as instruções detalhadas no arquivo `tutorial.md`

## Conceitos Abordados

- **Autenticação de Usuários**: Verificação de credenciais
- **Sessões**: Manutenção do estado do usuário entre requisições
- **Hashing de Senhas**: Armazenamento seguro de senhas
- **Proteção de Rotas**: Restrição de acesso a usuários não autenticados
- **Decoradores em Flask**: Simplificação da proteção de rotas

## Segurança

Este projeto é uma demonstração educacional. Em um ambiente de produção, considere:

- Implementar bancos de dados reais para armazenamento de usuários
- Utilizar chaves secretas fortes e variáveis de ambiente
- Implementar proteção contra ataques comuns (CSRF, XSS, etc.)
- Usar HTTPS para transmissão segura de dados

## Aprendizado

Este projeto serve como uma introdução à autenticação web e ajuda a entender:

1. O fluxo de autenticação em aplicações web
2. Como Flask gerencia sessões de usuário
3. Boas práticas de segurança para senhas
4. Organização de código em aplicações Flask

## Próximos Passos

- Cadastro de novos usuários
- Recuperação de senha
- Diferentes níveis de acesso (admin, usuário, etc.)
- Integração com banco de dados (SQLite, PostgreSQL, etc.)
- Implementação de autenticação por token para APIs

## Autor

Este projeto foi criado como material educacional para o curso de desenvolvimento backend.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes. 