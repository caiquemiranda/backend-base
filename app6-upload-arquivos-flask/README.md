# APP6 - Upload de Arquivos com Flask

## Visão Geral

Este projeto demonstra como implementar um sistema completo de upload, armazenamento e gerenciamento de arquivos usando Flask. O sistema inclui validação de arquivos, armazenamento seguro, visualização e funcionalidades de gerenciamento de arquivos.

## Funcionalidades

- Upload de arquivos únicos ou múltiplos
- Validação de tipos e tamanhos de arquivo
- Geração de nomes de arquivo seguros
- Listagem de arquivos enviados
- Visualização/Download de arquivos
- Exclusão de arquivos
- Visualização especial para imagens e documentos
- Processamento opcional de imagens (miniaturas)

## Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **Werkzeug**: Utilitários de segurança e manipulação de arquivos
- **Jinja2**: Engine de templates (integrada ao Flask)
- **HTML/CSS**: Frontend do sistema
- **Pillow (opcional)**: Processamento de imagens

## Estrutura do Projeto

```
app6-upload-arquivos-flask/
├── app.py                 # Arquivo principal com comentários explicativos
├── tutorial.md            # Instruções passo a passo detalhadas
├── README.md              # Este arquivo
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial com formulário de upload
│   ├── arquivos.html      # Listagem de arquivos
│   ├── visualizar.html    # Visualizador de arquivos
│   └── upload_sucesso.html # Confirmação de upload
├── static/                # Arquivos estáticos
│   └── style.css          # Estilos CSS
└── uploads/               # Diretório que armazena os arquivos enviados
```

## Como Executar

1. Certifique-se de ter Python 3.x instalado
2. Siga as instruções detalhadas no arquivo `tutorial.md`

## Conceitos Abordados

### Manipulação de Arquivos
- **Upload via Formulário**: Captura de arquivos enviados por formulários HTML
- **Armazenamento de Arquivos**: Salvamento seguro no sistema de arquivos
- **Manipulação de Caminhos**: Trabalho com caminhos de arquivos e diretórios

### Segurança
- **Validação de Extensões**: Restrição dos tipos de arquivo aceitos
- **Nomes de Arquivo Seguros**: Prevenção de ataques de path traversal
- **Limite de Tamanho**: Controle sobre o tamanho máximo de arquivos

### Interface do Usuário
- **Formulários de Upload**: Interface para envio de arquivos
- **Listagem de Arquivos**: Exibição organizada dos arquivos enviados
- **Feedback ao Usuário**: Mensagens flash para resultados de operações

### Processamento de Arquivos
- **Metadados**: Exibição de informações como tamanho e data de modificação
- **Visualização Específica**: Tratamento diferenciado para imagens e documentos
- **Miniaturas**: Geração opcional de versões reduzidas de imagens

## Segurança

Este projeto implementa várias medidas de segurança:

- Validação rigorosa de tipos de arquivo
- Uso de `secure_filename` para prevenir path traversal
- Limite de tamanho de arquivo para prevenir ataques DoS
- Estrutura que pode ser adaptada para armazenar arquivos fora da árvore pública

Em um ambiente de produção, considere medidas adicionais como:
- Autenticação de usuários
- Análise de conteúdo malicioso
- Armazenamento em nuvem seguro

## Aprendizado

Este projeto serve como introdução a:

1. Manipulação de arquivos em aplicações web
2. Segurança no upload de arquivos
3. Organização de código em aplicações Flask
4. Interfaces responsivas para gerenciamento de arquivos

## Próximos Passos

- Integração com banco de dados para metadados de arquivos
- Implementação de sistema de usuários com permissões
- Categorização e tags para arquivos
- Mecanismo de busca e filtragem
- Integração com serviços de armazenamento em nuvem (S3, Google Cloud)
- Geração de links compartilháveis com controle de acesso

## Autor

Este projeto foi criado como material educacional para o curso de desenvolvimento backend.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes. 