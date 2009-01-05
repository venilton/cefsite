import sys
import MySQLdb

def connect():
    global bd
    global cursor
    try:
        bd = MySQLdb.connect('localhost','marcos','marcos123')
        bd.select_db('cefshop')
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
    print "Clientes...Feito."

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
    print " Generodvd...Feito."

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
    print " Filme...Feito."

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
    print " Dvd...Feito."

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
    print " locados...Feito."

if __name__ == '__main__':
    connect()
    #clientes()
    #generodvd()
    #filme()
    #dvd()
    locados()    
