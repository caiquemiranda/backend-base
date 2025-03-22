# CRUD com Arquivos Locais em Portugol

Este projeto implementa um sistema CRUD (Create, Read, Update, Delete) em Portugol utilizando arquivos locais para persistência de dados.

## Funcionalidades

- **C**reate: Adicionar novos itens
- **R**ead: Listar todos os itens ou buscar por ID
- **U**pdate: Atualizar itens existentes
- **D**elete: Excluir itens

## Como executar

Para executar este sistema, você precisa de um interpretador de Portugol. Recomendamos o [Portugol Studio](http://lite.acad.univali.br/portugol/).

1. Abra o arquivo `crud.por` no Portugol Studio
2. Clique no botão "Executar" ou pressione F6
3. Use o menu interativo para navegar pelo sistema

## Estrutura de dados

Cada item no sistema possui os seguintes campos:
- ID (inteiro único)
- Nome (texto)
- Descrição (texto)
- Data de criação (texto no formato DD/MM/AAAA)

## Persistência de dados

Os dados são armazenados em um arquivo texto chamado `dados.txt` no seguinte formato:
```
ID|Nome|Descrição|Data
```

Exemplo:
```
1|Notebook|Computador portátil|15/03/2025
2|Mouse|Dispositivo de entrada|16/03/2025
```

## Estrutura do código

O código está organizado em seções:
- Definição de constantes e estruturas de dados
- Menu principal e interface com usuário
- Implementação das operações CRUD
- Funções auxiliares
- Operações de arquivo (salvar/carregar dados)

## Limitações

- Capacidade máxima de 100 itens
- Interface de linha de comando simples
- Não possui validação avançada de dados
- Não suporta operações de busca complexas 