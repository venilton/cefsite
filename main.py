# -*- coding: latin-1 -*-

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

def prompt_caixas():
    tabela = query.caixas
    campos = tabela.all_fields[1:]
    prompt_table('caixas', tabela.all_fields[0], campos, tabela)

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
            

#--------------------------------------------------------------------

while (1):
    print """
    Digite:

    1 - Clientes
    2 - Gêneros
    3 - Filmes
    4 - DVDs
    5 - Locações

    6 - Caixas
    7 - Categorias
    8 - Produtos
    9 - Estoque

    0 - Sair	
    """
    op=raw_input()
    if op=='1': # Clientes
        prompt_clientes()

    elif op=='2': # Gêneros
        prompt_generos()

    elif op=='3': # Filmes
        prompt_filmes()

    elif op=='4': # DVD
        prompt_dvds()

    elif op=='5': # Locações
        prompt_locados()

    elif op=='6': # Caixa
        prompt_caixas()

    elif op=='7': # Categorias
        prompt_categorias()

    elif op=='8': # Produtos
        prompt_produtos()

    elif op=='9': # Estoque
        prompt_estoque()

    else:
        if op=='0':
            break
