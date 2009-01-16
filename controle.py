# coding: utf-8

import gtk
import pygtk
pygtk.require('2.0')
from datetime import date

from querys import Modelo
from main_base import Login

#Exceções
class ControleError(Exception): pass
class EmBranco(ControleError):pass
class CodigoInvalido(ControleError):pass

class Controle:
    def __init__(self):
        self.status = False
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
            
    def notify(self):
        if self.status == True:
            self.status = False
            return True , self.notify_text
        else:
            self.notify_label.set_text(self.notify_text)
            return False, self.notify_text
            
    def cliente_localizado(self):
        if self.cliente_encontrado == True:
            self.cliente_encontrado = False
            return True , self.dadoscliente
        else:
            return False, self.dadoscliente
        
    def cadastra_cliente(self, cod, name, editando):
        if name=='':
            self.notify_text = 'ERRO : Campo NOME precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Nome deve ser preenchido'
                
        else:
            if editando == True:
                self.modelo.update_cliente(cod, name)
                self.notify_text = 'Cliente ' + name +' Editado com sucesso!'
            else:    
                self.modelo.insert_cliente(name)
                self.notify_text = 'Cliente ' + name +' cadastrado com sucesso!'
                self.status = True
            
    def locate_clientes(self):
        rows = self.modelo.select_all_clientes()
        return rows
    
    def listar_cliente(self,cod):
        rows = self.modelo.select_cliente(cod)
        return rows
    
    def alugar(self,cod_cliente,cod_dvd):
        today = date.today()
        if date(today.year, today.day, today.month).weekday() == 6 : # Sunday
            dias = 7  # Uma semana para devolução com preço cheio
        elif date(today.year, today.day, today.month).weekday() == 1: # Tuesday
            dias = 5 # Devolução no proximo domingo
        
        if cod_cliente =='':
            self.notify_text = 'ERRO : campo CÓDIGO CLIENTE precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        else:
            try:
                cod_cliente = int(cod_cliente)
            except:
                self.notify_text = 'ERRO : campo CÓDIGO CLIENTE deve conter apenas números!'
                self.status = False
                raise CodigoInvalido , 'Código deve conter apenas números'
                
        if cod_dvd=='':
            self.notify_text = 'ERRO : campo CÓDIGO DVD precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        
        else:
            try:
                cod_dvd = int(cod_dvd)
            except:
                self.notify_text = 'ERRO : campo CÓDIGO DVD deve conter apenas números!'
                self.status = False
                raise CodigoInvalido , 'Código deve conter apenas números'
        
        dvds = self.listar_titulo_filme(cod_dvd)
        if dvds != ():  
            locado = self.modelo.locate_locados(cod_dvd)
            if locado == ():
                self.modelo.insert_locacao(cod_cliente, cod_dvd, dias)
                self.notify_text = 'Locação realizada com sucesso!'
                self.status = True
                return
            else:
                self.notify_text = 'ERRO : DvD cod = %s já está Alugado!'%(cod_dvd)
                self.status = False
        else:
            self.notify_text = 'ERRO : DvD cod = %s não Cadastrado!'%(cod_dvd)
            self.status = False
        
    def devolucao(self,cod_dvd):
        if cod_dvd != '':
            try:
                cod_dvd = int(cod_dvd)
            except:
                self.notify_text = 'ERRO : campo CÓDIGO deve conter apenas números!'
                self.status = False
                raise CodigoInvalido , 'Código deve conter apenas números'
        else:
            self.notify_text = 'ERRO : Campo CÓDIGO precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        
        cods = self.modelo.select_locados()
        for cod in cods:
            if (int(cod_dvd) == cod[1]):
                self.modelo.insert_devolucao(cod[0])
                self.notify_text = 'Devolução do DvD cod = %s realizada com sucesso!'%(cod_dvd)
                self.status = True
                return
        self.notify_text = 'ERRO : DvD cod = %s não está Alugado!'%(cod_dvd)
        self.status = False
        
    def cadastra_genero_dvd(self,descricao):
        self.modelo.insert_generodvd(descricao)
        return True
    
    def listar_genero_dvd(self):
        rows = self.modelo.select_all_generodvd()
        return rows
    
    def popular_combo_genero(self):
        rows=self.modelo.select_all_generodvd()
        return rows
    
    def cadastra_filme(self, genero_ativo, generos, titulo, quantidade):
        if genero_ativo >= 0:  
            genero = generos[genero_ativo][1]
            cod_genero = self.modelo.select_generodvd(genero)
            cod_filme = self.modelo.insert_filme(cod_genero[0][0], titulo, quantidade)

            for quant in range(quantidade):
                self.modelo.insert_dvd(cod_filme[0])
            return True
        else:
            return False
        
    def listar_locados(self):
        rows = self.modelo.select_locados()
        return rows
    
    def listar_titulo_filme(self,codigo):
        rows = self.modelo.select_dvd(codigo)
        return rows
    
    def listar_atrasados(self):
        rows = self.modelo.select_locados_atrasados()
        return rows
