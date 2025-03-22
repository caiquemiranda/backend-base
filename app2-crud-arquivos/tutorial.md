# Tutorial: Criando um CRUD com Arquivos Locais em Python

## Introdução

Neste tutorial, vamos criar um sistema CRUD (Create, Read, Update, Delete) usando Python e arquivos locais para armazenamento de dados. Essa é uma maneira simples de entender os conceitos de persistência de dados sem precisar de um banco de dados.

## Pré-requisitos

- Python 3.x instalado
- Conhecimentos básicos de Python
- Editor de texto ou IDE

## O que é um CRUD?

CRUD é um acrônimo para as quatro operações básicas de persistência:
- **C**reate (Criar): adicionar novos dados
- **R**ead (Ler): consultar dados existentes
- **U**pdate (Atualizar): modificar dados existentes
- **D**elete (Excluir): remover dados existentes

## Passo 1: Configuração Inicial

Crie um arquivo chamado `crud.py` e comece adicionando os imports necessários:

```python
import os
import json
from datetime import datetime
```

## Passo 2: Definir Constantes

```python
# Arquivo onde os dados serão armazenados
ARQUIVO_DADOS = 'dados.json'

# Codificação para leitura/escrita de arquivos
ENCODING = 'utf-8'

# Campo usado como identificador único
CAMPO_ID = 'id'

# Campos obrigatórios para cada item
CAMPOS_OBRIGATORIOS = ['id', 'nome', 'descricao']
```

## Passo 3: Criar uma Classe para Representar um Item

```python
class Item:
    def __init__(self, id=None, nome='', descricao=''):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    def validar(self):
        # Verificar se todos os campos obrigatórios estão preenchidos
        if not self.nome or not self.descricao:
            return False
        return True
    
    def para_dicionario(self):
        # Converter objeto para dicionário (para serialização)
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao
        }
    
    @classmethod
    def de_dicionario(cls, dicionario):
        # Criar objeto a partir de dicionário (para deserialização)
        item = cls()
        item.id = dicionario.get('id')
        item.nome = dicionario.get('nome', '')
        item.descricao = dicionario.get('descricao', '')
        item.data_criacao = dicionario.get('data_criacao', '')
        return item
```

## Passo 4: Criar a Classe para Gerenciar as Operações CRUD

```python
class GerenciadorCRUD:
    def __init__(self, arquivo_dados=ARQUIVO_DADOS):
        self.arquivo_dados = arquivo_dados
        self.itens = []
        self.proximo_id = 1
        self.inicializar()
    
    def inicializar(self):
        # Verificar se o arquivo existe, se não, criar um novo
        if os.path.exists(self.arquivo_dados):
            self.carregar_dados()
        else:
            self.salvar_dados()
    
    def carregar_dados(self):
        # Carregar dados do arquivo JSON
        try:
            with open(self.arquivo_dados, 'r', encoding=ENCODING) as arquivo:
                dados = json.load(arquivo)
                
                # Converter dicionários para objetos Item
                self.itens = [Item.de_dicionario(item) for item in dados]
                
                # Encontrar o próximo ID disponível
                if self.itens:
                    maior_id = max(item.id for item in self.itens)
                    self.proximo_id = maior_id + 1
                else:
                    self.proximo_id = 1
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.itens = []
            self.proximo_id = 1
    
    def salvar_dados(self):
        # Salvar dados no arquivo JSON
        try:
            # Converter objetos Item para dicionários
            dados = [item.para_dicionario() for item in self.itens]
            
            with open(self.arquivo_dados, 'w', encoding=ENCODING) as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
```

## Passo 5: Implementar as Operações CRUD

Adicione os métodos para operações CRUD à classe `GerenciadorCRUD`:

```python
def criar(self, nome, descricao):
    # Criar novo item
    novo_item = Item(self.proximo_id, nome, descricao)
    
    if not novo_item.validar():
        return None
    
    self.itens.append(novo_item)
    self.proximo_id += 1
    self.salvar_dados()
    
    return novo_item

def ler_todos(self):
    # Retornar todos os itens
    return self.itens

def ler_por_id(self, id):
    # Buscar item por ID
    for item in self.itens:
        if item.id == id:
            return item
    return None

def atualizar(self, id, nome=None, descricao=None):
    # Atualizar item existente
    item = self.ler_por_id(id)
    
    if not item:
        return False
    
    if nome:
        item.nome = nome
    
    if descricao:
        item.descricao = descricao
    
    self.salvar_dados()
    return True

def excluir(self, id):
    # Remover item
    item = self.ler_por_id(id)
    
    if not item:
        return False
    
    self.itens.remove(item)
    self.salvar_dados()
    return True
```

## Passo 6: Criar uma Interface de Linha de Comando

```python
class InterfaceCLI:
    def __init__(self):
        self.gerenciador = GerenciadorCRUD()
    
    def limpar_tela(self):
        # Limpar tela (compatível com diferentes sistemas)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        self.limpar_tela()
        print("===== SISTEMA CRUD EM PYTHON =====")
        print("1. Listar todos os itens")
        print("2. Buscar item por ID")
        print("3. Adicionar novo item")
        print("4. Atualizar item existente")
        print("5. Excluir item")
        print("0. Sair")
        print("==============================")
    
    def iniciar(self):
        while True:
            self.exibir_menu()
            
            try:
                opcao = int(input("Escolha uma opção: "))
                
                if opcao == 0:
                    print("\nSaindo... Dados salvos.")
                    break
                elif opcao == 1:
                    self.listar_itens()
                elif opcao == 2:
                    self.buscar_item()
                elif opcao == 3:
                    self.adicionar_item()
                elif opcao == 4:
                    self.atualizar_item()
                elif opcao == 5:
                    self.excluir_item()
                else:
                    print("\nOpção inválida!")
            except ValueError:
                print("\nPor favor, digite um número válido.")
            
            input("\nPressione ENTER para continuar...")
```

