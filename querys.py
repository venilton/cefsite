import sys
import MySQLdb

import dblogin

class Modelo:
    def __init__(self):
        self.conecta()
        
    def conecta(self):
        try:
            self.bd = MySQLdb.connect('localhost',dblogin.user,dblogin.passwd)
            self.bd.select_db(dblogin.dbname)
            self.cursor = self.bd.cursor()
            
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)

        self.in_transaction = 0

        #! Aqui se declaram as tabelas
        self.clientes = Cliente(self, 'clientes')
        self.filmes = Filme(self, 'filme')
        self.generos = Genero(self, 'generodvd')
        self.categorias_dvd = Categoria_dvd(self, 'categoria_dvd')
        self.dvds = DVD(self, 'dvd')
        self.locados = Locacao(self, 'locados')

        self.caixa = Caixa(self, 'caixa')
        self.contas = Conta(self, 'conta')
        self.categorias = Categoria(self, 'categoria')
        self.produtos = Produto(self, 'produto')
        self.estoque = Estoque(self, 'estoque')
        self.pedidos = Pedido(self, 'pedido')
        self.item_pedidos = ItemPedido(self, 'itempedido')

    def last_insert_id(self):
        self.cursor.execute('SELECT LAST_INSERT_ID()')
        ret = self.cursor.fetchall()
        return ret[0][0]

        def begin_transaction(self):
            """ Inicia uma nova transação. """
            self.in_transaction += 1

    def end_transaction(self):
        """ Termina uma transação (realiza commit caso não haja mais transações abertas). """
        if self.in_transaction == 0:
            raise Exception, "Nenhuma transação aberta."
        elif self.in_transaction == 1:
            self.bd.commit()

        self.in_transaction -= 1

    def rollback(self):
        """ Realiza um rollback e termina quaisquer transações abertas. """
        self.bd.rollback()
        self.in_transaction = 0

#Classe genérica
class Tabela:
    """ Classe genérica que define os comandos em uma tabela ou relacionamento. """
    def __init__(self, modelo, nome_tabela):
        self.modelo = modelo
        self.nome_tabela = nome_tabela
        self.all_fields = []

    def runSql(self, query, params = None):
        """ Roda um comando execute (insert, update, delete) no banco de dados. """
        self.modelo.cursor.execute(query, params)
        if self.modelo.in_transaction == 0:
            #Nenhuma transação aberta: realiza auto-commit
            self.modelo.bd.commit()

    def runQuery(self, query, params = None):
        """ Roda uma consulta (select) no banco de dados. """
        self.modelo.cursor.execute(query, params)
        rows = self.modelo.cursor.fetchall()
        return rows

    def select(self, campos, chaves = {}):
        """ Seleciona os campos especificados em campos dos registros especificados em chaves. """
        values = []
        sql1 = 'SELECT '
        for campo in campos:
            sql1 += campo + ', '
        sql1 = sql1[:-2] + ' FROM ' + self.nome_tabela

        if chaves:
            sql1 += ' WHERE '
            for chave in chaves:
                sql1 += chave + '=%s and '
                values.append(chaves[chave])

        return self.runQuery(sql1, values)

    def insert(self, campos):
        """ Insere um registro usando os valores do dicionário na tabela atual (nome_tabela). """
        sql1 = 'INSERT INTO ' + self.nome_tabela + ' ('
        sql2 = ' values ('
        values = []
        for campo in campos:
            sql1 += campo + ', '
            sql2 += '%s, '
            values.append(campos[campo])
        sql1 = sql1[:-2] + ')'
        sql2 = sql2[:-2] + ')'

        return self.runSql(sql1 + sql2, values)

    def update(self, campos, chaves={}):
        """ Atualiza o registro identificado por chaves usando os valores de campos na tabela atual (nome_tabela). """
        sql1 = 'UPDATE ' + self.nome_tabela + ' SET '
        values = []
        for campo in campos:
            sql1 += campo + '=%s, '
            values.append(campos[campo])
        sql1 = sql1[:-2] #tira o ', '

        if chaves:
            sql1 += ' WHERE '
            for chave in chaves:
                sql1 += chave + "=%s and "
                values.append(chaves[chave])
            sql1 = sql1[:-5] #tira o ' and '

        return self.runSql(sql1, values)

    def delete(self, chaves = {}):
        """ Delete os registros identificado por chaves usando os valores de campos na tabela atual (nome_tabela). """
        sql1 = 'DELETE FROM ' + self.nome_tabela

        if chaves:
            sql1 += ' WHERE '
            for chave in chaves:
                sql1 += chave + "=%s and "
                values.append(chaves[chave])
            sql1 = sql1[:-5] #tira o ' and '

        return self.runSql(sql1, values)

    def select_all(self):
        return self.select(self.all_fields)

    #Para ser implementado nas classes filhas
    def insert_item(): pass
    def update_item(): pass
    def locate_item(): pass
    def delete_item(): pass

