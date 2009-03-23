# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from datetime import date

from kiwi.ui.objectlist import Column
from kiwi.accessor import ksetattr

from querys import Modelo , Caixa
from login import Login
from notify import Notify


#Exceções
class ControleError(Exception): pass
class EmBranco(ControleError): pass
class CodigoInvalido(ControleError): pass
class PedidoError(ControleError): pass

#Classe usada para armazenar o resultado de uma consulta ou tabela
class Record: pass
class Recordset:
    def __init__(self, rows, columns):
        """ Cria um novo Recordset
        rows é o resultado da query (lista de tuplas)
        columns é uma lista de Column identificando cada coluna do resultado.
        """
        self.columns = columns
        self.items = []
        # Cria os objetos Record e altera cada atributo
        for row in rows:
            rec = Record()
            for i in range(len(self.columns)):
                ksetattr(rec, columns[i].attribute, row[i])
            self.items.append(rec)

    def row_count(self):
        return len(self.items)

    def col_count(self):
        return len(self.columns)

class TabelaControle:
    """ Essa classe controla uma funcionalidade do sistema, por exemplo:
        - Cadastro de categorias, gêneros, produtos, etc. 
        Pode envolver mais de uma tabela. """
    def __init__(self, modelo, tabela):
        self.modelo = modelo
        self.tabela = tabela
    
    def set_notify(self, notify):
        self.notify = notify
    
    def validate(self, field):
        """ Validação dos campos dessa tabela."""
        if field.requerido :
            if field.entry.get_text() == '':
                self.notify.show_notify('erro','Campo %s não deve ficar em branco' % field.field_name)
                return False
        return True
    
    def obrigatorio(self, valor, mensagem = ''):
        """ Verifica se um campo está preenchido e, se não, exibe o notify com a mensagem de erro (caso especificada). """
        if not valor:
            if self.notify and mensagem:
                self.notify.show_notify('erro', mensagem)
            return False
        else:
            return True

    #As funções a seguir demonstram um comportamento padrão. Podem ser substituídas.
    def insert(self, fields):
        record = {}
        for field in fields:
            validate = self.validate(field)
            if validate == True:
                if not field.identificador:
                    if field.tabelacombo:
                        record[field.field_name] = field.entry.get_selected_data()
                    elif field.entry:
                        record[field.field_name] = field.entry.get_text()
            else:
                return False
        record['last_id'] = self.tabela.insert_item(record)
        return record
    
    def update(self, fields, item):
        record = {}
        for field in fields:
            validate = self.validate(field)
            if validate == True:
                if field.identificador:
                    cod = (str(getattr(item, field.field_name)))
                else:
                    if field.entry:
                        record[field.field_name] = field.entry.get_text()
                        #setattr(item, field.field_name, record[field.field_name])
            else:
                return False
        self.tabela.update_item(cod, record)
        return record
        
    def delete(self, cod):
        if self.tabela:
            return self.tabela.delete_item(cod)
        
    def listar(self):
        return self.tabela.select_all_records()

class Controle:
    def __init__(self):
        self.status = False
        self.main_status = False
        self.notify_text = ''
        self.cliente_encontrado = False
        self.dadoscliente = [0][0]
        self.itens = []
        self.recebido = False
        
    def set_modelo(self, modelo):
        self.modelo = modelo
    
    def get_modelo(self):
        return self.modelo
    
    def set_interface(self, interface):
        self.interface = interface
    
    def start(self):
        self.notify = Notification()
        
        #instancias das classes que fazem referencias a tabelas no modelo
        self.categorias_dvd = Categorias_dvd(self.modelo, self.modelo.categorias_dvd)
        self.generos = Generos(self.modelo, self.modelo.generos)
        self.clientes = Clientes(self.modelo, self.modelo.clientes)
        self.filmes = Filmes(self.modelo, self.modelo.filmes)
        
        self.interface.show()

    def logoff(self):        
        self.interface.w_login.show()

    def toInt(self, cod):
        try:
            cod = int(cod)
        except:
            self.notify_text = 'ERRO : campo CÓDIGO deve conter apenas números!'
            self.status = False
            raise CodigoInvalido , 'Código deve conter apenas números'
        return cod

#notificacao
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
            
#clientes
    def cliente_localizado(self):
        if self.cliente_encontrado == True:
            self.cliente_encontrado = False
            return True , self.dadoscliente
        else:
            return False, self.dadoscliente
        
    def cadastra_cliente(self, cod_cliente, name, telefone, celular, endereco, bairro, cidade, estado, cep, editando):
        if name == '':
            self.notify_text = 'ERRO: Campo NOME precisa ser preenchido!'
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
            self.notify_text = 'ERRO: Cliente não Cadastrado!'
            self.status = False
            raise CodigoInvalido,  'Código não cadastrado'
        self.status = True
        return rows
    