## Passo 7: Implementar as Funções da Interface

Adicione os métodos para cada operação à classe `InterfaceCLI`:

```python
def listar_itens(self):
    self.limpar_tela()
    print("=== LISTA DE TODOS OS ITENS ===\n")
    
    itens = self.gerenciador.ler_todos()
    
    if not itens:
        print("Nenhum item cadastrado.")
        return
    
    for item in itens:
        self.exibir_item(item)
        print("-----------------------------")
    
    print(f"\nTotal de itens: {len(itens)}")

def buscar_item(self):
    self.limpar_tela()
    print("=== BUSCAR ITEM POR ID ===\n")
    
    try:
        id_busca = int(input("Digite o ID do item: "))
        
        item = self.gerenciador.ler_por_id(id_busca)
        
        if not item:
            print("\nItem não encontrado!")
            return
        
        print("\nItem encontrado:")
        self.exibir_item(item)
    except ValueError:
        print("\nPor favor, digite um número válido.")

def adicionar_item(self):
    self.limpar_tela()
    print("=== ADICIONAR NOVO ITEM ===\n")
    
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    
    item = self.gerenciador.criar(nome, descricao)
    
    if item:
        print(f"\nItem adicionado com sucesso! ID: {item.id}")
    else:
        print("\nErro ao adicionar item. Verifique os dados informados.")

def atualizar_item(self):
    self.limpar_tela()
    print("=== ATUALIZAR ITEM ===\n")
    
    try:
        id_atualizar = int(input("Digite o ID do item que deseja atualizar: "))
        
        item = self.gerenciador.ler_por_id(id_atualizar)
        
        if not item:
            print("\nItem não encontrado!")
            return
        
        print("\nDados atuais do item:")
        self.exibir_item(item)
        
        print("\nNovos dados do item (deixe vazio para manter o valor atual):")
        
        novo_nome = input("Novo nome: ")
        nova_descricao = input("Nova descrição: ")
        
        # Usar os valores atuais se os novos estiverem vazios
        nome = novo_nome if novo_nome else None
        descricao = nova_descricao if nova_descricao else None
        
        if self.gerenciador.atualizar(id_atualizar, nome, descricao):
            print("\nItem atualizado com sucesso!")
        else:
            print("\nErro ao atualizar item.")
    except ValueError:
        print("\nPor favor, digite um número válido.")

def excluir_item(self):
    self.limpar_tela()
    print("=== EXCLUIR ITEM ===\n")
    
    try:
        id_excluir = int(input("Digite o ID do item que deseja excluir: "))
        
        item = self.gerenciador.ler_por_id(id_excluir)
        
        if not item:
            print("\nItem não encontrado!")
            return
        
        print("\nItem a ser excluído:")
        self.exibir_item(item)
        
        confirmacao = input("\nTem certeza que deseja excluir este item? (S/N): ")
        
        if confirmacao.upper() == "S":
            if self.gerenciador.excluir(id_excluir):
                print("\nItem excluído com sucesso!")
            else:
                print("\nErro ao excluir item.")
        else:
            print("\nOperação cancelada!")
    except ValueError:
        print("\nPor favor, digite um número válido.")

def exibir_item(self, item):
    print(f"ID: {item.id}")
    print(f"Nome: {item.nome}")
    print(f"Descrição: {item.descricao}")
    print(f"Data de criação: {item.data_criacao}")
```

## Passo 8: Adicionar o Bloco Principal de Execução

```python
if __name__ == "__main__":
    try:
        print("Iniciando Sistema CRUD com Arquivos Locais")
        interface = InterfaceCLI()
        interface.iniciar()
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")
```

## Testando o Sistema CRUD

1. Salve o arquivo `crud.py` e execute-o com Python:
   ```
   python crud.py
   ```

2. Use o menu interativo para testar todas as operações CRUD:
   - Adicionar novos itens
   - Listar todos os itens
   - Buscar itens específicos
   - Atualizar itens existentes
   - Excluir itens

3. Verifique que os dados são persistidos entre execuções do programa no arquivo `dados.json`.

## Funcionamento da Persistência de Dados

O sistema usa um arquivo JSON para armazenar os dados, que é carregado na inicialização e salvo após cada operação que modifica os dados. Esta abordagem é simples, mas eficaz para pequenas aplicações.

## Próximos Passos

Depois de entender o básico, você pode aprimorar seu sistema:

- Adicionar mais campos aos itens
- Implementar busca por texto nos itens
- Adicionar validação mais robusta
- Implementar ordenação e filtragem na listagem
- Migrar para um banco de dados real (SQLite, MySQL, etc.)
- Criar uma interface web simples com Flask

## Conclusão

Parabéns! Você criou um sistema CRUD completo com persistência de dados em arquivos JSON. Este projeto te dá uma compreensão fundamental de como operações CRUD funcionam, o que é a base para praticamente qualquer aplicação que lida com dados persistentes. 