class Cliente(Tabela):
    def __init__(self, modelo, nome_tabela='clientes'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_cliente', 'nome', 'telefone', 'celular', 'endereco', 'bairro', 'cidade', 'estado', 'cep']

    def insert_item(self, name, telefone, celular, endereco, bairro, cidade, estado, cep):
        campos = {}
        campos['nome'] = name
        if telefone is not None:    campos['telefone'] = telefone
        if celular is not None:        campos['celular'] = celular
        if endereco is not None:    campos['endereco'] = endereco
        if bairro is not None:        campos['bairro'] = bairro
        if cidade is not None:        campos['cidade'] = cidade
        if estado is not None:        campos['estado'] = estado
        if cep is not None:            campos['cep'] = cep

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_cliente, name, telefone, celular, endereco, bairro, cidade, estado, cep):
        campos = {}
        if name is not None:        campos['nome'] = name
        if telefone is not None:    campos['telefone'] = telefone
        if celular is not None:     campos['celular'] = celular
        if endereco is not None:    campos['endereco'] = endereco
        if bairro is not None:      campos['bairro'] = bairro
        if cidade is not None:      campos['cidade'] = cidade
        if estado is not None:      campos['estado'] = estado
        if cep is not None:         campos['cep'] = cep

        return self.update(campos, {'cod_cliente': cod_cliente})

    def locate_item(self, name):
        return self.runQuery("SELECT * FROM clientes WHERE nome like '%%%s%%'" % (name))

    def select_cliente(self, cod):
        return self.runQuery("SELECT * FROM clientes WHERE cod_cliente=%s", [cod])

class Conta(Tabela):
    def __init__(self, modelo, nome_tabela='conta'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_conta', 'nome', 'faturar']

    def insert_item(self, nome, faturar):
        campos = {}
        if nome is not None:     campos['nome'] = nome
        if faturar is not None:  campos['faturar'] = faturar

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_conta, nome, faturar):
        campos = {}
        if nome is not None:     campos['nome'] = nome
        if faturar is not None:  campos['faturar'] = faturar

        return self.update(campos, {'cod_conta': cod_conta })

