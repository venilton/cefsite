import sys
import MySQLdb

class Modelo:
    def __init__(self):
        self.conecta()
        
    def conecta(self):
        global bd
        global cursor
        try:
            bd = MySQLdb.connect('localhost','marcos','marcos123')
            bd.select_db('cefshop')
            cursor = bd.cursor()
            
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1) 

    def insert_cliente(self,name):
        cursor.execute ('INSERT INTO clientes (nome) VALUES (%s)',(name))
        bd.commit()

    def select_all_clientes(self):
        cursor.execute ("SELECT cod_cliente, nome FROM clientes")
        rows = cursor.fetchall ()
        return rows

    def locate_cliente(self,name):
        cursor.execute ('SELECT nome, LOCATE(%s,nome) FROM clientes', name)
        rows = cursor.fetchall ()
        return rows

    def select_cliente(self,cod):
        cursor.execute ('SELECT cod_cliente, nome FROM clientes WHERE cod_cliente = %s', cod)
        rows = cursor.fetchall ()
        return rows

    def insert_generodvd(self,name):
        cursor.execute ('INSERT INTO generodvd (descricao) VALUES (%s)',(name))
        bd.commit()

    def select_all_generodvd(self):
        cursor.execute ("SELECT cod_genero, descricao FROM generodvd")
        rows = cursor.fetchall ()
        return rows

    def select_generodvd(self,name):
        cursor.execute ('SELECT cod_genero FROM generodvd WHERE descricao = %s', name)
        rows = cursor.fetchall ()
        return rows


    def insert_filme(self,genero,name,quantidade):
        cursor.execute ('INSERT INTO filme (cod_genero, titulo, quantidade) VALUES (%s,%s,%s)',(genero,name,quantidade))
        bd.commit()
        cursor.execute ('SELECT LAST_INSERT_ID( )')
        cod_filme= cursor.fetchall ()
        return cod_filme

    def select_all_filme(self):
        cursor.execute ("SELECT filme.cod_filme, generodvd.descricao, filme.titulo, filme.quantidade FROM generodvd,filme WHERE filme.cod_genero = generodvd.cod_genero")
        rows = cursor.fetchall ()
        return rows

    def insert_dvd(self,cod_filme):
        cursor.execute ('INSERT INTO dvd (cod_filme) VALUES (%s)',(cod_filme))
        bd.commit()

    def select_all_dvd(self):
        cursor.execute ("SELECT dvd.cod_dvd, filme.titulo FROM dvd, filme WHERE filme.cod_filme = dvd.cod_filme")
        rows = cursor.fetchall ()
        return rows

    def select_dvd(self,cod):
        cursor.execute ("SELECT dvd.cod_dvd, filme.titulo FROM dvd, filme WHERE filme.cod_filme = dvd.cod_filme AND dvd.cod_dvd = %s",(cod))
        rows = cursor.fetchall ()
        return rows


    def insert_locacao(self,cod_cliente, cod_dvd, dias):
        cursor.execute ('INSERT INTO locados (cod_cliente, cod_dvd,retirada,expire_date) VALUES (%s,%s,NOW( ),DATE_ADD(CURDATE( ),INTERVAL %s DAY))',(cod_cliente, cod_dvd, dias))
        bd.commit()

    def select_all_locados(self):
        cursor.execute ("SELECT cod_dvd ,retirada, expire_date, devolucao  FROM locados ")
        rows = cursor.fetchall ()
        return rows

    def select_locados(self):
        cursor.execute ("SELECT locados.idcod, locados.cod_dvd, locados.cod_cliente, clientes.nome ,locados.retirada, locados.expire_date FROM locados, dvd, clientes WHERE locados.status = '0' AND dvd.cod_dvd = locados.cod_dvd AND clientes.cod_cliente = locados.cod_cliente")
        rows = cursor.fetchall ()
        return rows

    def locate_locados(self,cod_dvd):
        cursor.execute ("SELECT cod_dvd FROM locados WHERE status = '0' AND cod_dvd= %s",(cod_dvd))
        rows = cursor.fetchall ()
        return rows

    def insert_devolucao(self,idcod):
        cursor.execute ("""
               UPDATE locados SET status = %s
               WHERE idcod = %s
             """, ('1', idcod))
        bd.commit()
    
    def select_locados_atrasados(self):
        cursor.execute ("SELECT locados.idcod, locados.cod_dvd, locados.cod_cliente, clientes.nome ,locados.retirada, locados.expire_date FROM locados, dvd, clientes WHERE locados.status = '0' AND locados.expire_date < CURDATE() AND dvd.cod_dvd = locados.cod_dvd AND clientes.cod_cliente = locados.cod_cliente")
        rows = cursor.fetchall ()
        return rows
