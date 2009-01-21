# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from notify import notify_area
from iconmenu import iconMenuItem
    
class Admin:
    def createMenus(self, vbox):
        self.menubar = gtk.MenuBar()
        vbox.pack_start(self.menubar, expand=False)

        topmenuitem = gtk.MenuItem('_Menu')
        self.menubar.add(topmenuitem)
    
        menu = gtk.Menu()
        topmenuitem.set_submenu(menu)
 
        menuitem = iconMenuItem(('_Logoff'), gtk.STOCK_QUIT)
        menu.add(menuitem)
        menuitem.connect('activate', self.logoff)

        menuitem = iconMenuItem(('_Fechar'),gtk.STOCK_CLOSE)
        menuitem.connect('activate', gtk.main_quit)
        menu.add(menuitem)
    
    def notification (self, widget, focus):
        status = self.controle.notify()
        if status[0] == True:
            self.notify.set_text(self.notify_text)
            self.hboxnotify.show()
        else:
            self.hboxnotify.hide()
            
    def open_generos(self, widget):
        Generos(self.controle)
        
    def close_notification(self, widget):
        self.show_notify == False
        self.hboxnotify.hide()
        
    def open_filmes(self, widget):
        Filmes(self.controle)

    def open_locados(self, widget):
        Locados(self.controle)

    def open_atrasados(self, widget):
        Atrasados(self.controle)
        
    def logoff(self,widget):
        self.w_admin.destroy()
        self.controle.logoff()
    
    def __init__(self,controle):
        self.w_admin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_admin.set_position(gtk.WIN_POS_CENTER)
        self.w_admin.connect("delete_event", lambda w,e: gtk.main_quit())
        self.w_admin.set_title("CEF SHOP - Administração")
        self.w_admin.set_size_request(580,280)
        self.controle = controle

#---Botoes
        button_generos = gtk.Button("Generos")
        button_generos.connect("clicked", self.open_generos)

        button_filmes = gtk.Button("Filmes")
        button_filmes.connect("clicked",self.open_filmes)
       
        button_locados = gtk.Button("Locados")
        button_locados.connect("clicked",self.open_locados)
       
        button_atrasados = gtk.Button("Atrasados")
        button_atrasados.connect("clicked",self.open_atrasados)

#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_admin.add(vbox_main)     

#------Menu
        self.createMenus(vbox_main)

#------Divisao h principal
        hbox_main = gtk.HBox(False, 2)     
        vbox_main.pack_start(hbox_main, True, True, 2)

#------Divisoes v dos elementos 
        vbox1 = gtk.VBox(True, 1)
        hbox_main.pack_start(vbox1, True, True, 2)
 
        vbox2 = gtk.VBox(True, 1)
        hbox_main.pack_start(vbox2, True, True, 2)
     
#------Frame cadastro
        frame_cad = gtk.Frame("Cadastro")
        vbox1.pack_start(frame_cad, True, True, 2)

        vbox_cad=gtk.VButtonBox()
        vbox_cad.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_cad.set_spacing(10)
        frame_cad.add(vbox_cad)
        
        vbox_cad.add(button_generos)
        vbox_cad.add(button_filmes)

#------Frame Controle
        frame_controle = gtk.Frame("Controle")
        vbox2.pack_start(frame_controle, True, True, 2)
 
        vbox_controle=gtk.VButtonBox()
        vbox_controle.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_controle.set_spacing(10)
        frame_controle.add(vbox_controle)
        
        vbox_controle.add(button_locados)
        vbox_controle.add(button_atrasados)

#-------Mostra tudo
        self.w_admin.show_all()
        self.w_admin.show()
