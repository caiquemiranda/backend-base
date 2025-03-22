# CRUD com Flask e SQLite
# Este arquivo contém orientações para criar um aplicativo CRUD completo
# utilizando Flask e SQLite como banco de dados

# 1. Importações necessárias
# - Flask: framework web para criar a aplicação
# - jsonify: para retornar respostas JSON na API
# - request: para acessar dados das requisições
# - render_template: para renderizar templates HTML
# - redirect e url_for: para redirecionamentos
# - sqlite3: para conexão com o banco de dados SQLite
# - os: para verificar existência de arquivos

# 2. Inicialização do aplicativo Flask
# - Criar uma instância do Flask

# 3. Configuração do banco de dados
# - Definir o caminho do arquivo do banco de dados SQLite

# 4. Função para conexão com o banco de dados
# - Criar uma função que retorna uma conexão com o banco
# - Configurar a conexão para retornar linhas como dicionários (row_factory)

# 5. Função para inicialização do banco de dados
# - Verificar se o banco já existe, caso contrário criar
# - Criar tabela de produtos com os campos:
#   * id: identificador único (chave primária)
#   * nome: nome do produto
#   * preco: preço do produto
#   * estoque: quantidade em estoque
#   * categoria: categoria do produto
# - Inserir alguns produtos de exemplo para teste

# 6. Rotas para API REST

# 6.1. Listar todos os produtos (GET /api/produtos)
# - Permitir filtro por categoria via query parameter
# - Conectar ao banco e executar consulta SQL
# - Retornar lista de produtos em formato JSON

# 6.2. Obter produto específico por ID (GET /api/produtos/<id>)
# - Receber ID do produto pela URL
# - Buscar o produto no banco de dados
# - Retornar erro 404 se não encontrado
# - Retornar dados do produto em formato JSON

# 6.3. Adicionar novo produto (POST /api/produtos)
# - Receber dados do produto em formato JSON
# - Validar se todos os campos obrigatórios estão presentes
# - Inserir produto no banco de dados
# - Retornar o produto criado com status 201

# 6.4. Atualizar produto existente (PUT /api/produtos/<id>)
# - Receber ID do produto pela URL e dados em formato JSON
# - Verificar se o produto existe
# - Preparar atualização apenas dos campos fornecidos
# - Executar atualização no banco de dados
# - Retornar o produto atualizado

# 6.5. Excluir produto (DELETE /api/produtos/<id>)
# - Receber ID do produto pela URL
# - Verificar se o produto existe
# - Excluir o produto do banco de dados
# - Retornar mensagem de sucesso

# 7. Rotas para interface web

# 7.1. Página inicial (GET /)
# - Buscar todos os produtos no banco de dados
# - Renderizar template index.html com a lista de produtos

# 7.2. Formulário para adicionar produto (GET/POST /produtos/novo)
# - GET: Renderizar template form.html para novo produto
# - POST: Receber dados do formulário
#   * Inserir novo produto no banco de dados
#   * Redirecionar para página inicial

# 7.3. Formulário para editar produto (GET/POST /produtos/editar/<id>)
# - GET: Buscar produto pelo ID e renderizar form.html preenchido
# - POST: Receber dados do formulário
#   * Atualizar produto no banco de dados
#   * Redirecionar para página inicial

# 7.4. Excluir produto via interface web (GET /produtos/excluir/<id>)
# - Receber ID do produto pela URL
# - Excluir o produto do banco de dados
# - Redirecionar para página inicial

# 8. Inicialização do aplicativo
# - Verificar se o script está sendo executado diretamente
# - Inicializar o banco de dados se necessário
# - Iniciar o servidor Flask em modo de desenvolvimento 