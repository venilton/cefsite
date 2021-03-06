﻿# -*- coding: utf-8 -*-

from querys import *

query = Modelo()
query.conecta()

def prompt_table(plural, campo_codigo, campos, tabela, func_select = None, func_insert = None, func_update = None, func_locate = None):
    rep = 1
    while rep:
        print """\n%s
    a) Listar todos
    b) Adicionar
    c) Atualizar
    d) Procurar
    [Enter] para voltar""" % plural.upper()
        op = raw_input()
        if op == 'a':
            if func_select:
                func_select()
            else:
                rows = tabela.select_all()
                for row in rows:
                    line = "- "
                    for col in row:
                        line += "%s, " % col
                    print line[:-2]

                print "\n %s encontrados: %d" % (plural, len(rows))

        elif op == 'b':
            if func_insert:
                func_insert()
            else:
                info = {}
                for campo in campos:
                    conteudo = raw_input(campo + ': ')
                    if conteudo:
                        info[campo] = conteudo
                tabela.insert(info)
                print "\nAdicionado."

        elif op == 'c':
            if func_update:
                func_update()
            else:
                cod = raw_input('Código: ')
                info = {}
                for campo in campos:
                    conteudo = raw_input(campo + ': ')
                    if conteudo:
                        info[campo] = conteudo
                tabela.update(info, {campo_codigo: cod })
                print "\nAtualizado."

        elif op == 'd':
            if func_locate:
                func_locate()
            else:
                srch = raw_input('Procurar por: ')
                rows = tabela.locate_item(srch)
                for row in rows:
                    line = "- "
                    for col in row:
                        line += "%s, " % col
                    print line[:-2]

                print "\n %s encontrados: %d" % (plural, len(rows))

        else:
            rep = 0

def not_implemented():
    print "Função não implementada.\n"

def insert_filme():
    info = {}
    for campo in query.filmes.all_fields[1:]:
        conteudo = raw_input(campo + ': ')
        if conteudo:
            info[campo] = conteudo

    query.filmes.insert(info)
    cod_filme = query.filmes.lastInsertId()
    print cod_filme
    if cod_filme:
        for quant in range(int(info['quantidade'])):
            query.dvds.insert_item(cod_filme)
        print "\nAdicionado."

#prompt_table(plural, campo_codigo, campos, tabela)
def prompt_clientes():
    tabela = query.clientes
    campos = tabela.all_fields[1:]
    prompt_table('clientes', tabela.all_fields[0], campos, tabela)

def prompt_categoria_dvd():
    tabela = query.categoria_dvd
    campos = tabela.all_fields[1:]
    prompt_table('categorias', tabela.all_fields[0], campos, tabela)

def prompt_filmes():
    tabela = query.filmes
    campos = tabela.all_fields[1:]
    prompt_table('filmes', tabela.all_fields[0], campos, tabela, func_insert=insert_filme)

def prompt_generos():
    tabela = query.generos
    campos = tabela.all_fields[1:]
    prompt_table('gêneros', tabela.all_fields[0], campos, tabela)

def prompt_dvds():
    tabela = query.dvds
    campos = tabela.all_fields[1:]
    prompt_table('DVDs', tabela.all_fields[0], campos, tabela, func_locate=not_implemented)

def prompt_contas():
    tabela = query.contas
    campos = tabela.all_fields[1:]
    prompt_table('conta', tabela.all_fields[0], campos, tabela)

def prompt_categorias():
    tabela = query.categorias
    campos = tabela.all_fields[1:]
    prompt_table('categorias', tabela.all_fields[0], campos, tabela)

def prompt_produtos():
    tabela = query.produtos
    campos = tabela.all_fields[1:]
    prompt_table('produtos', tabela.all_fields[0], campos, tabela)

def prompt_locados():
    rep = 1
    while rep:
        print """\nLOCAÇÃO
    a) Listar locados
    b) Alugar
    c) Devolver
    d) Lista atrasados
    [Enter] para voltar"""

        op = raw_input()
        if op == 'a':
            rows = query.locados.select_locados()
            for row in rows:
                line = "- "
                for col in row:
                    line += "%s, " % col
                print line[:-2]

            print "\n Locações encontradas: %d" % len(rows)

        elif op == 'b':
            cod_cliente = raw_input('Cliente: ')
            cod_dvd = int(raw_input('Código do DVD: '))

            locado = query.locados.locate_locados(cod_dvd)
            if locado:
                print "DVD já esta alugado\n"
            else:
                dias = 7
                query.locados.insert_locacao(cod_cliente, cod_dvd, dias)

        elif op == 'c':
            cod_dvd = int(raw_input('Código do DVD: '))
            idcod = locate_locados(cod_dvd)
            query.locados.insert_devolucao(idcod)
            print "Devolução OK"

        elif op == 'd':
            rows = query.locados.select_locados_atrasados()
            for row in rows:
                line = "- "
                for col in row:
                    line += "%s, " % col
                print line[:-2]

            print "\n Locações atrasadas: %d" % len(rows)

        else:
            rep = 0

def prompt_estoque():
    rep = 1
    while rep:
        print """\nESTOQUE
    a) Consultar estoque
    b) Entrada
    c) Saída
    [Enter] para voltar"""

        op = raw_input()
        if op == 'a':
            cod_produto = raw_input('Produto: ')
            localiz = raw_input('Localização: ')
            quant = query.estoque.get_estoque(cod_produto, localiz)
            if quant:
                print "%d encontrado." % quant
            else:
                print "Produto não está no estoque.\n"

        elif op == 'b':
            cod_produto = raw_input('Produto: ')
            localiz = raw_input('Localização: ')
            quant = raw_input('Quantidade: ')
            query.estoque.add_estoque(cod_produto, localiz, quant)
            print "Adicionado.\n"

        elif op == 'c':
            cod_produto = raw_input('Produto: ')
            localiz = raw_input('Localização: ')
            quant = raw_input('Quantidade: ')
            try:
                query.estoque.baixa_estoque(cod_produto, localiz, quant)
                print "Retirado do estoque.\n"
            except:
                print "Erro na retirada do estoque."

        else:
            rep = 0

