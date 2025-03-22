# Backend em Portugol

Este repositório contém projetos de backend implementados em Portugol, uma pseudo-linguagem de programação em português usada para fins educacionais. O objetivo é apresentar conceitos de desenvolvimento backend de forma mais acessível para falantes de português, similar ao que seria feito com Python (Flask, FastAPI, Django), mas usando Portugol.

## Sobre o Portugol

Portugol é uma linguagem estruturada com sintaxe em português, projetada para o ensino de lógica de programação. Embora seja mais simples que linguagens profissionais, ela é útil para entender os conceitos fundamentais da programação.

## Projetos Disponíveis

### 1. Servidor HTTP Básico (`app1-servidor-http`)

Um servidor HTTP simples implementado em Portugol, sem uso de frameworks. Este projeto demonstra:
- Como funciona um servidor HTTP basicamente
- Processamento de requisições GET e POST
- Roteamento de URLs
- Geração de respostas HTML

### 2. CRUD com Arquivos Locais (`app2-crud-arquivos`)

Um sistema CRUD (Create, Read, Update, Delete) que utiliza arquivos de texto para persistência de dados. Este projeto demonstra:
- Operações básicas de um banco de dados (CRUD)
- Armazenamento e leitura de dados em arquivos
- Interface de linha de comando para interação com usuário
- Estruturação de dados em memória

### 3. Mini API com Flask Básico (`app3-mini-api-flask`)

Uma API REST simples implementada usando o framework Flask. Este projeto demonstra:
- Construção de APIs web com o padrão REST
- Endpoints para operações CRUD de produtos
- Respostas em formato JSON
- Uso de diferentes métodos HTTP (GET, POST, PUT, DELETE)

## Como Executar os Projetos

Para executar os projetos, você precisará do [Portugol Studio](http://lite.acad.univali.br/portugol/) para as versões em Portugol, e Python 3.x para as versões em Python.

### Projetos em Portugol:
1. Baixe e instale o Portugol Studio
2. Abra o arquivo `.por` do projeto desejado
3. Execute o programa (F6 ou botão "Executar")

### Projetos em Python:
1. Instale as dependências necessárias (veja o README específico de cada projeto)
2. Execute o arquivo Python principal
3. Siga as instruções específicas de cada projeto

## Tutoriais Passo a Passo

Cada projeto inclui um tutorial detalhado passo a passo (`tutorial.md`) explicando como implementar a versão Python do projeto do zero. Estes tutoriais são ideais para iniciantes em desenvolvimento backend.

## Limitações

Por serem implementados em Portugol, estes projetos:
- São simulações e não criam serviços reais na rede
- Possuem funcionalidades limitadas comparadas a implementações profissionais
- São orientados ao aprendizado e não à produção

## Próximos Passos

Futuros projetos incluirão:
- API REST mais avançada com autenticação
- Integração com banco de dados relacional
- Templates e renderização de páginas
- WebSockets para comunicação em tempo real 