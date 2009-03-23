# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel, ColoredColumn
from kiwi.ui.entry import KiwiEntry

from notify import Notify
from iconmenu import iconMenuItem
from listdialog import FieldType, ListDialog


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
        fields.append(FieldType('descricao', 'Descrição', str, 0, None, searchable = True,requerido = True))
        fields.append(FieldType('preco', 'Preço',currency, 0, None,requerido = True))
        
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
        fields.append(FieldType('cod_categoria', 'Categoria', None,requerido = True, tabelacombo='categorias_dvd'))
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

class Filmes_old:
    
    def close(self,w):
        self.w_filmes.destroy()

    def cadastra (self, widget):
        genero = self.combo_genero.get_active()
        categoria = self.combo_categoria.get_active()
        titulo = self.entry_titulo.get_text()
        quantidade =int(self.entry_quantidade.get_text())
        self.controle.cadastra_filme(genero, self.generos, categoria, self.categorias, titulo, quantidade)
        
    def __init__(self,controle):
        self.w_filmes = gtk.Dialog()
        self.w_filmes.set_position(gtk.WIN_POS_CENTER)
        self.w_filmes.connect("destroy", self.close)
        self.w_filmes.set_title("CEF SHOP - Cadastrar Filmes")
        self.w_filmes.set_size_request(450,250)
        self.w_filmes.set_border_width(8)
        self.controle = controle

#-------Elementos       
        label_titulo = gtk.Label("Titulo :")
        self.entry_titulo = gtk.Entry(0)

        label_genero = gtk.Label("Genero :")
        self.combo_genero = gtk.combo_box_new_text()
        
        self.generos = self.controle.listar_genero_dvd()
        for genero in self.generos:
            self.combo_genero.append_text(genero[1])

        label_categoria = gtk.Label("Categoria :")
        self.combo_categoria = gtk.combo_box_new_text()
        
        self.categorias = self.controle.listar_categoria_dvd()
        for categoria in self.categorias:
            self.combo_categoria.append_text(categoria[1])
        
        label_quantidade = gtk.Label("Quantidade :")
        self.entry_quantidade = gtk.Entry(0)
     
#------Frame cadastra
        frame_dados = gtk.Frame("Dados do Filme")
        self.w_filmes.vbox.add(frame_dados)
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)
        
        vbox_label = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_label, False, True, 2)
       
        vbox_entry = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_entry, True, True, 2)

        vbox_label.pack_start(label_titulo, False, True, 8)
        vbox_entry.pack_start(self.entry_titulo, False, True, 2)

        vbox_label.pack_start(label_genero, False, True, 8)
        vbox_entry.pack_start(self.combo_genero, False, True, 2)

        vbox_label.pack_start(label_categoria, False, True, 8)
        vbox_entry.pack_start(self.combo_categoria, False, True, 2)
        
        vbox_label.pack_start(label_quantidade, False, True, 8)
        vbox_entry.pack_start(self.entry_quantidade, False, True, 2)

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_filmes.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()

        self.w_filmes.show_all()
        self.w_filmes.show()
#-----------------------------------------------------
