programa
{
    inclua biblioteca Util
    inclua biblioteca Texto
    
    // Constantes
    const inteiro PORTA = 5000
    const cadeia METODO_GET = "GET"
    const cadeia METODO_POST = "POST"
    const cadeia METODO_PUT = "PUT"
    const cadeia METODO_DELETE = "DELETE"
    
    // Estrutura de dados para um produto
    tipo Produto {
        inteiro id
        cadeia nome
        real preco
        inteiro estoque
        cadeia categoria
    }
    
    // Banco de dados simulado (array de produtos)
    Produto produtos[100]
    inteiro total_produtos = 0
    inteiro proximo_id = 1
    
    // Tipos para requisição e resposta
    tipo Requisicao {
        cadeia metodo
        cadeia rota
        cadeia dados
    }
    
    tipo Resposta {
        inteiro status
        cadeia tipo_conteudo
        cadeia dados
    }
    
    funcao inicio()
    {
        // Inicializar com alguns produtos
        inicializar_dados()
        
        escreva("API Flask simulada em Portugol\n")
        escreva("Rodando na porta ", PORTA, "\n")
        escreva("------------------------------\n")
        
        // Loop principal do servidor
        enquanto (verdadeiro)
        {
            escreva("\nAguardando requisição...\n")
            
            // Simular uma requisição recebida
            Requisicao req = receber_requisicao()
            
            // Processar a requisição e gerar resposta
            Resposta resp = processar_requisicao(req)
            
            // Enviar resposta
            enviar_resposta(resp)
            
            // Pausa para simular tempo de processamento
            Util.aguarde(1000)
        }
    }
    
    funcao inicializar_dados()
    {
        // Adicionar alguns produtos iniciais
        adicionar_produto("Notebook", 3500.0, 10, "Eletrônicos")
        adicionar_produto("Smartphone", 1800.0, 15, "Eletrônicos")
        adicionar_produto("Fones de Ouvido", 150.0, 30, "Acessórios")
        adicionar_produto("Mochila", 120.0, 20, "Acessórios")
        adicionar_produto("Livro Python", 85.0, 50, "Livros")
    }
    
    funcao adicionar_produto(cadeia nome, real preco, inteiro estoque, cadeia categoria)
    {
        produtos[total_produtos].id = proximo_id
        produtos[total_produtos].nome = nome
        produtos[total_produtos].preco = preco
        produtos[total_produtos].estoque = estoque
        produtos[total_produtos].categoria = categoria
        
        total_produtos++
        proximo_id++
    }
    
    funcao Requisicao receber_requisicao()
    {
        // Simulação de uma requisição HTTP
        Requisicao req
        
        // Escolher aleatoriamente um método HTTP para simulação
        inteiro escolha_metodo = Util.sorteia(1, 4)
        
        escolha(escolha_metodo)
        {
            caso 1:
                req.metodo = METODO_GET
                
                // Gerar aleatoriamente rota para GET
                inteiro tipo_get = Util.sorteia(1, 2)
                
                se (tipo_get == 1)
                {
                    req.rota = "/api/produtos"
                    escreva("Requisição recebida: ", req.metodo, " ", req.rota, "\n")
                }
                senao
                {
                    // Busca por ID
                    inteiro id_random = Util.sorteia(1, proximo_id - 1)
                    req.rota = "/api/produtos/" + id_random
                    escreva("Requisição recebida: ", req.metodo, " ", req.rota, "\n")
                }
                pare
                
            caso 2:
                req.metodo = METODO_POST
                req.rota = "/api/produtos"
                req.dados = "{'nome':'Produto Novo','preco':99.9,'estoque':5,'categoria':'Diversos'}"
                escreva("Requisição recebida: ", req.metodo, " ", req.rota, "\n")
                escreva("Dados: ", req.dados, "\n")
                pare
                
            caso 3:
                req.metodo = METODO_PUT
                inteiro id_random = Util.sorteia(1, proximo_id - 1)
                req.rota = "/api/produtos/" + id_random
                req.dados = "{'nome':'Produto Atualizado','preco':199.9,'estoque':10,'categoria':'Atualizados'}"
                escreva("Requisição recebida: ", req.metodo, " ", req.rota, "\n")
                escreva("Dados: ", req.dados, "\n")
                pare
                
            caso 4:
                req.metodo = METODO_DELETE
                inteiro id_random = Util.sorteia(1, proximo_id - 1)
                req.rota = "/api/produtos/" + id_random
                escreva("Requisição recebida: ", req.metodo, " ", req.rota, "\n")
                pare
        }
        
        retorne req
    }
    
    funcao Resposta processar_requisicao(Requisicao req)
    {
        Resposta resp
        resp.tipo_conteudo = "application/json"
        
        // Verificar se a rota é para produtos
        se (Texto.posicao(req.rota, "/api/produtos", 0) == 0)
        {
            // Rota para operações com produtos
            
            // Verificar se é uma rota para um produto específico (com ID)
            se (Texto.numero_caracteres(req.rota) > 13 e Texto.posicao(req.rota, "/", 13) == 13)
            {
                // Extrair ID da rota (/api/produtos/ID)
                cadeia id_str = Texto.extrair_subtexto(req.rota, 14, Texto.numero_caracteres(req.rota))
                inteiro id = Util.validos_para_inteiro(id_str) ? Util.cadeia_para_inteiro(id_str) : 0
                
                // Operações para um produto específico (ID)
                escolha (req.metodo)
                {
                    caso METODO_GET:
                        resp = obter_produto_por_id(id)
                        pare
                        
                    caso METODO_PUT:
                        resp = atualizar_produto(id, req.dados)
                        pare
                        
                    caso METODO_DELETE:
                        resp = excluir_produto(id)
                        pare
                        
                    caso contrario:
                        resp.status = 405  // Método não permitido
                        resp.dados = "{'erro': 'Método não permitido'}"
                }
            }
            senao
            {
                // Operações para todos os produtos
                escolha (req.metodo)
                {
                    caso METODO_GET:
                        resp = listar_produtos()
                        pare
                        
                    caso METODO_POST:
                        resp = criar_produto(req.dados)
                        pare
                        
                    caso contrario:
                        resp.status = 405  // Método não permitido
                        resp.dados = "{'erro': 'Método não permitido'}"
                }
            }
        }
        senao
        {
            // Rota não encontrada
            resp.status = 404
            resp.dados = "{'erro': 'Rota não encontrada'}"
        }
        
        escreva("Processando requisição... Status: ", resp.status, "\n")
        retorne resp
    }
    
    funcao Resposta listar_produtos()
    {
        Resposta resp
        resp.status = 200
        
        // Simular dados JSON de resposta
        resp.dados = "["
        
        para (inteiro i = 0; i < total_produtos; i++)
        {
            se (produtos[i].id > 0)  // Verificar se o produto não foi excluído
            {
                se (i > 0 e resp.dados != "[")
                {
                    resp.dados = resp.dados + ","
                }
                
                resp.dados = resp.dados + "{'id':" + produtos[i].id + 
                             ",'nome':'" + produtos[i].nome + 
                             "','preco':" + produtos[i].preco + 
                             ",'estoque':" + produtos[i].estoque + 
                             ",'categoria':'" + produtos[i].categoria + "'}"
            }
        }
        
        resp.dados = resp.dados + "]"
        retorne resp
    }
    
    funcao Resposta obter_produto_por_id(inteiro id)
    {
        Resposta resp
        
        // Buscar produto pelo ID
        inteiro indice = -1
        para (inteiro i = 0; i < total_produtos; i++)
        {
            se (produtos[i].id == id)
            {
                indice = i
                pare
            }
        }
        
        se (indice != -1)
        {
            resp.status = 200
            resp.dados = "{'id':" + produtos[indice].id + 
                         ",'nome':'" + produtos[indice].nome + 
                         "','preco':" + produtos[indice].preco + 
                         ",'estoque':" + produtos[indice].estoque + 
                         ",'categoria':'" + produtos[indice].categoria + "'}"
        }
        senao
        {
            resp.status = 404
            resp.dados = "{'erro': 'Produto não encontrado'}"
        }
        
        retorne resp
    }
    
    funcao Resposta criar_produto(cadeia dados)
    {
        // Simulação simples da criação de um produto
        Resposta resp
        
        se (total_produtos < 100)
        {
            // Em um cenário real, analisaríamos os dados JSON
            // Aqui vamos apenas criar um produto com dados fixos para simulação
            produtos[total_produtos].id = proximo_id
            produtos[total_produtos].nome = "Produto " + proximo_id
            produtos[total_produtos].preco = 50.0 * proximo_id
            produtos[total_produtos].estoque = 10
            produtos[total_produtos].categoria = "Novos"
            
            resp.status = 201  // Created
            resp.dados = "{'id':" + proximo_id + 
                         ",'nome':'Produto " + proximo_id + 
                         "','preco':" + (50.0 * proximo_id) + 
                         ",'estoque':10" + 
                         ",'categoria':'Novos'}"
            
            total_produtos++
            proximo_id++
        }
        senao
        {
            resp.status = 507  // Insufficient Storage
            resp.dados = "{'erro': 'Capacidade máxima de produtos atingida'}"
        }
        
        retorne resp
    }
    
    funcao Resposta atualizar_produto(inteiro id, cadeia dados)
    {
        Resposta resp
        
        // Buscar produto pelo ID
        inteiro indice = -1
        para (inteiro i = 0; i < total_produtos; i++)
        {
            se (produtos[i].id == id)
            {
                indice = i
                pare
            }
        }
        
        se (indice != -1)
        {
            // Em um cenário real, analisaríamos os dados JSON
            // Aqui vamos apenas atualizar com valores fixos para simulação
            produtos[indice].nome = "Produto Atualizado " + id
            produtos[indice].preco = 75.0
            produtos[indice].estoque = 20
            produtos[indice].categoria = "Atualizados"
            
            resp.status = 200
            resp.dados = "{'id':" + produtos[indice].id + 
                         ",'nome':'" + produtos[indice].nome + 
                         "','preco':" + produtos[indice].preco + 
                         ",'estoque':" + produtos[indice].estoque + 
                         ",'categoria':'" + produtos[indice].categoria + "'}"
        }
        senao
        {
            resp.status = 404
            resp.dados = "{'erro': 'Produto não encontrado'}"
        }
        
        retorne resp
    }
    
    funcao Resposta excluir_produto(inteiro id)
    {
        Resposta resp
        
        // Buscar produto pelo ID
        inteiro indice = -1
        para (inteiro i = 0; i < total_produtos; i++)
        {
            se (produtos[i].id == id)
            {
                indice = i
                pare
            }
        }
        
        se (indice != -1)
        {
            // Na simulação, apenas marcamos como ID 0 para indicar que foi excluído
            produtos[indice].id = 0
            
            resp.status = 204  // No Content
            resp.dados = ""    // Resposta vazia para 204
        }
        senao
        {
            resp.status = 404
            resp.dados = "{'erro': 'Produto não encontrado'}"
        }
        
        retorne resp
    }
    
    funcao enviar_resposta(Resposta resp)
    {
        escreva("Enviando resposta com status ", resp.status, "\n")
        escreva("Content-Type: ", resp.tipo_conteudo, "\n")
        
        se (resp.dados != "")
        {
            // Simular limite de dados para exibição
            inteiro max_exibicao = 100
            cadeia dados_exibir = resp.dados
            
            se (Texto.numero_caracteres(dados_exibir) > max_exibicao)
            {
                dados_exibir = Texto.extrair_subtexto(dados_exibir, 0, max_exibicao) + "..."
            }
            
            escreva("Corpo da resposta: ", dados_exibir, "\n")
        }
        senao
        {
            escreva("Resposta sem corpo (No Content)\n")
        }
    }
} 