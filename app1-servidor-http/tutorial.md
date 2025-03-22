# Tutorial: Criando um Servidor HTTP Básico com Python

## Introdução

Neste tutorial, vamos construir um servidor HTTP básico usando Python puro, sem frameworks. Isso vai te ajudar a entender como os servidores web funcionam por baixo dos panos.

## Pré-requisitos

- Python 3.x instalado
- Conhecimentos básicos de Python
- Editor de texto ou IDE

## Passo 1: Configuração Inicial

Crie um arquivo chamado `servidor.py` e adicione os imports necessários:

```python
import socket
import threading
import datetime
import os
import sys
```

## Passo 2: Definir Constantes Básicas

Adicione as constantes que seu servidor vai utilizar:

```python
# Configurações do servidor
HOST = '127.0.0.1'  # Localhost
PORTA = 8080
TAMANHO_BUFFER = 1024
CODIFICACAO = 'utf-8'
```

## Passo 3: Criar Mapeamentos de Tipos MIME

Os tipos MIME informam ao navegador que tipo de conteúdo está sendo enviado:

```python
TIPOS_MIME = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.txt': 'text/plain'
}
```

## Passo 4: Definir Códigos de Status HTTP

Adicione os códigos de status que você vai usar:

```python
STATUS_HTTP = {
    200: 'OK',
    404: 'Not Found',
    500: 'Internal Server Error'
}
```

## Passo 5: Criar uma Classe para Requisições HTTP

```python
class Requisicao:
    def __init__(self):
        self.metodo = None
        self.caminho = None
        self.versao = None
        self.cabecalhos = {}
        self.corpo = None
    
    def analisar_requisicao(self, dados):
        linhas = dados.split('\r\n')
        
        # Extrair método, caminho e versão HTTP
        if linhas and linhas[0]:
            partes = linhas[0].split()
            if len(partes) >= 3:
                self.metodo = partes[0]
                self.caminho = partes[1]
                self.versao = partes[2]
        
        # Extrair cabeçalhos
        i = 1
        while i < len(linhas) and linhas[i]:
            if ':' in linhas[i]:
                nome, valor = linhas[i].split(':', 1)
                self.cabecalhos[nome.strip()] = valor.strip()
            i += 1
        
        # Extrair corpo (se houver)
        if i < len(linhas):
            self.corpo = '\r\n'.join(linhas[i+1:])
```

## Passo 6: Criar uma Classe para Respostas HTTP

```python
class Resposta:
    def __init__(self, codigo=200, corpo='', tipo_conteudo='text/html'):
        self.codigo = codigo
        self.corpo = corpo
        self.cabecalhos = {
            'Content-Type': tipo_conteudo,
            'Content-Length': len(corpo),
            'Server': 'ServidorPython/1.0',
            'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
    
    def gerar_resposta(self):
        resposta_linhas = [f'HTTP/1.1 {self.codigo} {STATUS_HTTP[self.codigo]}']
        
        # Adicionar cabeçalhos
        for nome, valor in self.cabecalhos.items():
            resposta_linhas.append(f'{nome}: {valor}')
        
        # Adicionar linha em branco e corpo
        resposta = '\r\n'.join(resposta_linhas) + '\r\n\r\n' + self.corpo
        
        return resposta.encode(CODIFICACAO)
```

## Passo 7: Criar a Classe Principal do Servidor

```python
class ServidorHTTP:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.socket_servidor = None
    
    def iniciar(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket_servidor.bind((self.host, self.porta))
            self.socket_servidor.listen(5)
            print(f"Servidor iniciado em http://{self.host}:{self.porta}")
            
            while True:
                socket_cliente, endereco = self.socket_servidor.accept()
                thread_cliente = threading.Thread(target=self.tratar_cliente, args=(socket_cliente, endereco))
                thread_cliente.daemon = True
                thread_cliente.start()
                
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
        finally:
            if self.socket_servidor:
                self.socket_servidor.close()
    
    def tratar_cliente(self, socket_cliente, endereco):
        print(f"Conexão de {endereco[0]}:{endereco[1]}")
        
        try:
            # Receber dados
            dados = socket_cliente.recv(TAMANHO_BUFFER).decode(CODIFICACAO)
            
            if dados:
                # Analisar requisição
                requisicao = Requisicao()
                requisicao.analisar_requisicao(dados)
                
                # Gerar resposta
                resposta = self.rotear_requisicao(requisicao)
                
                # Enviar resposta
                socket_cliente.sendall(resposta.gerar_resposta())
        
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
        finally:
            socket_cliente.close()
```

