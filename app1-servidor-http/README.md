# Servidor HTTP Básico em Portugol

Este projeto implementa um servidor HTTP básico usando apenas Portugol, sem frameworks externos. É uma implementação educacional para entender os conceitos de um servidor web.

## Funcionalidades

- Servidor HTTP que atende requisições GET e POST
- Roteamento básico para diferentes caminhos
- Geração de respostas HTML
- Simulação de cabeçalhos HTTP

## Como executar

Para executar este servidor, você precisa de um interpretador de Portugol. Recomendamos o [Portugol Studio](http://lite.acad.univali.br/portugol/).

1. Abra o arquivo `servidor.por` no Portugol Studio
2. Clique no botão "Executar" ou pressione F6
3. O servidor iniciará na porta 8080 (simulada)

## Endpoints disponíveis

- `GET /`: Página inicial
- `GET /pagina`: Página de exemplo
- `POST /enviar`: Endpoint para receber dados

## Estrutura do código

- Definição de tipos para Requisição e Resposta
- Funções para iniciar o servidor
- Funções para processar requisições
- Simulação do ciclo de vida de um servidor HTTP

## Como funciona

Este servidor é uma simulação para fins educacionais. Ele não estabelece conexões reais de rede, mas demonstra o fluxo lógico de um servidor HTTP:

1. Receber requisição
2. Analisar método e caminho
3. Processar a requisição
4. Gerar uma resposta apropriada
5. Enviar a resposta

## Limitações

Por ser implementado em Portugol e para fins didáticos, este servidor:
- Não estabelece conexões reais de rede
- Simula requisições aleatórias para demonstrar o funcionamento
- Tem recursos limitados comparados a servidores reais 