#locacao
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
            self.notify_text = 'ERRO: campo CÓDIGO CLIENTE precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        else:
            cod_cliente = self.toInt(cod_cliente)
            
        if cod_dvd == '':
            self.notify_text = 'ERRO: campo CÓDIGO DVD precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        
        else:
            cod_dvd =self.toInt(cod_dvd)
        
        dvds = self.listar_titulo_filme(cod_dvd)
        if dvds != ():  
            locado = self.modelo.locados.locate_locados(cod_dvd)
            if locado == ():
                self.modelo.locados.insert_locacao(cod_caixa, cod_cliente, cod_dvd, dias)
                self.notify_text = 'LocaÃ§ão realizada com sucesso!'
                self.status = False
                self.main_status = True
                return
            else:
                self.notify_text = 'ERRO: DvD cod = %s já está Alugado!'%(cod_dvd)
                self.status = True
        else:
            self.notify_text = 'ERRO: DvD cod = %s não Cadastrado!'%(cod_dvd)
            self.status = True
        
    def devolucao(self,cod_dvd):
        if cod_dvd != '':
            cod_dvd = self.toInt(cod_dvd)
        else:
            self.notify_text = 'ERRO: Campo CÓDIGO precisa ser preenchido!'
            self.status = False
            raise  EmBranco , 'Código deve ser preenchido'
        
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
    
    def get_categoria_cod(self):
        return self.cod_categoria
        
    def cadastra_categoria_dvd(self, descricao, preco):
        self.cod_categoria = self.modelo.categorias_dvd.insert_item(descricao, preco)
        return True
    
    def listar_categoria_dvd(self):
        rows = self.modelo.categorias_dvd.select_all()
        return rows
    
    def listar_genero_dvd(self):
        rows = self.modelo.generos.select_all()
        return rows
    
    def cadastra_filme(self, genero_ativo, generos, categoria_ativa, categorias, titulo, quantidade):
        if genero_ativo >= 0 and categoria_ativa >=0:  
            genero = generos[genero_ativo][1]
            categoria = categorias[categoria_ativa][1]
            cod_genero = self.modelo.generos.select_genero_desc(genero)
            cod_categoria = self.modelo.categorias_dvd.select_categoria_desc(categoria)
            cod_filme = self.modelo.filmes.insert_item(cod_genero[0][0], cod_categoria[0][0], titulo, quantidade)
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
        for cods in lista:
            if cod == cods.cod :
                self.status = False
                self.notify_text = 'DvD já está inserido na lista de locação'
                raise CodigoInvalido,  'Código em uso'
        dvd = self.modelo.dvds.select_dvd(cod)
        dvds = []
        if dvd != ():  
            locado = self.modelo.locados.locate_locados(cod)
            if locado == ():
                self.status = True
                preco = self.modelo.categorias_dvd.get_preco(dvd[0][2])
                preco = preco[0][0]
                listar = ([dvd[0][0] ,  dvd[0][1] , preco])
                dvds.append(listar)
            else:
                self.notify_text = 'ERRO: DvD cod = %s já está Alugado!'%(cod)
                self.status = False
                raise CodigoInvalido,  'Código em uso'
        else:
            self.notify_text = 'ERRO: DvD cod = %s não Cadastrado!'%(cod)
            self.status = False
            raise CodigoInvalido,  'Código não cadastrado'
        return dvds

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
                item['item'] = self.modelo.item_pedidos.add_item(cod_pedido, item['cod_produto'], item['localiz'], item['cod_conta'], item['quantidade'], item['preco_unit'], item['desconto'])
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

    def rs_estoque(self):
        rows = self.modelo.estoque.listar_estoque()
        cols = []
        cols.append(Column('cod_produto', title="Código", justify=gtk.JUSTIFY_RIGHT))
        cols.append(Column('nome', title="Descrição", sorted=True))
        cols.append(Column('localiz', title="Local"))
        cols.append(Column('quantidade', title="Quantidade"))
        return Recordset(rows, cols)

    def cliente_devolucao(self):
        return self.cod_cliente_devolucao
        
    def dvd_listado_check(self):
        return self.listado
        
    def get_total_locacao(self):
        return self.total
        
    def listar_dvds_locados(self, cod_dvd, lista):
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
                    preco = self.modelo.categorias_dvd.get_preco(dvd[0][2])
                    preco = preco[0][0]
                    listar = ([dvd[0][0] ,  dvd[0][1] , preco])
                    dvds.append(listar)
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

#---caixa
    def open_caixa(self, inicial):
           #FixMe: get conta default
           caixa = 0
           self.modelo.caixa.insert_item(caixa, inicial)
           
    def close_caixa(self):
           self.modelo.caixa.update_item(self.status[0][0], date.today)

    def get_caixa_status(self):
        self.status = self.modelo.caixa.locate_item()
        if self.status == ():
            return 'Closed'
        else:
            today = date.today()
            if today == self.status[0][2]:
                return 'Opened'
            else:
                return 'NotClosed'

#recebimento
    def receber_locacao(self, lista):
        self.itens = []
        for iten in lista:
            self.itens.append([iten.title , iten.valor])
        return self.itens
        
    def receber_devolucao(self, lista):
        self.itens = []
        for iten in lista:
            if iten.check ==True:
                self.itens.append([iten.title , iten.valor])
        return self.itens
        
    def set_receber_status(self, recebido):
        self.recebido = recebido
        
    def get_receber_status(self):
        return self.recebido

class Categorias_dvd(TabelaControle):
    def combo(self):
        lista = []
        rows = self.tabela.select_all_records()
        for row in rows:
            lista.append((row['descricao'], row['cod_categoria']))
        return lista
        
    def item_descricao(self, cod):
        return self.tabela.select_categoria_dvd(cod)
        
class Generos(TabelaControle):
    def combo(self):
        lista = []
        rows = self.tabela.select_all_records()
        for row in rows:
            lista.append((row['descricao'], row['cod_genero']))
        return lista
        
    def item_descricao(self, cod):
        return self.tabela.select_genero(cod)
        
class Clientes(TabelaControle):
    pass

class Filmes(TabelaControle):
    pass
    
class Notification:
    def __init__(self):
        self.notification = Notify()
        self.msg = self.notification.add_msg()
        self.close = self.notification.add_button()
        self.close.connect("clicked",self.close_notify)
        
    def get_widget(self):
        return self.notification
        
    def hide(self):
        self.notification.hide_all()
        
    def close_notify(self, w):
        self.notification.hide_all()
    
    def add_icon(self, icon):
        self.notification.add_icon(icon)
        
    def show_notify(self, icon, text):
        if text:
            self.add_icon(icon)
            self.msg.set_text(text)
            self.notification.show_all()
