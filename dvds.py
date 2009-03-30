# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from iconmenu import iconMenuItem 
from listdialog import FieldType, ListDialog, ListToolButton #FixMe: to controle


class Categorias:
    def close(self,w):
        self.w_categorias_dvd.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_categorias_dvd = gtk.Dialog()
        self.w_categorias_dvd.set_position(gtk.WIN_POS_CENTER)
        self.w_categorias_dvd.connect("destroy", self.close)
        self.w_categorias_dvd.set_title("CEF SHOP - Cadastrar Categorias de Dvds ")
        self.w_categorias_dvd.set_size_request(600,450)
        self.w_categorias_dvd.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_categoria', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('descricao', 'Descrição', str, 0, searchable = True,requerido = True))
        fields.append(FieldType('preco', 'Preço',currency, 0,  requerido = True))
        
        listobject =  ListDialog(self.controle, 'categorias_dvd', 'Categorias' )
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_categorias_dvd.action_area.pack_start(button_close, False, True, 0)        
        self.w_categorias_dvd.vbox.pack_start(widget,True, True, 2)
        
        self.w_categorias_dvd.show_all()
        self.w_categorias_dvd.show()
#-----------------------------------------------------    
class Generos:
    def close(self,w):
        self.w_generos.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_generos = gtk.Dialog()
        self.w_generos.set_position(gtk.WIN_POS_CENTER)
        self.w_generos.connect("destroy", self.close)
        self.w_generos.set_title("CEF SHOP - Cadastrar Generos de Dvds ")
        self.w_generos.set_size_request(600,450)
        self.w_generos.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_genero', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('descricao', 'Descrição', str, 0, None, searchable = True))
        
        listobject =  ListDialog(self.controle, 'generos', 'Generos' )
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_generos.action_area.pack_start(button_close, False, True, 0)        
        self.w_generos.vbox.pack_start(widget,True, True, 2)
        
        self.w_generos.show_all()
        self.w_generos.show()
#-----------------------------------------------------    
class Filmes:
    def close(self,w):
        self.w_filmes.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_filmes = gtk.Dialog()
        self.w_filmes.set_position(gtk.WIN_POS_CENTER)
        self.w_filmes.connect("destroy", self.close)
        self.w_filmes.set_title("CEF SHOP - Cadastro de Filmes ")
        self.w_filmes.set_size_request(700,600)
        self.w_filmes.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_filme', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('titulo', 'Titulo', str, 0, None, searchable = True,requerido = True))
        fields.append(FieldType('cod_genero', 'Genero',requerido = True, tabelacombo='generos'))
        fields.append(FieldType('cod_categoria', 'Categoria',requerido = True, tabelacombo='categorias_dvd'))
        fields.append(FieldType('quantidade', 'Quantidade',int, 0, None,requerido = True))
        
        listobject =  ListDialog(self.controle, 'filmes', 'Filmes' )
        
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_filmes.action_area.pack_start(button_close, False, True, 0)        
        self.w_filmes.vbox.pack_start(widget,True, True, 2)
        
        self.w_filmes.show_all()
        self.w_filmes.show()
#-----------------------------------------------------    
class Dvds:
    def close(self,w):
        self.w_dvd.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_dvd = gtk.Dialog()
        self.w_dvd.set_position(gtk.WIN_POS_CENTER)
        self.w_dvd.connect("destroy", self.close)
        self.w_dvd.set_title("CEF SHOP - Gerenciar Dvds ")
        self.w_dvd.set_size_request(600,450)
        self.w_dvd.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_dvd', 'Código do DvD', int, 0, None, True, False, identificador = True))
        fields.append(FieldType('cod_filme', 'Codigo do Filme', int, 0, None,False, False, searchable = True))#Titulo do filme
        fields.append(FieldType('titulo', 'Titulo', str, 0, None,True, False, searchable = True))#Titulo do filme
        listobject =  ListDialog(self.controle, 'dvds', 'Dvds' )
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_dvd.action_area.pack_start(button_close, False, True, 0)        
        self.w_dvd.vbox.pack_start(widget,True, True, 2)
        
        self.w_dvd.show_all()
        self.w_dvd.show()
#-----------------------------------------------------    