## Passo 8: Implementar o Roteamento de Requisições

```python
def rotear_requisicao(self, requisicao):
    if requisicao.metodo == 'GET':
        if requisicao.caminho == '/':
            return self.pagina_inicial()
        elif requisicao.caminho == '/pagina':
            return self.pagina_exemplo()
        else:
            return self.pagina_nao_encontrada()
    elif requisicao.metodo == 'POST':
        if requisicao.caminho == '/enviar':
            return self.processar_envio(requisicao.corpo)
        else:
            return self.pagina_nao_encontrada()
    else:
        return Resposta(405, '<html><body><h1>Método não permitido</h1></body></html>')
```

## Passo 9: Implementar Páginas e Manipuladores

```python
def pagina_inicial(self):
    conteudo = """
    <html>
        <head>
            <title>Servidor Python</title>
        </head>
        <body>
            <h1>Bem-vindo ao Servidor HTTP em Python</h1>
            <p>Este é um servidor HTTP básico implementado em Python puro.</p>
            <a href="/pagina">Ir para página de exemplo</a>
        </body>
    </html>
    """
    return Resposta(200, conteudo)

def pagina_exemplo(self):
    conteudo = """
    <html>
        <head>
            <title>Página de Exemplo</title>
        </head>
        <body>
            <h1>Página de Exemplo</h1>
            <p>Esta é uma página de exemplo servida pelo nosso servidor Python.</p>
            <form action="/enviar" method="post">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome"><br><br>
                <label for="idade">Idade:</label>
                <input type="number" id="idade" name="idade"><br><br>
                <input type="submit" value="Enviar">
            </form>
            <a href="/">Voltar</a>
        </body>
    </html>
    """
    return Resposta(200, conteudo)

def processar_envio(self, dados):
    conteudo = f"""
    <html>
        <head>
            <title>Dados Recebidos</title>
        </head>
        <body>
            <h1>Dados Recebidos com Sucesso!</h1>
            <p>Dados: {dados}</p>
            <a href="/">Voltar ao início</a>
        </body>
    </html>
    """
    return Resposta(200, conteudo)

def pagina_nao_encontrada(self):
    conteudo = """
    <html>
        <head>
            <title>Página Não Encontrada</title>
        </head>
        <body>
            <h1>404 - Página Não Encontrada</h1>
            <p>A página que você está procurando não existe.</p>
            <a href="/">Voltar ao início</a>
        </body>
    </html>
    """
    return Resposta(404, conteudo)
```

## Passo 10: Adicionar o Bloco Principal de Execução

```python
if __name__ == "__main__":
    try:
        servidor = ServidorHTTP(HOST, PORTA)
        print("Iniciando servidor HTTP na porta 8080...")
        print("Pressione Ctrl+C para encerrar")
        servidor.iniciar()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")
```

## Testando o Servidor

1. Salve o arquivo `servidor.py` e execute-o com Python:
   ```
   python servidor.py
   ```

2. Abra seu navegador e acesse:
   ```
   http://127.0.0.1:8080
   ```

3. Teste as diferentes rotas e o formulário.

## Próximos Passos

Depois de entender o básico, você pode aprimorar seu servidor:

- Adicionar suporte para arquivos estáticos (CSS, imagens)
- Implementar sessões e cookies
- Melhorar a segurança
- Estudar frameworks como Flask ou Django que fazem isso tudo por você

## Conclusão

Parabéns! Você criou um servidor HTTP básico do zero usando Python puro. Isso te dá uma compreensão fundamental de como servidores web funcionam, o que será útil mesmo quando você usar frameworks mais avançados. 