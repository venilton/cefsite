import sys
import MySQLdb

import dblogin

class Modelo:
	def __init__(self):
		self.conecta()
		
	def conecta(self):
		global bd
		global cursor
		try:
			bd = MySQLdb.connect('localhost',dblogin.user,dblogin.passwd)
			bd.select_db(dblogin.dbname)
			cursor = bd.cursor()
			
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit (1)

		#! Aqui se declaram as tabelas
		self.clientes = Cliente(bd, cursor, 'clientes')
		self.filmes = Filme(bd, cursor, 'filme')
		self.generos = Genero(bd, cursor, 'generodvd')
		self.dvds = DVD(bd, cursor, 'dvd')
		self.locados = Locacao(bd, cursor, 'locados')

		self.caixas = Caixa(bd, cursor, 'caixa')
		self.categorias = Categoria(bd, cursor, 'categoria')
		self.produtos = Produto(bd, cursor, 'produto')
		self.estoque = Estoque(bd, cursor, 'estoque')


#Classe genérica
class Tabela:
	""" Classe genérica que define os comandos em uma tabela ou relacionamento. """
	def __init__(self, bd, cursor, nome_tabela):
		self.bd = bd
		self.cursor = cursor
		self.nome_tabela = nome_tabela
		self.all_fields = []

	def runSql(self, query, params = None):
		""" Roda um comando execute (insert, update, delete) no banco de dados. """
		cursor.execute(query, params)
		bd.commit()

	def runQuery(self, query, params = None):
		""" Roda uma consulta (select) no banco de dados. """
		cursor.execute(query, params)
		rows = cursor.fetchall()
		return rows

	def lastInsertId(self):
		cursor.execute('SELECT LAST_INSERT_ID()')
		ret = cursor.fetchall()
		return ret[0][0]

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

	def select_all(self):
		return self.select(self.all_fields)

	def insert_item():
		pass
	def update_item():
		pass
	def locate_item():
		pass

class Cliente(Tabela):
	def __init__(self, bd, cursor, nome_tabela='clientes'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_cliente', 'nome', 'telefone', 'celular', 'endereco', 'bairro', 'cidade', 'estado', 'cep']

	def insert_item(self, name, telefone, celular, endereco, bairro, cidade, estado, cep):
		campos = {}
		campos['nome'] = name
		if telefone is not None:	campos['telefone'] = telefone
		if celular is not None:		campos['celular'] = celular
		if endereco is not None:	campos['endereco'] = endereco
		if bairro is not None:		campos['bairro'] = bairro
		if estado is not None:		campos['estado'] = estado
		if cep is not None:			campos['cep'] = cep

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_cliente, name, telefone, celular, endereco, bairro, cidade, estado, cep):
		campos = {}
		if name is not None:		campos['nome'] = name
		if telefone is not None:	campos['telefone'] = telefone
		if celular is not None:		campos['celular'] = celular
		if endereco is not None:	campos['endereco'] = endereco
		if bairro is not None:		campos['bairro'] = bairro
		if estado is not None:		campos['estado'] = estado
		if cep is not None:			campos['cep'] = cep

		return self.update(campos, {'cod_cliente': cod_cliente})

	def locate_item(self, name):
		return self.runQuery("SELECT * FROM %s WHERE nome like '%%%s%%'" % (self.nome_tabela, name))

class Caixa(Tabela):
	def __init__(self, bd, cursor, nome_tabela='caixa'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_caixa', 'nome', 'faturar']

	def insert_item(self, nome, faturar):
		campos = {}
		if nome is not None:		campos['nome'] = nome
		if faturar is not None:		campos['faturar'] = faturar

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_caixa, nome, faturar):
		campos = {}
		if nome is not None:		campos['nome'] = nome
		if faturar is not None:		campos['faturar'] = faturar

		return self.update(campos, {'cod_caixa': cod_caixa })

	def locate_item(self, name):
		return self.runQuery("SELECT * FROM %s WHERE nome like '%%%s%%'" % (self.nome_tabela, name))

class Filme(Tabela):
	def __init__(self, bd, cursor, nome_tabela='filme'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_filme', 'cod_genero', 'titulo', 'quantidade']

	def insert_item(self, cod_genero, titulo, quantidade):
		campos = {}
		if cod_genero is not None:	campos['cod_genero'] = cod_genero
		if titulo is not None:		campos['titulo'] = titulo
		if quantidade is not None:	campos['quantidade'] = quantidade

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_filme, cod_genero, titulo, quantidade):
		campos = {}
		if cod_genero is not None:	campos['cod_genero'] = cod_genero
		if titulo is not None:		campos['titulo'] = titulo
		if quantidade is not None:	campos['quantidade'] = quantidade

		return self.update(campos, {'cod_filme': cod_filme})

	def locate_item(self, name):
		return self.runQuery("SELECT * FROM %s WHERE nome like '%%%s%%'" % (self.nome_tabela, name))

class Genero(Tabela):
	def __init__(self, bd, cursor, nome_tabela='generodvd'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_genero', 'descricao']

	def insert_item(self, descricao):
		campos = {}
		if descricao is not None:	campos['descricao'] = descricao

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_genero, descricao):
		campos = {}
		if descricao is not None:	campos['descricao'] = descricao

		return self.update(campos, {'cod_genero': cod_genero })

	def locate_item(self, descricao):
		return self.runQuery("SELECT * FROM %s WHERE descricao like '%%%s%%'" % (self.nome_tabela, descricao))