class Caixa(Tabela):
    def __init__(self, modelo, nome_tabela='caixa'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_caixa', 'data_abertura', 'data_fechamento', 'saldo_inicial', 'saldo_total']

    def insert_item(self, cod_caixa, saldo_inicial):
        self.runSql('INSERT INTO caixa (cod_caixa, data_abertura, saldo_inicial) VALUES (%s, CURDATE(), %s)', (cod_caixa, saldo_inicial))
        return self.lastInsertId()

    def update_item(self, id, data_fechamento, saldo_total):
        campos = {}
        if data_fechamento is not None: campos['data_fechamento'] = data_fechamento
        if saldo_total is not None:     campos['saldo_total'] = saldo_total
        
        return self.update(campos, {'id': id })
        
    def locate_item(self):
        return self.runQuery('SELECT * FROM caixa WHERE data_fechamento is NULL' )
        
class Filme(Tabela):
    def __init__(self, modelo, nome_tabela='filme'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_filme', 'cod_genero', 'cod_categoria','titulo', 'quantidade']

    def insert_item(self, cod_genero, cod_categoria_dvd, titulo, quantidade):
        campos = {}
        if cod_genero is not None:          campos['cod_genero'] = cod_genero
        if cod_categoria_dvd is not None:   campos['cod_categoria'] = cod_categoria_dvd
        if titulo is not None:              campos['titulo'] = titulo
        if quantidade is not None:          campos['quantidade'] = quantidade

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_filme, cod_genero, cod_categoria_dvd, titulo, quantidade):
        campos = {}
        if cod_genero is not None:          campos['cod_genero'] = cod_genero
        if cod_categoria_dvd is not None:   campos['cod_categoria'] = cod_categoria_dvd
        if titulo is not None:              campos['titulo'] = titulo
        if quantidade is not None:          campos['quantidade'] = quantidade

        return self.update(campos, {'cod_filme': cod_filme})

    def locate_item(self, name):
        return self.runQuery("SELECT * FROM filme WHERE nome like '%%%s%%'" % (name))

class Genero(Tabela):
    def __init__(self, modelo, nome_tabela='generodvd'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_genero', 'descricao']

    def insert_item(self, descricao):
        campos = {}
        if descricao is not None:   campos['descricao'] = descricao

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_genero, descricao):
        campos = {}
        if descricao is not None:    campos['descricao'] = descricao

        return self.update(campos, {'cod_genero': cod_genero })

    def locate_item(self, descricao):
        return self.runQuery("SELECT * FROM generodvd WHERE descricao like '%%%s%%'" % (descricao))

    def select_genero(self, cod):
        return self.runQuery("SELECT * FROM generodvd WHERE cod_genero=%s", [cod])
    
    def select_genero_desc(self, descricao):
        return self.runQuery("SELECT * FROM generodvd WHERE descricao=%s", [descricao])

class Categoria_dvd(Tabela):
    def __init__(self, bd, cursor, nome_tabela='categoria_dvd'):
        Tabela.__init__(self, bd, cursor, nome_tabela)
        self.all_fields = ['cod_categoria', 'descricao', 'preco']

    def insert_item(self, descricao, preco):
        campos = {}
        if descricao is not None:   campos['descricao'] = descricao
        if preco is not None:       campos['preco'] = preco
        self.insert(campos)
        return self.lastInsertId()

    def update_item(self, descricao, preco):
        campos = {}
        if descricao is not None:   campos['descricao'] = descricao
        if preco is not None:       campos['preco'] = preco

        return self.update(campos, {'cod_genero': cod_genero })

    def locate_item(self, descricao):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE descricao like '%%%s%%'" % (descricao))

    def select_categoria_dvd(self, cod):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE cod_categoria=%s", [cod])
    
    def select_categoria_desc(self, descricao):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE descricao=%s", [descricao])

    def get_preco(self, cod):
        return self.runQuery("SELECT preco FROM categoria_dvd WHERE cod_categoria=%s", [cod])

class Categoria_dvd(Tabela):
    def __init__(self, modelo, nome_tabela='categoria_dvd'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_categoria', 'descricao', 'preco']
 
    def insert_item(self, descricao, preco):
        campos = {}
        if descricao is not None:   campos['descricao'] = descricao
        if preco is not None:       campos['preco'] = preco
        self.insert(campos)
        return self.lastInsertId()
 
    def update_item(self, descricao, preco):
        campos = {}
        if descricao is not None:   campos['descricao'] = descricao
        if preco is not None:       campos['preco'] = preco
 
        return self.update(campos, {'cod_genero': cod_genero })
 
    def locate_item(self, descricao):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE descricao like '%%%s%%'" % (descricao))
 
    def select_categoria_dvd(self, cod):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE cod_categoria=%s", [cod])
    
    def select_categoria_desc(self, descricao):
        return self.runQuery("SELECT * FROM categoria_dvd WHERE descricao=%s", [descricao])
 
    def get_preco(self, cod):
        return self.runQuery("SELECT preco FROM categoria_dvd WHERE cod_categoria=%s", [cod])
 
class DVD(Tabela):
    def __init__(self, modelo, nome_tabela='dvd'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_dvd', 'cod_filme']

    def insert_item(self, cod_filme):
        campos = {}
        if cod_filme is not None:   campos['cod_filme'] = cod_filme

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_dvd, cod_filme):
        campos = {}
        if cod_filme is not None:    campos['cod_filme'] = cod_filme

        return self.update(campos, {'cod_dvd': cod_dvd })

    def select_dvd(self, cod):
        return self.runQuery("SELECT d.cod_dvd, f.titulo, f.cod_categoria FROM dvd d, filme f WHERE f.cod_filme = d.cod_filme AND d.cod_dvd = %s", (cod))

class Locacao(Tabela):
    def __init__(self, modelo, nome_tabela='locados'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['idcod', 'cod_cliente', 'cod_dvd', 'retirada', 'devolucao', 'expire_date', 'status_dvd']

    def select_locados(self):
        return self.runQuery("SELECT idcod, cod_dvd, cod_cliente, retirada, expire_date FROM locados WHERE status_dvd = '0'")

    def select_locados_atrasados(self):
        return self.runQuery("SELECT idcod, cod_dvd, cod_cliente, retirada, expire_date FROM locados WHERE status_dvd = '0' AND expire_date < CURDATE()")

    def locate_locados(self, cod_dvd):
        return self.runQuery("SELECT idcod FROM locados WHERE status_dvd = '0' AND cod_dvd= %s", (cod_dvd))

    def insert_locacao(self, cod_caixa, cod_cliente, cod_dvd, dias):
        self.runSql('INSERT INTO locados (cod_caixa, cod_cliente, cod_dvd, retirada, expire_date) VALUES (%s, %s, %s, NOW(), DATE_ADD(CURDATE( ), INTERVAL %s DAY))', (cod_caixa, cod_cliente, cod_dvd, dias))
        return self.modelo.last_insert_id()

    def insert_devolucao(self, idcod):
        return self.runSql("UPDATE locados SET status_dvd = %s, devolucao = NOW() where idcod=%s", ('1', idcod))

    def update_item(self, cod_dvd, cod_filme):
        campos = {}
        if cod_filme is not None:    campos['cod_filme'] = cod_filme

        return self.update(campos, {'cod_dvd': cod_dvd })

class Categoria(Tabela):
    def __init__(self, modelo, nome_tabela='categoria'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_categoria', 'cod_conta_padrao', 'nome', 'cod_categoria_pai']

    def insert_item(self, cod_conta_padrao, nome, cod_categoria_pai):
        campos = {}
        if cod_conta_padrao is not None:    campos['cod_conta_padrao'] = cod_conta_padrao
        if nome is not None:                campos['nome'] = nome
        if cod_categoria_pai is not None:   campos['cod_categoria_pai'] = cod_categoria_pai

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_categoria, cod_conta_padrao, nome, cod_categoria_pai):
        campos = {}
        if cod_conta_padrao is not None:    campos['cod_conta_padrao'] = cod_conta_padrao
        if nome is not None:                campos['nome'] = nome
        if cod_categoria_pai is not None:   campos['cod_categoria_pai'] = cod_categoria_pai

        return self.update(campos, {'cod_categoria': cod_categoria })

    def locate_item(self, name):
        return self.runQuery("SELECT * FROM categoria WHERE nome like '%%%s%%'" % (name))

class Produto(Tabela):
    def __init__(self, modelo, nome_tabela='produto'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_produto', 'cod_categoria', 'nome', 'descricao', 'preco', 'ativo']

    def insert_item(self, cod_categoria, nome, descricao, preco, ativo):
        campos = {}
        if cod_categoria is not None:    campos['cod_categoria'] = cod_categoria
        if nome is not None:             campos['nome'] = nome
        if descricao is not None:        campos['descricao'] = descricao
        if preco is not None:            campos['preco'] = preco
        if ativo is not None:            campos['ativo'] = ativo

        self.insert(campos)
        return self.modelo.last_insert_id()

    def update_item(self, cod_produto, cod_categoria, nome, descricao, preco, ativo):
        campos = {}
        if cod_categoria is not None:    campos['cod_categoria'] = cod_categoria
        if nome is not None:             campos['nome'] = nome
        if descricao is not None:        campos['descricao'] = descricao
        if preco is not None:            campos['preco'] = preco
        if ativo is not None:            campos['ativo'] = ativo

        return self.update(campos, {'cod_produto': cod_produto })

    def locate_item(self, nome):
        return self.runQuery("SELECT * FROM produto WHERE nome like '%%%s%%'" % (nome))

class EstoqueError(Exception): pass

class Estoque(Tabela):
    def __init__(self, modelo, nome_tabela='estoque'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_produto', 'localiz', 'quantidade']

    def add_estoque(self, cod_produto, localiz, quantidade):
        campos = {}

        qatual = self.get_estoque(cod_produto, localiz)
        if qatual is None:
            #Nenhum registro do produto no localiz
            campos['cod_produto'] = cod_produto
            campos['localiz'] = localiz
            campos['quantidade'] = quantidade
            self.insert(campos)
        else:
            campos['quantidade'] = qatual + quantidade
            self.update(campos, { 'cod_produto': cod_produto, 'localiz': localiz })

    def baixa_estoque(self, cod_produto, localiz, quantidade):
        campos = {}

        qatual = self.get_estoque(cod_produto, localiz)
        if qatual is None or qatual < quantidade:
            raise EstoqueError, 'Quantidade em estoque insuficiente.'
        else:
            campos['quantidade'] = qatual - quantidade
            self.update(campos, { 'cod_produto': cod_produto, 'localiz': localiz })

    def get_estoque(self, cod_produto, localiz):
        """ Retorna o estoque de um produto (se for especificado, em um armazém). Retorna a quantidade em estoque,
            0 caso não haja nenhum item no estoque ou None caso haja registro do produto no estoque. """
        sql1 = "SELECT sum(quantidade) FROM estoque WHERE cod_produto=%s"
        params = [cod_produto]
        if localiz:
            sql1 += " AND localiz=%s"
            params.append(localiz)

        rset = self.runQuery(sql1, params)
        if rset:
            return rset[0][0] #Primeiro registro, primeiro campo
        else:
            return None

    def listar_estoque(self, cod_produto = None, localiz = None):
        params = []
        sql1 = """SELECT p.cod_produto, p.nome, e.localiz, e.quantidade
            FROM produto p, estoque e
            WHERE p.cod_produto=e.cod_produto"""
        if cod_produto:
            sql1 += " AND cod_produto=%s"
            params.append(cod_produto)
        if localiz:
            sql1 += " AND localiz=%s"
            params.append(localiz)

        rows = self.runQuery(sql1, params)
        return rows

class PedidoError(Exception): pass

class Pedido(Tabela):
    def __init__(self, modelo, nome_tabela='pedido'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_pedido', 'cod_cliente', 'datahora', 'status_pedido']

    def novo_pedido(self, cod_cliente):
        """ Inclui um novo pedido em branco """
        runSql('INSERT INTO pedido (cod_cliente, datahora, status_pedido) VALUES (%s, NOW(), %s)', (cod_cliente, '0'))
        return self.modelo.last_insert_id()

    def status_pedido(self, cod_pedido):
        rows = self.select(['status_pedido'], { 'cod_pedido': cod_pedido })
        if rows:
            return rows[0][0]
        else:
            return None

    def fechar_pedido(self, cod_pedido):
        """ Fecha o pedido gravado. """
        return self.update({ 'status_pedido': '1' }, { 'cod_pedido': cod_pedido })

    def cancelar_pedido(self, cod_pedido):
        """ Cancela o pedido (status_pedido = 2) """
        return self.update({ 'status_pedido': '2' }, { 'cod_pedido': cod_pedido })

class ItemPedido(Tabela):
    def __init__(self, modelo, nome_tabela='itempedido'):
        Tabela.__init__(self, modelo, nome_tabela)
        self.all_fields = ['cod_pedido', 'item', 'cod_produto', 'cod_conta', 'localiz', 'quantidade', 'preco_unit', 'desconto', 'total']

    def next_item(self, cod_pedido):
        """ Obtém o número do próximo item no pedido (1 se o pedido não tiver itens) """
        rows = self.runQuery("select max(item) from itempedido where cod_pedido=%s", (cod_pedido))
        if rows[0][0]:
            nitem = rows[0][0] + 1
        else:
            nitem = 1
        return nitem

    def add_item(self, cod_pedido, cod_produto, localiz, cod_conta=None, quantidade=None, preco_unit=None, desconto=None):
        nitem = self.next_item(cod_pedido)

        rows = self.runQuery("""
            SELECT c.cod_conta_padrao, p.preco, p.ativo
            FROM produto p, categoria c
            WHERE c.cod_categoria=p.cod_categoria and p.cod_produto=%s
            """, (cod_produto))
        if not rows:
            rows = [('', 0, 0)]
        campos = {}
        campos['cod_produto'] = cod_produto
        campos['localiz'] = localiz
        campos['cod_conta'] = cod_conta or rows[0][0]
        campos['preco_unit'] = preco_unit or rows[0][1]
        campos['quantidade'] = quantidade or 1
        campos['desconto'] = desconto or 0
        campos['total'] = campos['quantidade'] * campos['preco_unit'] - campos['desconto']

        self.insert(campos)
        return nitem

    def delete_item(self, cod_pedido, item):
        return self.delete({ 'cod_pedido': cod_pedido, 'item': item })

    def get_itens(self, cod_pedido):
        ret = []
        rows = self.select(self.all_fields, { 'cod_pedido': cod_pedido })
        for row in rows:
            campos = {}
            for i in range(len(self.all_fields)):
                campos[self.all_fields[i]] = row[i]
            ret.append(campos)
        return ret