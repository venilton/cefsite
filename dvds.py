# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel
from kiwi.ui.entry import KiwiEntry

from notify import notify_area
from iconmenu import iconMenuItem

class Categoria_dvd:
    def __init__(self, cod, title, valor):
        self.cod = cod
        self.title = title
        self.valor = valor
    def __repr__(self):
        return '<Categoria_dvd %s>' % self.title
        
class Categorias:
    def create_list(self):
        columns = [
        Column('cod', data_type =int, sorted=True),
        Column('title', data_type = str,  title = 'Descrição'),
        Column('valor', data_type = currency,  title = 'Valor')
        ]
        data =[]
        categorias = self.controle.listar_categoria_dvd()
        for categoria in categorias:
            codigo = categoria[0]
            descricao = categoria[1]
            valor = categoria[2]
            data.append(Categoria_dvd(codigo, descricao, valor))

        lista = ObjectList(columns)
        lista.extend(data)
            
        return lista

    def destroy(self, widget, data=None):
        gtk.main_quit()
    
    def close(self,w):
        self.w_categorias_dvd.destroy()

    def cadastra (self, widget):
        descricao = self.entry_descricao.get_text()       
        preco = self.entry_preco.get_text()
        status = self.controle.cadastra_categoria_dvd(descricao, preco)
        if status == True:
            self.w_categorias_dvd.destroy()
       
    def __init__(self, controle):
        self.w_categorias_dvd = gtk.Dialog()
        self.w_categorias_dvd.set_position(gtk.WIN_POS_CENTER)
        self.w_categorias_dvd.connect("destroy", self.close)
        self.w_categorias_dvd.set_title("CEF SHOP - Cadastrar Categorias de Dvds ")
        self.w_categorias_dvd.set_size_request(450,250)
        self.w_categorias_dvd.set_border_width(8)
        self.controle = controle

#-------Elementos       
        label_descricao = gtk.Label("Descrição :")
        self.entry_descricao = gtk.Entry(0)
        
        label_preco = gtk.Label("Preço :")
        self.entry_preco = gtk.Entry()
        #self.entry_preco.set_mask('0000,00')
#------Lista
        frame_generos = gtk.Frame("Categorias")
        self.w_categorias_dvd.vbox.add(frame_generos)

        listview = self.create_list()
        frame_generos.add(listview)

#------Frame cadastra
        frame_dados = gtk.Frame("Cadastrar Nova Categoria")
        self.w_categorias_dvd.vbox.add(frame_dados)
      
        hbox_labelentry = gtk.HBox(False, 4)
        hbox_labelentry.set_border_width(4)
        frame_dados.add(hbox_labelentry)
        
        vbox_label = gtk.VBox(False, 4)
        hbox_labelentry.pack_start(vbox_label, False, True, 2)
       
        vbox_entry = gtk.VBox(False, 4)
        hbox_labelentry.pack_start(vbox_entry, True, True, 2)

        vbox_label.pack_start(label_descricao, False, True, 8)
        vbox_label.pack_start(label_preco, False, True, 8)

        vbox_entry.pack_start(self.entry_descricao, False, True, 2)
        vbox_entry.pack_start(self.entry_preco, False, True, 2)

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_categorias_dvd.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()

        self.w_categorias_dvd.show_all()
        self.w_categorias_dvd.show()
#-----------------------------------------------------
class Generos:

    def create_list(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        lista = gtk.ListStore(int,str)
        tree_view = gtk.TreeView(lista)
        scrolled_window.add_with_viewport (tree_view)

        self.generos = self.controle.listar_genero_dvd()
        for genero in self.generos:
            lista.append([genero[0], genero[1]])

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Cod", cell, text=0)
        
        cell2 = gtk.CellRendererText()
        column2 = gtk.TreeViewColumn("Descrição", cell2, text=1)
        
        tree_view.append_column(column)
        tree_view.append_column(column2)

        return scrolled_window

    def destroy(self, widget, data=None):
        gtk.main_quit()
    
    def close(self,w):
        self.w_generos.destroy()

    def cadastra (self, widget, entry_descricao):
        descricao = entry_descricao.get_text()       
        status = self.controle.cadastra_genero_dvd(descricao)
        if status == True:
            self.w_generos.destroy()
       
    def __init__(self, controle):
        self.w_generos = gtk.Dialog()
        self.w_generos.set_position(gtk.WIN_POS_CENTER)
        self.w_generos.connect("destroy", self.close)
        self.w_generos.set_title("CEF SHOP - Cadastrar Generos")
        self.w_generos.set_size_request(450,250)
        self.w_generos.set_border_width(8)
        self.controle = controle

#-------Elementos       
        label_descricao = gtk.Label("Descrição :")
        entry_descricao = gtk.Entry(0)
  
#------Lista
        vpaned = gtk.VPaned()
        self.w_generos.vbox.add(vpaned)

        frame_generos = gtk.Frame("Generos")
        vpaned.add(frame_generos)

        liststore = self.create_list()
        frame_generos.add(liststore)

#------Frame cadastra
        frame_dados = gtk.Frame("Cadastrar Novo Genero")
        self.w_generos.vbox.add(frame_dados)
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)
        
        vbox_label = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_label, False, True, 2)
       
        vbox_entry = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_entry, True, True, 2)

        vbox_label.pack_start(label_descricao, False, True, 8)
        vbox_entry.pack_start(entry_descricao, False, True, 2)

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra, entry_descricao)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_generos.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()

        self.w_generos.show_all()
        self.w_generos.show()
#-----------------------------------------------------
class Filmes:
    
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