class DVD(Tabela):
	def __init__(self, bd, cursor, nome_tabela='dvd'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_dvd', 'cod_filme']

	def insert_item(self, cod_filme):
		campos = {}
		if cod_filme is not None:	campos['cod_filme'] = cod_filme

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_dvd, cod_filme):
		campos = {}
		if cod_filme is not None:	campos['cod_filme'] = cod_filme

		return self.update(campos, {'cod_dvd': cod_dvd })

class Locacao(Tabela):
	def __init__(self, bd, cursor, nome_tabela='locados'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['idcod', 'cod_cliente', 'cod_dvd', 'retirada', 'devolucao', 'expire_date', 'status_dvd']

	def select_locados(self):
		return self.runQuery("SELECT idcod, cod_dvd, cod_cliente, retirada, expire_date FROM " + self.nome_tabela + " WHERE status_dvd = '0'")

	def select_locados_atrasados(self):
		return self.runQuery("SELECT idcod, cod_dvd, cod_cliente, retirada, expire_date FROM locados WHERE status_dvd = '0' AND expire_date < CURDATE()")

	def locate_locados(self, cod_dvd):
		return self.runQuery("SELECT idcod FROM " + self.nome_tabela + " WHERE status_dvd = '0' AND cod_dvd= %s", (cod_dvd))

	def insert_locacao(self, cod_cliente, cod_dvd, dias):
		runSql('INSERT INTO ' + self.nome_tabela + ' (cod_cliente, cod_dvd, retirada, expire_date) VALUES (%s, %s, NOW(), DATE_ADD(CURDATE( ), INTERVAL %s DAY))', (cod_cliente, cod_dvd, dias))
		return self.lastInsertId()

	def insert_devolucao(self, idcod):
		return self.runSql("UPDATE " + self.nome_tabela + " SET status_dvd = %s, devolucao = NOW() where idcod=%s", ('1', idcod))

	def update_item(self, cod_dvd, cod_filme):
		campos = {}
		if cod_filme is not None:	campos['cod_filme'] = cod_filme

		return self.update(campos, {'cod_dvd': cod_dvd })

class Categoria(Tabela):
	def __init__(self, bd, cursor, nome_tabela='categoria'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_categoria', 'cod_caixa_padrao', 'nome', 'cod_categoria_pai']

	def insert_item(self, cod_caixa_padrao, nome, cod_categoria_pai):
		campos = {}
		if cod_caixa_padrao is not None:	campos['cod_caixa_padrao'] = cod_caixa_padrao
		if nome is not None:				campos['nome'] = nome
		if cod_categoria_pai is not None:	campos['cod_categoria_pai'] = cod_categoria_pai

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_categoria, cod_caixa_padrao, nome, cod_categoria_pai):
		campos = {}
		if cod_caixa_padrao is not None:	campos['cod_caixa_padrao'] = cod_caixa_padrao
		if nome is not None:				campos['nome'] = nome
		if cod_categoria_pai is not None:	campos['cod_categoria_pai'] = cod_categoria_pai

		return self.update(campos, {'cod_categoria': cod_categoria })

	def locate_item(self, name):
		return self.runQuery("SELECT * FROM %s WHERE nome like '%%%s%%'" % (self.nome_tabela, name))

class Produto(Tabela):
	def __init__(self, bd, cursor, nome_tabela='produto'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_produto', 'cod_categoria', 'nome', 'descricao', 'preco', 'ativo']

	def insert_item(self, cod_categoria, nome, descricao, preco, ativo):
		campos = {}
		if cod_categoria is not None:	campos['cod_categoria'] = cod_categoria
		if nome is not None:			campos['nome'] = nome
		if descricao is not None:		campos['descricao'] = descricao
		if preco is not None:			campos['preco'] = preco
		if ativo is not None:			campos['ativo'] = ativo

		self.insert(campos)
		return self.lastInsertId()

	def update_item(self, cod_produto, cod_categoria, nome, descricao, preco, ativo):
		campos = {}
		if cod_categoria is not None:	campos['cod_categoria'] = cod_categoria
		if nome is not None:			campos['nome'] = nome
		if descricao is not None:		campos['descricao'] = descricao
		if preco is not None:			campos['preco'] = preco
		if ativo is not None:			campos['ativo'] = ativo

		return self.update(campos, {'cod_produto': cod_produto })

	def locate_item(self, nome):
		return self.runQuery("SELECT * FROM %s WHERE nome like '%%%s%%'" % (self.nome_tabela, nome))

class EstoqueError(Exception): pass

class Estoque(Tabela):
	def __init__(self, bd, cursor, nome_tabela='estoque'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
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
		params = [cod_produto]

		sql1 = "SELECT sum(quantidade) FROM %s" % self.nome_tabela
		sql1 += " WHERE cod_produto=%s"
		if localiz:
			sql1 += " AND localiz=%s"
			params.append(localiz)

		rset = self.runQuery(sql1, localiz)
		if rset:
			return rset[0][0] #Primeiro registro, primeiro campo
		else:
			return None

class Pedido(Tabela):
	def __init__(self, bd, cursor, nome_tabela='pedido'):
		Tabela.__init__(self, bd, cursor, nome_tabela)
		self.all_fields = ['cod_pedido', 'cod_cliente', 'datahora', 'status_pedido']

	def novo_pedido(self):
		pass

