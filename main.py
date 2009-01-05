# -*- coding: latin-1 -*-
from querys import Modelo
query = Modelo()
query.conecta()

def listar_clientes():
    rows=query.select_all_clientes()
    for row in rows:
        print "%s, %s" % (row[0], row[1])
    print "Numero de Clientes: %d" % len(rows)   


def listar_generos():
    rows=query.select_all_generodvd()
    for row in rows:
        print "%s, %s" % (row[0], row[1])
    print "Numero de Generos: %d" % len(rows)

def listar_filmes():
    rows=query.select_all_filme()
    for row in rows:
        print "%s, %s, %s, %s" % (row[0], row[1], row[2], row[3])
    print "Total de Filmes: %d" % len(rows)

def listar_dvd():
    rows=query.select_all_dvd()
    for row in rows:
        print "%s, %s" % (row[0], row[1])
    print "Numero de Dvds: %d" % len(rows)

def listar_locados():
    locados=query.select_locados()
  
    for locado in locados:
        titulo = query.select_dvd(locado[0])
        print "%s, %s, %s, %s , %s ,%s" % (locado[1],titulo[0][1], locado[2], locado[3], locado[4], locado[5])
    print "Numero de locações: %d" % len(locados)

def listar_locados_atrasados():
    rows=query.select_locados_atrasados2()
    for row in rows:
        print "%s, %s, %s, %s , %s" % (row[0], row[1], row[2], row[3], row[4])
    print "Numero de locações em atraso: %d" % len(rows)
    return rows



while (1):
    print """
       Digite:

       1 - Add Cliente  
       2 - Listar Clientes

       3 - Add Filme
       4 - Listar Filmes

       5 - Add Genero
       6 - Listar
       
       7 - Listar Dvd
       
       8 - Locar (Retirada)
       9 - Devolução

       10- Locados
       11- Atrasados
  
       0 - Sair    
    """
    op=raw_input()
    if op=='1': # Adicionar Clientes  
        name=raw_input('Digite o nome do Cliente\n')
        query.insert_cliente(name)

    elif op=='2': #Listar Clientes
        listar_clientes()

    elif op=='3': # Adicionar Filme 

        listar_generos()
            
        genero=raw_input('Selecione o genero:')
        name=raw_input('Titulo:\n')
        quantidade=int(raw_input('Quantidade:\n'))
        cod_filme=query.insert_filme(genero,name,quantidade)
        print "Codigo do filme %s" % cod_filme[0]
        for quant in range(quantidade):
            query.insert_dvd(cod_filme[0])
        
    elif op=='4': #Listar Filmes
        listar_filmes()

    elif op=='5': # Adicionar Generos 
        name=raw_input('Genero:\n')
        query.insert_generodvd(name)

    elif op=='6': #Listar Generos
        listar_generos()

    elif op=='7': #Listar dvd
        listar_dvd()

    elif op=='8': #Locar
            cod_cliente = raw_input('Cod do cliente:\n')
            cod_dvd = int(raw_input('Cod do DVD:\n'))

            locado = query.locate_locados(cod_dvd)

            if locado ==():
                dias = '7'
                query.insert_locacao(cod_cliente, cod_dvd, dias)
                
            else:
                print "Dvd já esta alugado"
                break
                    

    elif op=='9': #Devolucao
        
        cod_dvd = int(raw_input('Cod do DVD:\n'))
        cods=listar_locados()
        for cod in cods:
            print cod[1]
            if (cod_dvd == cod[1]):
                print "Devolucao OK..1"
                query.insert_devolucao(cod[0])
                break
        #else
        #   print "Nao alugado"
    
    elif op=='10': #Locados
        listar_locados()

    elif op=='11': #Atrasados
        listar_locados_atrasados()


    else:
        if op=='0':
            break
