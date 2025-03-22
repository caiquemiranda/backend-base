#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ====================================================================
# SERVIDOR HTTP BÁSICO COM PYTHON PURO (SEM FRAMEWORKS)
# ====================================================================

# Importar bibliotecas necessárias
# ----------------------------------------------------------------------
# socket: Para comunicação de rede
# threading: Para lidar com múltiplas conexões simultâneas
# datetime: Para gerar timestamps
# os, sys: Para operações do sistema


# Definir constantes
# ----------------------------------------------------------------------
# PORTA: Porta onde o servidor irá escutar (por exemplo, 8080)
# HOST: Endereço onde o servidor irá escutar (127.0.0.1 para localhost ou '' para todas interfaces)
# DIRETORIO_RAIZ: Diretório onde os arquivos estáticos estão (se aplicável)
# TAMANHO_BUFFER: Tamanho do buffer para receber dados (ex: 1024, 4096 bytes)
# CODIFICACAO: UTF-8 para manipulação de texto em requisições/respostas


# Definir mapeamento de tipos MIME
# ----------------------------------------------------------------------
# Criar um dicionário para mapear extensões de arquivo para tipos MIME
# Exemplos:
# '.html': 'text/html'
# '.css': 'text/css'
# '.js': 'application/javascript'
# '.jpg': 'image/jpeg'
# '.png': 'image/png'


# Definir códigos de status HTTP
# ----------------------------------------------------------------------
# Criar um dicionário para mapear códigos de status HTTP para suas descrições
# Exemplos:
# 200: 'OK'
# 404: 'Not Found'
# 500: 'Internal Server Error'


# Classe para manipular requisições HTTP
# ----------------------------------------------------------------------
# Criar uma classe para representar uma requisição HTTP:
#   - Método (GET, POST, etc.)
#   - Caminho da URL solicitada
#   - Versão do protocolo HTTP
#   - Cabeçalhos
#   - Corpo da requisição (para POST)
#
# Incluir método para analisar (parse) os dados da requisição bruta


# Classe para gerar respostas HTTP
# ----------------------------------------------------------------------
# Criar uma classe para representar uma resposta HTTP:
#   - Código de status (200, 404, etc.)
#   - Cabeçalhos
#   - Corpo da resposta
#
# Incluir método para gerar a resposta HTTP completa formatada


# Classe do servidor HTTP
# ----------------------------------------------------------------------
# Criar a classe principal do servidor que:
#   1. Inicializa o socket do servidor
#   2. Aceita conexões de clientes
#   3. Gerencia múltiplas conexões usando threads
#   4. Direciona requisições para os manipuladores apropriados


# Funções para manipular diferentes tipos de requisições
# ----------------------------------------------------------------------
# Implementar funções para diferentes caminhos e métodos:
#
# 1. Função para manipular requisição GET para a raiz ("/"):
#    - Retornar uma página HTML simples de boas-vindas
#
# 2. Função para servir arquivos estáticos (se aplicável):
#    - Verificar se o arquivo existe
#    - Determinar o tipo MIME com base na extensão
#    - Ler o conteúdo do arquivo
#    - Retornar com cabeçalhos apropriados
#
# 3. Função para manipular requisição POST (por exemplo, para "/submit"):
#    - Extrair dados do corpo da requisição
#    - Processar os dados conforme necessário
#    - Retornar uma resposta apropriada


# Funções auxiliares
# ----------------------------------------------------------------------
# 1. Função para analisar a linha de requisição HTTP:
#    - Extrair método, caminho e versão
#
# 2. Função para analisar cabeçalhos HTTP:
#    - Extrair nomes e valores dos cabeçalhos
#
# 3. Função para analisar parâmetros de consulta (query string):
#    - Extrair parâmetros e valores da URL
#
# 4. Função para analisar dados de formulário:
#    - Extrair campos e valores de dados de formulário
#
# 5. Função para gerar log:
#    - Registrar detalhes das requisições e respostas


# Função principal para iniciar o servidor
# ----------------------------------------------------------------------
# Implementar função que:
#   1. Cria uma instância do servidor
#   2. Define o manipulador de sinal para encerramento elegante
#   3. Inicia o servidor para escutar conexões
#   4. Mostra mensagem informando que o servidor está rodando
#   5. Entra em loop para manter o servidor ativo


# Bloco de execução principal
# ----------------------------------------------------------------------
# Verificar se o script está sendo executado diretamente
# Caso positivo, chamar a função principal para iniciar o servidor
# Incluir tratamento de exceções para encerramento elegante


# Exemplo de implementação real:
# 
# ```python
# if __name__ == "__main__":
#    try:
#        print("Iniciando servidor HTTP na porta 8080...")
#        print("Pressione Ctrl+C para encerrar")
#        iniciar_servidor()
#    except KeyboardInterrupt:
#        print("\nServidor encerrado pelo usuário")
#    except Exception as e:
#        print(f"Erro: {e}")
# ``` 