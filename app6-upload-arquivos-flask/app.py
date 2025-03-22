# Upload de Arquivos com Flask
# Este arquivo contém orientações para criar um sistema de upload de arquivos
# utilizando Flask, com validação, armazenamento e visualização dos arquivos

# 1. Importações necessárias
# - Flask: framework web para criar a aplicação
# - render_template: para renderizar templates HTML
# - request: para acessar dados das requisições e arquivos enviados
# - redirect e url_for: para redirecionamentos após upload
# - secure_filename: para garantir nomes de arquivos seguros
# - os: para manipulação de diretórios e arquivos
# - werkzeug.utils: contém função secure_filename
# - datetime: para gerar timestamps únicos para arquivos

# 2. Inicialização do aplicativo Flask
# - Criar uma instância do Flask
# - Configurar o diretório de upload (UPLOAD_FOLDER)
# - Definir extensões permitidas (ALLOWED_EXTENSIONS)
# - Configurar tamanho máximo de arquivo (MAX_CONTENT_LENGTH)

# 3. Função para validar extensões de arquivo
# - Criar função auxiliar (allowed_file) que verifica extensões
# - Extrair extensão do arquivo e comparar com lista permitida
# - Retornar True/False para facilitar validação nas rotas

# 4. Rota para página inicial (GET /)
# - Renderizar o template da página inicial
# - Exibir formulário de upload
# - Listar arquivos já enviados (se existirem)

# 5. Rota para processar upload (POST /upload)
# - Verificar se a requisição contém arquivos ('file' em request.files)
# - Validar se o arquivo existe e tem nome
# - Verificar se a extensão é permitida
# - Gerar nome de arquivo seguro (secure_filename)
# - Adicionar timestamp para evitar sobrescrita
# - Salvar arquivo no diretório configurado
# - Redirecionar de volta para página inicial ou página de sucesso

# 6. Rota para exibir/baixar arquivos (GET /uploads/<filename>)
# - Receber nome do arquivo pela URL
# - Verificar se o arquivo existe no diretório de uploads
# - Enviar o arquivo ao cliente (send_from_directory)
# - Opcionalmente configurar para download ou visualização

# 7. Rota para listar todos os arquivos (GET /arquivos)
# - Obter lista de arquivos no diretório de uploads
# - Renderizar página com lista e links para visualização/download
# - Mostrar metadados como tamanho e data de upload

# 8. Rota para excluir arquivo (GET /excluir/<filename>)
# - Receber nome do arquivo pela URL
# - Verificar se o arquivo existe
# - Remover arquivo do sistema (os.remove)
# - Redirecionar para página de lista de arquivos

# 9. Templates principais
# - index.html: formulário de upload e lista de arquivos
# - upload_sucesso.html: confirmação de upload bem-sucedido
# - arquivos.html: lista detalhada de arquivos com opções
# - visualizar.html: para exibir arquivos como imagens ou textos

# 10. Estilos e aparência
# - CSS para melhorar a experiência do usuário
# - Feedback visual durante upload (barra de progresso)
# - Estilos para lista de arquivos e formulário
# - Responsividade para diferentes dispositivos

# 11. Segurança e validações
# - Validação de extensões para evitar arquivos maliciosos
# - Uso de secure_filename para evitar path traversal
# - Limitação de tamanho do arquivo
# - Armazenamento em diretório específico fora da árvore pública
# - Validação do tipo de conteúdo (MIME type)

# 12. Funcionalidades avançadas
# - Upload de múltiplos arquivos
# - Barra de progresso com AJAX/Fetch
# - Preview de imagens antes do upload
# - Organização por pastas ou categorias
# - Metadados adicionais (descrição, tags)

# 13. Processamento de imagens (opcional)
# - Redimensionamento de imagens após upload (PIL/Pillow)
# - Geração de miniaturas (thumbnails)
# - Compressão para otimizar armazenamento
# - Extração de metadados EXIF

# 14. Armazenamento em nuvem (opcional)
# - Integração com serviços como AWS S3, Google Cloud Storage
# - Configuração de credenciais seguras
# - Adaptação das rotas para armazenamento em nuvem
# - Geração de URLs temporárias para acesso

# 15. Inicialização da aplicação
# - Verificar se o script está sendo executado diretamente
# - Criar diretório de uploads se não existir
# - Iniciar o servidor Flask em modo de desenvolvimento
#   Não usar modo debug em produção 