#--------------------------------------------------------------------

def auto_insert():
    print "Inserindo..."
    query.cursor.execute("insert into conta(nome, faturar) values (%s, %s)", ('Padrão', 100))
    codconta = query.last_insert_id()

    query.cursor.execute("insert into categoria(cod_conta_padrao, nome, tipo) values (%s, %s, %s)", (codconta, 'Camisetas', 1))
    codcategoria1 = query.last_insert_id()
    query.cursor.execute("insert into categoria(cod_conta_padrao, nome, tipo) values (%s, %s, %s)", (codconta, 'Livros', 2))
    codcategoria2 = query.last_insert_id()

    query.cursor.execute("insert into produto(cod_categoria, nome, descricao, preco, tamanho, ativo) values (%s, %s, %s, %s, %s, %s)", (codcategoria1, 'Camiseta Liberdade', 'Camiseta Paixão, Fogo e Glória - Liberdade', 25, 'P', 1))
    codproduto = query.last_insert_id()
    query.cursor.execute("insert into estoque(cod_produto, localiz, quantidade) values (%s, %s, %s)", (codproduto, 'PAD', 5))

    query.cursor.execute("insert into produto(cod_categoria, nome, descricao, preco, tamanho, ativo) values (%s, %s, %s, %s, %s, %s)", (codcategoria1, 'Camiseta Liberdade', 'Camiseta Paixão, Fogo e Glória - Liberdade', 25, 'M', 1))
    codproduto = query.last_insert_id()
    query.cursor.execute("insert into estoque(cod_produto, localiz, quantidade) values (%s, %s, %s)", (codproduto, 'PAD', 5))

    query.cursor.execute("insert into produto(cod_categoria, nome, descricao, preco, tamanho, ativo) values (%s, %s, %s, %s, %s, %s)", (codcategoria1, 'Camiseta Liberdade', 'Camiseta Paixão, Fogo e Glória - Liberdade', 25, 'G', 1))
    codproduto = query.last_insert_id()
    query.cursor.execute("insert into estoque(cod_produto, localiz, quantidade) values (%s, %s, %s)", (codproduto, 'PAD', 5))

    query.cursor.execute("insert into produto(cod_categoria, nome, descricao, preco, autor, editora, ativo) values (%s, %s, %s, %s, %s, %s, %s)", (codcategoria2, 'Bom dia, Espírito Santo', 'Livro que fala sobre...', 22, 'Benny Hinn', 'Editora', 1))
    codproduto = query.last_insert_id()
    query.cursor.execute("insert into estoque(cod_produto, localiz, quantidade) values (%s, %s, %s)", (codproduto, 'PAD', 3))

    query.cursor.execute("insert into produto(cod_categoria, nome, descricao, preco, autor, editora, ativo) values (%s, %s, %s, %s, %s, %s, %s)", (codcategoria2, 'Os caçadores de Deus', 'Livro que fala sobre...', 18, 'Tommy Tenney', 'Editora', 1))
    codproduto = query.last_insert_id()
    query.cursor.execute("insert into estoque(cod_produto, localiz, quantidade) values (%s, %s, %s)", (codproduto, 'PAD', 3))

    query.cursor.execute("insert into clientes(nome) values (%s)", ('Cliente padrão'))
    query.cursor.execute("insert into clientes(nome) values (%s)", ('Augusto Men'))

#locacao

    query.cursor.execute("insert into categoria_dvd(descricao, preco) values (%s, %s)", ('Superlançamento', 3))
    query.cursor.execute("insert into categoria_dvd(descricao, preco) values (%s, %s)", ('Lançamento', 2))
    codcategoria_dvd = query.last_insert_id()
    
    query.cursor.execute("insert into generodvd(descricao) values (%s)", ('Biblico'))
    codgenero_dvd = query.last_insert_id()
    
    quantidade_dvds = 2
    query.cursor.execute("insert into filme(cod_genero, cod_categoria, titulo, quantidade) values (%s, %s, %s, %s)", (codgenero_dvd, codcategoria_dvd, 'Desafiando Gigantes', quantidade_dvds ))
    codfilme = query.last_insert_id()
    
    for quant in range(quantidade_dvds):
        query.cursor.execute("insert into dvd(cod_filme) values (%s)", (codfilme))
    
    query.bd.commit()

    print "Pronto."

#--------------------------------------------------------------------

while (1):
    print """
1 - Clientes
2 - Gêneros
3 - Categoria de DVD
4 - Filmes
5 - DVDs
6 - Locações

7 - Contas
8 - Categorias
9 - Produtos
10 - Estoque

A - Auto insert
0 - Sair
Opção: """

    op=raw_input().upper()
    if op=='1': # Clientes
        prompt_clientes()

    elif op=='2': # Gêneros
        prompt_generos()

    elif op=='3': # Categoria DVD
        prompt_categoria_dvd()

    elif op=='4': # Filmes
        prompt_filmes()

    elif op=='5': # DVD
        prompt_dvds()

    elif op=='6': # Locações
        prompt_locados()

    elif op=='7': # Conta
        prompt_contas()

    elif op=='8': # Categorias
        prompt_categorias()

    elif op=='9': # Produtos
        prompt_produtos()

    elif op=='10': # Estoque
        prompt_estoque()

    elif op=='A': # Auto insert
        auto_insert()

    else:
        if op=='0':
            break
