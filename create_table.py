import sys
import MySQLdb

def connect():
    global bd
    global cursor
    try:
        bd = MySQLdb.connect('localhost',dblogin.user,dblogin.passwd)
        bd.select_db(dblogin.dbname)
        cursor = bd.cursor()
        print "Conectado."
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1) 

def clientes():
    cursor.execute ("DROP TABLE IF EXISTS clientes")
    cursor.execute ("""
        CREATE TABLE clientes
        (
   	    cod_cliente    INT UNSIGNED NOT NULL AUTO_INCREMENT,
   	    PRIMARY KEY (cod_cliente),
   	    nome    VARCHAR(30) NOT NULL 
	)
      """)
    print " clientes... feito."

def generodvd():
    cursor.execute ("DROP TABLE IF EXISTS generodvd")
    cursor.execute ("""
        CREATE TABLE generodvd
        (
   	    cod_genero    INT UNSIGNED NOT NULL AUTO_INCREMENT,
   	    PRIMARY KEY (cod_genero),
   	    descricao    VARCHAR(20) NOT NULL 
	)
      """)
    print " generodvd... feito."

def filme():
    cursor.execute ("DROP TABLE IF EXISTS filme")
    cursor.execute ("""
        CREATE TABLE filme
        (
   	    cod_filme    INT UNSIGNED NOT NULL AUTO_INCREMENT,
   	    PRIMARY KEY (cod_filme),
            cod_genero INT UNSIGNED NOT NULL,
   	    titulo    VARCHAR(20) NOT NULL,
            quantidade int(10)
	)
      """)
    print " filme... feito."

def dvd():
    cursor.execute ("DROP TABLE IF EXISTS dvd")
    cursor.execute ("""
        CREATE TABLE dvd
        (
   	    cod_dvd    INT UNSIGNED NOT NULL AUTO_INCREMENT,
   	    PRIMARY KEY (cod_dvd),
            cod_filme INT UNSIGNED NOT NULL
	)
      """)
    print " dvd... feito."

def locados():
    cursor.execute ("DROP TABLE IF EXISTS locados")
    cursor.execute ("""
        CREATE TABLE locados
        (
            idcod  INT UNSIGNED NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (idcod),
            cod_cliente INT UNSIGNED NOT NULL,
   	    cod_dvd    INT UNSIGNED NOT NULL,
            retirada DATETIME,
            devolucao DATETIME Default NULL,
            expire_date DATE,
            status int(2) Default '0'
	)
      """)
    print " locados... feito."

def categoria():
	cursor.execute ("DROP TABLE IF EXISTS categoria")
	cursor.execute ("""
		CREATE TABLE categoria (
		  cod_categoria INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
		  nome VARCHAR(30) NULL,
		  cod_categoria_pai INTEGER UNSIGNED NULL,
		  PRIMARY KEY(cod_categoria)
		)
	""")
	print " categoria... feito."

def produto():
	cursor.execute ("DROP TABLE IF EXISTS produto")
	cursor.execute ("""
		CREATE TABLE produto (
		  cod_produto INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
		  cod_categoria INTEGER UNSIGNED NOT NULL,
		  nome VARCHAR(40) NULL,
		  descricao TEXT NULL,
		  preco FLOAT(12,2) NULL,
		  ativo INTEGER NULL,
		  PRIMARY KEY(cod_produto),
		  INDEX produto_FKIndex1(cod_categoria)
		)
	""")
	print " pedido... feito."

def estoque():
	cursor.execute ("DROP TABLE IF EXISTS estoque")
	cursor.execute ("""
		CREATE TABLE estoque (
		  cod_produto INTEGER UNSIGNED NOT NULL,
		  armazem VARCHAR(4) NULL,
		  quantidade FLOAT(7,2) NULL DEFAULT 0,
		  PRIMARY KEY(cod_produto),
		  INDEX estoque_FKIndex1(cod_produto)
		)
	""")
	print " estoque... feito."

def pedido():
	cursor.execute ("DROP TABLE IF EXISTS pedido")
	cursor.execute ("""
		CREATE TABLE pedido (
		  cod_pedido INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
		  cod_cliente INTEGER UNSIGNED NOT NULL,
		  datahora DATETIME NULL,
		  status_pedido INTEGER NULL,
		  PRIMARY KEY(cod_pedido),
		  INDEX pedido_FKIndex1(cod_cliente)
		)
	""")
	print " pedido... feito."

def itempedido():
	cursor.execute ("DROP TABLE IF EXISTS itempedido")
	cursor.execute ("""
		CREATE TABLE itempedido (
		  cod_pedido INTEGER UNSIGNED NOT NULL,
		  item INTEGER UNSIGNED NOT NULL,
		  cod_produto INTEGER UNSIGNED NOT NULL,
		  quantidade FLOAT(7,3) NULL DEFAULT 1,
		  preco_unit FLOAT(12,2) NULL,
		  desconto FLOAT(12,2) NULL,
		  total FLOAT(12,2) NULL,
		  PRIMARY KEY(cod_pedido, item),
		  INDEX itempedido_FKIndex1(cod_pedido),
		  INDEX itempedido_FKIndex2(cod_produto)
		)
	""")
	print " itempedido... feito."

if __name__ == '__main__':
    connect()
    clientes()

    # Locadora
    generodvd()
    filme()
    dvd()
    locados()

    # Loja
    categoria()
    produto()
    estoque()
    pedido()
    itempedido()
