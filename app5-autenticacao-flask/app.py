# Autenticação Simples com Flask
# Este arquivo contém orientações para criar um sistema de autenticação
# utilizando Flask com armazenamento de sessão e proteção de rotas

# 1. Importações necessárias
# - Flask: framework web para criar a aplicação
# - render_template: para renderizar templates HTML
# - request: para acessar dados das requisições (formulários)
# - redirect e url_for: para redirecionamentos após login/logout
# - flash: para mensagens de feedback ao usuário
# - session: para gerenciar sessões de usuário
# - werkzeug.security: para hash e verificação de senhas
# - functools.wraps: para criar decoradores de proteção de rotas

# 2. Inicialização do aplicativo Flask
# - Criar uma instância do Flask
# - Configurar uma chave secreta forte para sessões (app.secret_key)
#   A chave secreta é fundamental para criptografia de cookies

# 3. Modelo de usuários simulado
# - Em um projeto real, você usaria um banco de dados
# - Para demonstração, usar um dicionário com usuários
# - Armazenar apenas o hash das senhas, nunca em texto puro
# - Incluir informações como nome de usuário, hash da senha e nome completo

# 4. Rota da página inicial (GET /)
# - Renderizar o template da página inicial
# - Adaptar a exibição de acordo com estado de autenticação

# 5. Rota de login (GET/POST /login)
# - GET: Exibir formulário de login
# - POST: Processar tentativa de login:
#   * Obter dados do formulário (username e password)
#   * Verificar se o usuário existe
#   * Verificar se a senha está correta usando check_password_hash
#   * Se autenticado, armazenar usuário na sessão e redirecionar
#   * Se falhar, exibir mensagem de erro e mostrar form novamente

# 6. Rota de área protegida/dashboard (GET /dashboard)
# - Verificar se o usuário está autenticado (verificar session)
# - Se não estiver autenticado, redirecionar para login
# - Buscar informações do usuário e renderizar dashboard

# 7. Rota de logout (GET /logout)
# - Remover dados do usuário da sessão
# - Redirecionar para a página inicial ou login
# - Exibir mensagem de feedback (logout bem-sucedido)

# 8. Decorador para proteção de rotas
# - Criar função que recebe outra função (view)
# - Verificar se o usuário está na sessão
# - Redirecionar para login se não estiver autenticado
# - Permitir acesso à view original se estiver autenticado
# - Usar functools.wraps para preservar metadados da função

# 9. Templates principais
# - base.html: template base com navegação adaptativa
# - index.html: página inicial que muda conforme autenticação
# - login.html: formulário de login com validação
# - dashboard.html: área protegida com conteúdo personalizado

# 10. Estilos e aparência
# - Usar CSS para melhorar a experiência do usuário
# - Estilizar formulários, mensagens e navegação
# - Tornar o design responsivo

# 11. Segurança adicional
# - Proteção contra ataques de força bruta (limitar tentativas)
# - Uso de HTTPS em ambiente de produção
# - Tokens CSRF para proteger formulários
# - Cookies com flags secure e httponly

# 12. Expansões possíveis
# - Cadastro de novos usuários
# - Recuperação de senha
# - Níveis de permissão para diferentes tipos de usuário
# - Integração com banco de dados (SQLite, PostgreSQL)
# - Usar Flask-Login para gerenciamento avançado de autenticação

# 13. Inicialização da aplicação
# - Verificar se o script está sendo executado diretamente
# - Iniciar o servidor Flask em modo de desenvolvimento
#   Não usar modo debug em produção 