#-----------------------------------------------------
class Generos:

    def create_list(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        lista = gtk.ListStore(int,str)
        tree_view = gtk.TreeView(lista)
        scrolled_window.add_with_viewport (tree_view)

        generos = self.controle.listar_genero_dvd()
        for genero in generos:
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

    def cadastra (self, widget, combo_genero, generos, entry_titulo, entry_quantidade):
        active = combo_genero.get_active()
        titulo = entry_titulo.get_text()
        quantidade =int(entry_quantidade.get_text())
        self.controle.cadastra_filme(active, generos, titulo, quantidade)
        
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
        entry_titulo = gtk.Entry(0)

        label_genero = gtk.Label("Genero :")
        combo_genero = gtk.combo_box_new_text()
        
        generos = self.controle.popular_combo_genero()
        for genero in generos:
            combo_genero.append_text(genero[1])

        label_quantidade = gtk.Label("Quantidade :")
        entry_quantidade = gtk.Entry(0)
     
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
        vbox_entry.pack_start(entry_titulo, False, True, 2)

        vbox_label.pack_start(label_genero, False, True, 8)
        vbox_entry.pack_start(combo_genero, False, True, 2)

        vbox_label.pack_start(label_quantidade, False, True, 8)
        vbox_entry.pack_start(entry_quantidade, False, True, 2)

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra, combo_genero, generos, entry_titulo, entry_quantidade)

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
class Locados:
    
    def close(self,w):
        self.w_locados.destroy()

    def create_list(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        lista = gtk.ListStore(str, str, str, str)
        tree_view = gtk.TreeView(lista)
        scrolled_window.add_with_viewport (tree_view)
    
        locados = self.controle.listar_locados()

        for locado in locados:
            codvd = str(locado[1])
            titulo = self.controle.listar_titulo_filme(codvd)
            dvd = str(codvd) +' - '+ titulo[0][1]
            codcliente = str(locado[2])
            nome = self.controle.listar_cliente(codcliente)
            cliente = str(codcliente) + '-' + nome[0][1]
            retirada = locado[3]
            devolucao = locado[4]
            lista.append([dvd, cliente, retirada , devolucao])
           
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn("Codigo - Dvd", cell1, text=0)
        
        cell2 = gtk.CellRendererText()
        column2 = gtk.TreeViewColumn("Codigo - Cliente", cell2, text=1)
        
        cell3 = gtk.CellRendererText()
        column3 = gtk.TreeViewColumn("Retirada", cell3, text=2)
        
        cell4 = gtk.CellRendererText()
        column4 = gtk.TreeViewColumn("Devolver em", cell4, text=3)
        tree_view.append_column(column1)
        tree_view.append_column(column2)
        tree_view.append_column(column3)
        tree_view.append_column(column4)

        return scrolled_window
   
    def __init__(self,controle):
        self.w_locados = gtk.Dialog()
        self.w_locados.set_position(gtk.WIN_POS_CENTER)
        self.w_locados.connect("destroy", self.close)
        self.w_locados.set_title("CEF SHOP - Locados")
        self.w_locados.set_size_request(650,350)
        self.w_locados.set_border_width(8)
        self.controle = controle
  
#------Lista
        vpaned = gtk.VPaned()
        self.w_locados.vbox.add(vpaned)

        frame_locados = gtk.Frame("Dvds atualmente Alugados ")
        vpaned.add(frame_locados)

        liststore = self.create_list()
        frame_locados.add(liststore)

#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)
        
        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_locados.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_close)
        button_close.set_flags(gtk.CAN_DEFAULT)

        self.w_locados.show_all()
        self.w_locados.show()
#-----------------------------------------------------
class Atrasados:
    
    def close(self,w):
        self.w_atrasados.destroy()

    def create_list(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        lista = gtk.ListStore(str, str, str, str)
        tree_view = gtk.TreeView(lista)
        scrolled_window.add_with_viewport (tree_view)

        atrasados = self.controle.listar_atrasados()
        
        for locado in atrasados:
            codvd = str(locado[1])
            titulo = self.controle.listar_titulo_filme(codvd)
            dvd = str(codvd) +' - '+ titulo[0][1]
            codcliente = str(locado[2])
            nome = self.controle.listar_cliente(codcliente)
            cliente = str(codcliente) + '-' + nome[0][1]
            retirada = locado[3]
            devolucao = locado[4]
            lista.append([dvd, cliente, retirada , devolucao])
            
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn("Cod Dvd", cell1, text=0)
        
        cell2 = gtk.CellRendererText()
        column2 = gtk.TreeViewColumn("Cod Cliente", cell2, text=1)
        
        cell3 = gtk.CellRendererText()
        column3 = gtk.TreeViewColumn("Retirada", cell3, text=2)
        
        cell4 = gtk.CellRendererText()
        column4 = gtk.TreeViewColumn("Atrasado desde", cell4, text=3)
        
        tree_view.append_column(column1)
        tree_view.append_column(column2)
        tree_view.append_column(column3)
        tree_view.append_column(column4)

        return scrolled_window
   
    def __init__(self, controle):
        self.w_atrasados = gtk.Dialog()
        self.w_atrasados.set_position(gtk.WIN_POS_CENTER)
        self.w_atrasados.connect("destroy", self.close)
        self.w_atrasados.set_title("CEF SHOP - Locados")
        self.w_atrasados.set_size_request(450,250)
        self.w_atrasados.set_border_width(8)
        self.controle = controle

#------Lista
        vpaned = gtk.VPaned()
        self.w_atrasados.vbox.add(vpaned)

        frame_locados = gtk.Frame("Dvds atualmente Alugados ")
        vpaned.add(frame_locados)

        liststore = self.create_list()
        frame_locados.add(liststore)

#-------Botoes     

        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)
        
        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_atrasados.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_close)
        button_close.set_flags(gtk.CAN_DEFAULT)

        self.w_atrasados.show_all()
        self.w_atrasados.show()
#-----------------------------------------------------
