#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ====================================================================
# CRUD COM ARQUIVOS LOCAIS (SEM BANCO DE DADOS)
# ====================================================================

# Importar bibliotecas necessárias
# ----------------------------------------------------------------------
# os: Para operações do sistema de arquivos
# json: Para serializar/deserializar dados em formato JSON
# datetime: Para manipular datas e horários
# uuid: Para gerar identificadores únicos
# re: Para validações com expressões regulares (opcional)
# sys: Para acesso a argumentos de linha de comando e saída do programa


# Definir constantes
# ----------------------------------------------------------------------
# ARQUIVO_DADOS: Nome do arquivo onde os dados serão armazenados (ex: 'dados.json')
# ENCODING: Codificação para leitura/escrita de arquivos (ex: 'utf-8')
# CAMPO_ID: Nome do campo que será usado como identificador único (ex: 'id')
# CAMPOS_OBRIGATORIOS: Lista de campos que devem estar presentes em cada item


# Classe para representar um item
# ----------------------------------------------------------------------
# Criar uma classe para representar um item a ser armazenado:
#   - id: identificador único
#   - nome: nome do item
#   - descricao: descrição detalhada
#   - data_criacao: data de criação do item (gerada automaticamente)
#   - outros campos conforme necessário
#
# Incluir métodos para:
#   - Validar os dados do item
#   - Converter para dicionário (para serialização)
#   - Criar a partir de dicionário (para deserialização)


# Classe para operações CRUD
# ----------------------------------------------------------------------
# Criar a classe principal para gerenciar as operações CRUD:
#
# 1. Inicialização:
#    - Verificar se o arquivo de dados existe
#    - Criar o arquivo se não existir
#    - Carregar dados iniciais
#
# 2. Métodos para operações CRUD:
#    - CREATE: Adicionar novo item
#    - READ: Buscar todos os itens ou item específico por ID
#    - UPDATE: Atualizar item existente
#    - DELETE: Remover item
#
# 3. Métodos para persistência:
#    - Salvar todos os dados no arquivo
#    - Carregar dados do arquivo


# Classe para interface de linha de comando
# ----------------------------------------------------------------------
# Criar uma classe para gerenciar a interface com o usuário:
#
# 1. Inicialização:
#    - Criar instância do gerenciador CRUD
#
# 2. Métodos para o menu principal:
#    - Exibir menu de opções
#    - Processar escolha do usuário
#    - Chamar funções específicas para cada operação
#
# 3. Métodos para cada operação:
#    - Exibir formulário para adicionar item
#    - Exibir lista de itens
#    - Exibir formulário de busca por ID
#    - Exibir formulário para atualizar item
#    - Exibir confirmação para excluir item
#
# 4. Métodos auxiliares:
#    - Limpar tela
#    - Formatar saída de dados
#    - Validar entrada do usuário


# Funções auxiliares
# ----------------------------------------------------------------------
# 1. Função para limpar a tela do terminal (compatível com diferentes sistemas):
#    - Windows: 'cls'
#    - Unix/Linux/MacOS: 'clear'
#
# 2. Função para validar entrada do usuário:
#    - Verificar se é numérico quando necessário
#    - Validar formatos específicos (e-mail, data, etc.)
#
# 3. Função para formatar datas:
#    - Converter entre objetos datetime e strings
#
# 4. Função para gerar um ID único:
#    - Usar UUID ou incrementar contador


# Função principal para iniciar o programa
# ----------------------------------------------------------------------
# Implementar função que:
#   1. Cria uma instância da interface de linha de comando
#   2. Inicia o loop do menu principal
#   3. Trata exceções para encerramento elegante


# Bloco de execução principal
# ----------------------------------------------------------------------
# Verificar se o script está sendo executado diretamente
# Caso positivo, chamar a função principal para iniciar o programa
# Incluir tratamento de exceções para encerramento elegante


# Exemplo de implementação real:
#
# ```python
# if __name__ == "__main__":
#     try:
#         print("Iniciando Sistema CRUD com Arquivos Locais")
#         sistema = SistemaCRUD()
#         sistema.iniciar()
#     except KeyboardInterrupt:
#         print("\nPrograma encerrado pelo usuário")
#     except Exception as e:
#         print(f"Erro: {e}")
# ```


# Exemplos de possíveis melhorias futuras:
# ----------------------------------------------------------------------
# 1. Implementar busca por texto em campos específicos
# 2. Adicionar filtros e ordenação na listagem
# 3. Implementar validação mais rigorosa de dados
# 4. Adicionar autenticação simples para operações
# 5. Adicionar exportação para CSV ou outro formato
# 6. Implementar backup automático do arquivo de dados
# 7. Adicionar suporte para relacionamentos entre entidades
# 8. Implementar interface web simples usando Flask 