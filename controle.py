# coding: utf-8

import gtk
import pygtk
pygtk.require('2.0')
from datetime import date

from querys import Modelo
from login import Login

#ExceÃ§Ãµes
class ControleError(Exception): pass
class EmBranco(ControleError):pass
class CodigoInvalido(ControleError):pass
class PedidoError(ControleError):pass

class Controle:
    def __init__(self):
        self.status = False
        self.main_status = False
        self.notify_text = ''
        self.cliente_encontrado = False
        self.dadoscliente = [0][0]
    
    def set_modelo(self, modelo):
        self.modelo = modelo
    
    def set_interface(self, interface):
        self.interface = interface
    
    def start(self):
        self.interface.show()
        
    def logoff(self):        
        self.interface.w_login.show()
     
    def get_notify_label(self, notify_label):
            self.notify_label = notify_label
    
    def get_main_notify_label(self, notify_label):
            self.main_notify_label = notify_label
    
    def notify(self):
        if self.status == True:
            self.notify_label.set_text(self.notify_text)
            self.status = False
            return True
        else:
            self.notify_label.set_text(self.notify_text)
            return False

    def main_notify(self):
        if self.main_status == True:
            self.main_notify_label.set_text(self.notify_text)
            self.main_status = False
            return True
        else:
            return False
            
    def toInt(self, cod):
        try:
            cod = int(cod)
        except:
            self.notify_text = 'ERRO : campo CÃ“DIGO deve conter apenas nÃºmeros!'
            self.status = False
            raise CodigoInvalido , 'CÃ³digo deve conter apenas nÃºmeros'
        return cod
        
    def cliente_localizado(self):
        if self.cliente_encontrado == True:
            self.cliente_encontrado = False
            return True , self.dadoscliente
        else:
            return False, self.dadoscliente
        
    def cadastra_cliente(self, cod_cliente, name, telefone, celular, endereco, bairro, cidade, estado, cep, editando):
        if name == '':
            self.notify_text = 'ERRO : Campo NOME precisa ser preenchido!'
            self.status = True
            raise  EmBranco , 'Nome deve ser preenchido'
        elif editando == True:
            self.modelo.clientes.update_item(cod_cliente, name, telefone, celular, endereco, bairro, cidade, estado, cep)
            self.notify_text = 'Cliente ' + name +' Editado com sucesso!'
            self.status = True
        else:    
            self.modelo.clientes.insert_item(name, telefone, celular, endereco, bairro, cidade, estado, cep)
            self.notify_text = 'Cliente ' + name +' cadastrado com sucesso!'
            self.status = False
            self.main_status = True
        
    def locate_clientes(self):
        rows = self.modelo.clientes.select_all()
        return rows
    
    def listar_cliente(self,cod):
        cod = self.toInt(cod)
        rows = self.modelo.clientes.select_cliente(cod)
        if rows == ():
            self.notify_text = 'ERRO : Cliente nÃ£o Cadastrado!'
            self.status = False
            raise CodigoInvalido,  'CÃ³digo nÃ£o cadastrado'
        self.status = True
        return rows
    
    def alugar(self, cod_cliente, cod_dvd):
        cod_caixa = int(0)
        today = date.today()
        if date(today.year, today.month, today.day).weekday() == 6 : # Sunday
            dias = 2  # Devolução na terça
        elif date(today.year, today.month, today.day).weekday() == 1: # Tuesday
            dias = 5 # Devolução no proximo domingo
        else:
            dias = 7 #FixMe
    
        if cod_cliente =='':
            self.notify_text = 'ERRO : campo CÃ“DIGO CLIENTE precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'CÃ³digo deve ser preenchido'
        else:
            cod_cliente = self.toInt(cod_cliente)
            
        if cod_dvd == '':
            self.notify_text = 'ERRO : campo CÃ“DIGO DVD precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'CÃ³digo deve ser preenchido'
        
        else:
            cod_dvd =self.toInt(cod_dvd)
        
        dvds = self.listar_titulo_filme(cod_dvd)
        if dvds != ():  
            locado = self.modelo.locados.locate_locados(cod_dvd)
            if locado == ():
                self.modelo.locados.insert_locacao(cod_caixa, cod_cliente, cod_dvd, dias)
                self.notify_text = 'LocaÃ§Ã£o realizada com sucesso!'
                self.status = False
                self.main_status = True
                return
            else:
                self.notify_text = 'ERRO : DvD cod = %s jÃ¡ estÃ¡ Alugado!'%(cod_dvd)
                self.status = True
        else:
            self.notify_text = 'ERRO : DvD cod = %s nÃ£o Cadastrado!'%(cod_dvd)
            self.status = True
        
    def devolucao(self,cod_dvd):
        if cod_dvd != '':
            cod_dvd = self.toInt(cod_dvd)
        else:
            self.notify_text = 'ERRO : Campo CÃ“DIGO precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'CÃ³digo deve ser preenchido'
        
        cods = self.modelo.locados.select_locados()
        for cod in cods:
            if cod_dvd == cod[1]:
                self.modelo.locados.insert_devolucao(cod[0])
                self.notify_text = 'Devolução realizada com sucesso!'
                self.status = True
                return
        self.notify_text = 'ERRO: DVD cod = %s não está alugado!'%(cod_dvd)
        self.status = False
        
    def cadastra_genero_dvd(self,descricao):
        self.modelo.generos.insert_item(descricao)
        return True
    
    def listar_genero_dvd(self):
        rows = self.modelo.generos.select_all()
        return rows
    
    def popular_combo_genero(self):
        rows=self.modelo.generos.select_all()
        return rows
    
    def cadastra_filme(self, genero_ativo, generos, titulo, quantidade):
        if genero_ativo >= 0:  
            genero = generos[genero_ativo][1]
            cod_genero = self.modelo.generos.select_genero_desc(genero)
            cod_filme = self.modelo.filmes.insert_item(cod_genero[0][0], titulo, quantidade)
            for quant in range(quantidade):
                self.modelo.dvds.insert_item(cod_filme)
            return True
        else:
            return False
        
    def listar_locados(self):
        rows = self.modelo.locados.select_locados()
        return rows
        
    def listar_titulo_filme(self,codigo):
        rows = self.modelo.dvds.select_dvd(codigo)
        return rows
    
    def listar_atrasados(self):
        rows = self.modelo.locados.select_locados_atrasados()
        return rows
    
    def listar_dvd(self, cod, quant_itens, lista):
        cod = self.toInt(cod) 
        for iten in range(quant_itens):
            treeiter = lista.get_iter(iten)
            cod_inlista = int(lista.get_value(treeiter, 0))
            if cod == cod_inlista :
                self.status = False
                self.notify_text = 'DvD já está inserido na lista de locação'
                raise CodigoInvalido,  'Código em uso'
        dvd = self.modelo.dvds.select_dvd(cod)
        if dvd != ():  
            locado = self.modelo.locados.locate_locados(cod)
            if locado == ():
                self.status = True
            else:
                self.notify_text = 'ERRO : DvD cod = %s jÃ¡ estÃ¡ Alugado!'%(cod)
                self.status = False
                raise CodigoInvalido,  'CÃ³digo em uso'
        else:
            self.notify_text = 'ERRO : DvD cod = %s nÃ£o Cadastrado!'%(cod)
            self.status = False
            raise CodigoInvalido,  'CÃ³digo nÃ£o cadastrado'
        return dvd

	# Loja
	def novo_pedido(self, cod_cliente):
		cod_pedido = self.modelo.pedidos.novo_pedido(cod_cliente)
		return cod_pedido

	def incluir_itens(self, cod_pedido, itens):
		""" Inclui um ou mais itens no pedido. itens deve ser uma lista de dicionários com os campos. """

		status = self.modelo.pedidos.status_pedido(cod_pedido)
		if not status:
			raise CodigoInvalido, "Pedido não encontrado."
		elif status == '0':
			for item in itens:
				item['item'] = self.modelo.item_pedidos.add_item(cod_pedido, item['cod_produto'], item['localiz'], item['cod_caixa'], item['quantidade'], item['preco_unit'], item['desconto'])
		else:
			raise PedidoError, "Só é possível adicionar itens em pedidos em aberto."

	def fechar_pedido(self, cod_pedido):
		""" Fecha o pedido especificado, dando baixa em todos os produtos contidos nele. """

		status = self.modelo.pedidos.status_pedido(cod_pedido)
		if not status:
			raise CodigoInvalido, "Pedido não encontrado."
		elif status == '0':
			self.modelo.begin_transaction()
			try:
				rows = self.modelo.item_pedido.get_itens(cod_pedido)
				for row in rows:
					self.modelo.estoque.baixa_estoque(row['cod_produto'], row['localiz'], row['quantidade'])

				self.modelo.pedidos.fechar_pedido(cod_pedido)
			except:
				self.modelo.rollback()
				raise

			self.modelo.end_transaction()
		else:
			raise PedidoError, "Só é possível fechar pedidos em aberto."

	def cliente_devolucao(self):
        return self.cod_cliente_devolucao
        
    def dvd_listado_check(self):
        return self.listado
        
    def listar_dvds_locados(self, cod_dvd, quant_itens,  lista):
        self.listado = False
        if cod_dvd != '':
            cod_dvd = self.toInt(cod_dvd)
        else:
            self.notify_text = 'ERRO : Campo CÓDIGO precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        if lista == []:
            self.cod_cliente_devolucao = ''
            #Busca cod do cliente
            cods = self.modelo.locados.select_locados()
            for cod in cods:
                if cod_dvd == cod[1]:
                    self.cod_cliente_devolucao = cod[2]
                    self.status = True
                    break
            if self.cod_cliente_devolucao == '':
                self.notify_text = 'ERRO : DvD cod = %s não está Alugado!'%(cod_dvd)
                self.status = False
                raise CodigoInvalido,  'Código invalido'
            else:    
                #Busca dvds alugados pelo cliente        
                locados = self.modelo.locados.select_locados_porcliente(self.cod_cliente_devolucao)
                dvds = []
                for locado in locados:
                    dvd = self.modelo.dvds.select_dvd(locado[1])
                    dvds.append(dvd)
        else:
            for cods in lista:
                cod_inlista =cods.cod
                if cod_inlista == cod_dvd :
                    self.status = True
                    self.listado = True
                    cods.check = True
                    break
            if self.listado == False:
                self.notify_text = 'ERRO : DvD cod = %s não está Alugado para este Cliente!'%(cod_dvd)
                self.status = False
                raise CodigoInvalido,  'Código invalido'
        return dvds