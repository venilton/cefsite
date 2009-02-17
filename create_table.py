import sys
import MySQLdb
import dblogin

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
    CREATE TABLE clientes (
      cod_cliente INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
      nome VARCHAR(50) NULL,
      telefone VARCHAR(15) NULL,
      celular VARCHAR(15) NULL,
      endereco VARCHAR(100) NULL,
      bairro VARCHAR(40) NULL,
      cidade VARCHAR(40) NULL,
      estado VARCHAR(2) NULL DEFAULT 'SP',
      cep VARCHAR(8) NULL,
      PRIMARY KEY(cod_cliente)
    )
      """)
    print " clientes... feito."

def conta():
    cursor.execute ("DROP TABLE IF EXISTS conta")
    cursor.execute ("""
        CREATE TABLE conta (
          cod_conta INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
          nome VARCHAR(20) NULL,
          faturar INTEGER UNSIGNED NULL,
          PRIMARY KEY(cod_conta)
        )
    """)
    print " conta... feito."

def caixa():
    cursor.execute ("DROP TABLE IF EXISTS caixa")
    cursor.execute ("""
        CREATE TABLE caixa (
          id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,  
          cod_caixa INTEGER UNSIGNED NOT NULL ,
          data_abertura DATE NOT NULL,
          data_fechamento  DATE NULL,
          saldo_inicial FLOAT NOT NULL,
          saldo_total FLOAT, 
          PRIMARY KEY(id)
        )
    """)
    print " caixa... feito."

def generodvd():
    cursor.execute ("DROP TABLE IF EXISTS generodvd")
    cursor.execute ("""
        CREATE TABLE generodvd
        (
        cod_genero	INT UNSIGNED NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (cod_genero),
        descricao	VARCHAR(20) NOT NULL 
    )
      """)
    print " generodvd... feito."

def categoria_dvd():
    cursor.execute ("DROP TABLE IF EXISTS categoria_dvd")
    cursor.execute ("""
        CREATE TABLE categoria_dvd 
        (
          cod_categoria INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
          descricao VARCHAR(30) NOT NULL,
          preco VARCHAR(12) NOT NULL,
          PRIMARY KEY(cod_categoria)
        )
    """)
    print " categoria_dvd... feito."

def filme():
    cursor.execute ("DROP TABLE IF EXISTS filme")
    cursor.execute ("""
        CREATE TABLE filme
        (
        cod_filme	INT UNSIGNED NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (cod_filme),
            cod_genero INT UNSIGNED NOT NULL,
            cod_categoria INT UNSIGNED NOT NULL,
        titulo	VARCHAR(40) NOT NULL,
            quantidade int(10)
    )
      """)
    print " filme... feito."

def dvd():
    cursor.execute ("DROP TABLE IF EXISTS dvd")
    cursor.execute ("""
        CREATE TABLE dvd
        (
        cod_dvd	INT UNSIGNED NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (cod_dvd),
            cod_filme INT UNSIGNED NOT NULL
    )
      """)
    print " dvd... feito."

def locados():
    cursor.execute ("DROP TABLE IF EXISTS locados")
    cursor.execute ("""
        CREATE TABLE locados (
          idcod INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
          cod_caixa INTEGER UNSIGNED NOT NULL,
          cod_dvd INTEGER UNSIGNED NOT NULL,
          cod_cliente INTEGER UNSIGNED NOT NULL,
          retirada DATETIME NULL,
          devolucao DATETIME NULL,
          expire_date DATE NULL,
          status_dvd INTEGER  Default '0',
          PRIMARY KEY(idcod),
          INDEX locados_FKIndex1(cod_cliente),
          INDEX locados_FKIndex2(cod_dvd),
          INDEX locados_FKIndex3(cod_caixa)
        )
    """)
    print " locados... feito."

def categoria():
	cursor.execute ("DROP TABLE IF EXISTS categoria")
	cursor.execute ("""
        CREATE TABLE categoria (
          cod_categoria INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
          cod_conta_padrao INTEGER UNSIGNED NOT NULL,
          nome VARCHAR(30) NULL,
          cod_categoria_pai INTEGER UNSIGNED NULL,
          tipo INTEGER UNSIGNED NULL,
          PRIMARY KEY(cod_categoria),
          INDEX categoria_FKIndex1(cod_conta_padrao)
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
          tamanho VARCHAR(4) NULL,
          autor VARCHAR(50) NULL,
          editora VARCHAR(40) NULL,
          ativo INTEGER NULL DEFAULT 1,
          PRIMARY KEY(cod_produto),
          INDEX produto_FKIndex1(cod_categoria)
        )
	""")
	print " produto... feito."

def estoque():
    cursor.execute ("DROP TABLE IF EXISTS estoque")
    cursor.execute ("""
        CREATE TABLE estoque (
          cod_produto INTEGER UNSIGNED NOT NULL,
          localiz VARCHAR(4) NOT NULL,
          quantidade FLOAT(8,3) NULL DEFAULT 0,
          PRIMARY KEY(cod_produto, localiz),
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
          cod_conta INTEGER UNSIGNED NOT NULL,
          localiz VARCHAR(4) NOT NULL,
          cod_produto INTEGER UNSIGNED NOT NULL,
          quantidade FLOAT(8,3) NULL DEFAULT 1,
          preco_unit FLOAT(12,2) NULL,
          desconto FLOAT(12,2) NULL,
          total FLOAT(12,2) NULL,
          PRIMARY KEY(cod_pedido, item),
          INDEX itempedido_FKIndex1(cod_pedido),
          INDEX itempedido_FKIndex2(cod_produto, localiz),
          INDEX itempedido_FKIndex3(cod_conta)
        )
    """)
    print " itempedido... feito."

if __name__ == '__main__':
    connect()
    clientes()
    conta()
    caixa()

    # Locadora
    generodvd()
    categoria_dvd()
    filme()
    dvd()
    locados()

    # Loja
    categoria()
    produto()
    estoque()
    pedido()
    itempedido()
