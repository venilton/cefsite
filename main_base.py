# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

class Login:
   
    def createMenus(self, vbox):
        self.menubar = gtk.MenuBar()
        vbox.pack_start(self.menubar, expand=False)

        topmenuitem = gtk.MenuItem('_Menu')
        self.menubar.add(topmenuitem)
    
        menu = gtk.Menu()
        topmenuitem.set_submenu(menu)
 
        menuitem = iconMenuItem(('_Fechar'),gtk.STOCK_CLOSE)
        menuitem.connect('activate', gtk.main_quit)
        menu.add(menuitem)
    
    def set_controle(self, controle):
        self.controle = controle

    def destroy(self, widget, data=None):
        gtk.main_quit()
    
    def open_loja (self, widget):
        Loja(self.controle)
        self.w_login.hide()

    def open_admin (self, widget):
        Admin(self.controle)
        self.w_login.hide()

    def __init__(self):
        self.w_login = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_login.set_position(gtk.WIN_POS_CENTER)
        #self.w_login.set_resizable(False)
        self.w_login.connect("delete_event", lambda w,e: gtk.main_quit())
        self.w_login.set_title("CEF SHOP - Login")
        self.w_login.set_size_request(250,150)
        
#-------Botoes       
        button_loja = gtk.Button("Loja")
        button_loja.connect("clicked", self.open_loja)
        
        button_admin = gtk.Button("Administração")
        button_admin.connect("clicked", self.open_admin)
        
#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_login.add(vbox_main)
        vbox_main.show()     
#------Menu
        self.createMenus(vbox_main)
#------Divisao h principal
        hbox_main = gtk.HBox(False, 4)
        vbox_main.pack_start(hbox_main, True, True, 4)    

#------Frame escolha
        frame_escolha = gtk.Frame("Escolha")
        hbox_main.pack_start(frame_escolha, True, True, 4)

        vbox_escolha=gtk.VButtonBox()
        vbox_escolha.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_escolha.set_spacing(10)
        frame_escolha.add(vbox_escolha)
        
        vbox_escolha.add(button_admin)
        vbox_escolha.add(button_loja)

        self.w_login.show_all()
        self.w_login.show()
        
    def show(self):
        gtk.main()
#-----------------------------------------------------

class Loja:   
    show_notify = False
    def createMenus(self, vbox, window):
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
        #status = self.controle.notify()
        #show = status
        if self.show_notify == True:
            self.notify.set_text(self.notify_text)
            self.hboxnotify.show()
        else:
            self.hboxnotify.hide()
    
    def close_notification(self, widget):
        self.show_notify == False
        self.hboxnotify.hide()

    def open_cad_clientes (self, widget):
        Cadastro_clientes(self.controle)
        self.close_notification(widget)
    
    def open_locar(self, widget):
        Locar(self.controle)
        self.close_notification(widget)
        
    def open_devolver(self, widget):
        Devolver(self.controle)
        self.close_notification(widget)
        
    def logoff(self,widget):
        self.w_loja.destroy()
        self.controle.logoff()
        
    def __init__(self,controle):
        self.w_loja = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_loja.set_position(gtk.WIN_POS_CENTER)
        self.w_loja.connect("delete_event", lambda w,e: gtk.main_quit())
        self.w_loja.connect("focus_in_event", self.notification)
        self.w_loja.set_title("CEF SHOP - Loja")
        self.w_loja.set_size_request(580,280)
        self.controle = controle

#---Botoes
        button_clientes = gtk.Button("Clientes")
        button_clientes.connect("clicked", self.open_cad_clientes)
    
        button_retirada = gtk.Button("Retirada")
        button_retirada.connect("clicked",self.open_locar)
      
        button_devolucao = gtk.Button("Devolucao")
        button_devolucao.connect("clicked",self.open_devolver)
   
        button_venda = gtk.Button("Venda")
        #button_venda.connect("clicked", , None)

#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_loja.add(vbox_main)
#------Menu        
        self.createMenus(vbox_main, self.w_loja)
#------Divisao h principal
        hbox_main = gtk.HBox(False, 2)
        vbox_main.pack_start(hbox_main, True, True, 4)
#------Divisoes v dos elementos 
        vbox1 = gtk.VBox(True, 2)
        hbox_main.pack_start(vbox1, True, True, 2)
 
        vbox2 = gtk.VBox(True, 2)
        hbox_main.pack_start(vbox2, True, True, 2)
     
#------Frame cadastro

        frame_cad = gtk.Frame("Cadastro")
   
        vbox1.pack_start(frame_cad, True, True, 2)
        
        vbox_cad=gtk.VButtonBox()
        vbox_cad.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_cad.set_spacing(10)
        frame_cad.add(vbox_cad)
  
        vbox_cad.add(button_clientes)

#------Frame loja

        frame_loja = gtk.Frame("Loja")
        vbox1.pack_start(frame_loja, True, True, 2)
  
        vbox_loja=gtk.VButtonBox()
        vbox_loja.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_loja.set_spacing(10)
    
        frame_loja.add(vbox_loja)
        
        vbox_loja.add(button_venda)


#------Frame locacao
       
        frame_loca = gtk.Frame("Locação")

        vbox2.pack_start(frame_loca, True, True, 2)

        vbox_loca=gtk.VButtonBox()
        vbox_loca.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_loca.set_spacing(10)

        frame_loca.add(vbox_loca)
        
        vbox_loca.add(button_retirada)
        vbox_loca.add(button_devolucao)

#-------area de notificacao
        amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
        self.hboxnotify = gtk.HBox(False)
        vbox_main.pack_start(self.hboxnotify, False, True, 2)
        event_box = gtk.EventBox()

        self.hboxnotify.pack_start(event_box, True, True, 2)        
        
        close_button = gtk.Button()
        close_button.connect("clicked", self.close_notification)
        close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.add(close)
        #close_button.set_relief(gtk.RELIEF_NONE)
        close_button.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

        self.hboxnotify.pack_start(close_button, False, True, 2)
        
        self.notify = gtk.Label()
        event_box.add(self.notify)

        event_box.realize()
        #event_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

#-------Mostra tudo

        self.w_loja.show_all()
        self.hboxnotify.hide()
        self.w_loja.show()
        

#-----------------------------------------------------

class Cadastro_clientes:
    def set_controle(self, controle):
        self.controle = controle
        
    def close_notification(self, widget):
        self.hboxnotify.hide()
        
    def close(self,w):
        Loja.show_notify = False
        self.w_cad_clientes.destroy()

    def cadastra (self, widget, entry_nome):
        name = entry_nome.get_text()
        try:
            self.controle.cadastra_cliente(name)
        except:
            pass
        status = self.controle.notify()
        if status[0] == True:
            Loja.show_notify = True
            Loja.notify_text = status[1]
            self.w_cad_clientes.hide()
        else:
            self.notify.set_text(status[1])
            self.hboxnotify.show()
            
    def __init__(self,controle):
        self.w_cad_clientes = gtk.Dialog()
        self.w_cad_clientes.set_position(gtk.WIN_POS_CENTER)
        self.w_cad_clientes.set_size_request(580,280)
        self.w_cad_clientes.set_border_width(4)
        self.w_cad_clientes.set_title("CEF SHOP - Cadastro de Clientes")
        self.w_cad_clientes.connect("destroy", self.close)
        self.controle = controle

#------Frame Dados pessoais

        frame_dados = gtk.Frame("Dados Pessoais")
        self.w_cad_clientes.vbox.pack_start(frame_dados,False, True, 4)       
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)

        f_entry = gtk.Fixed()
        f_label = gtk.Fixed()
        
        label_nome = gtk.Label("Nome :")
        f_label.put(label_nome, 2, 14)
        entry_nome = gtk.Entry(0)
        entry_nome.set_size_request(400,28)
        f_entry.put(entry_nome, 10, 10)
        
        label_cpf = gtk.Label("CPF :")
        f_label.put(label_cpf, 2, 44)
        entry_cpf = gtk.Entry(0)
        entry_cpf.set_size_request(200,28)
        f_entry.put(entry_cpf, 10, 40)
                  
        vbox_labelentry.pack_start(f_label, False, True, 4)
        vbox_labelentry.pack_start(f_entry, False, True, 4)

#-------area de notificacao

        amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
        self.hboxnotify = gtk.HBox(False)
        #vbox_main.pack_start(self.hboxnotify, False, True, 2)
        self.w_cad_clientes.vbox.pack_start(self.hboxnotify,False, True, 4)
        event_box = gtk.EventBox()

        self.hboxnotify.pack_start(event_box, True, True, 2)        
        
        close_button = gtk.Button()
        close_button.connect("clicked", self.close_notification)
        close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.add(close)
        #close_button.set_relief(gtk.RELIEF_NONE)
        close_button.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

        self.hboxnotify.pack_start(close_button, False, True, 2)
        
        self.notify = gtk.Label()
        event_box.add(self.notify)

        event_box.realize()
        #event_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

#-------Botoes

        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra, entry_nome)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_cad_clientes.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()
          
#------Mostra tudo

        self.w_cad_clientes.show_all()
        self.hboxnotify.hide()
        self.w_cad_clientes.show()

#-----------------------------------------------------

class Locar:
    def set_controle(self, controle):
        self.controle = controle
        
    def close_notification(self, widget):
        self.hboxnotify.hide()
        
    def close(self,w):
        self.w_locar.destroy()

    def cadastra (self,widget, entry_cliente, entry_dvd):
        cod_cliente = entry_cliente.get_text()
        cod_dvd = entry_dvd.get_text()       
        dias = '7'
        try:
            self.controle.alugar(cod_cliente, cod_dvd, dias)
        except:
            pass
        status = self.controle.notify()
        if status[0] == True:
            Loja.show_notify = True
            Loja.notify_text = status[1]
            self.w_locar.hide()
        else:
            self.notify.set_text(status[1])
            self.hboxnotify.show()    
        
    def __init__(self,controle):
        self.w_locar = gtk.Dialog()
        self.w_locar.set_position(gtk.WIN_POS_CENTER)
        self.w_locar.connect("destroy", self.close)
        self.w_locar.set_title("CEF SHOP - Locar")
        self.w_locar.set_size_request(450,200)
        self.w_locar.set_border_width(8)
        self.controle = controle

#-------Elementos       
        
        label_cliente = gtk.Label("Codigo do Cliente :")
        entry_cliente = gtk.Entry(0)

        label_dvd = gtk.Label("Codigo do DvD :")
        entry_dvd = gtk.Entry(0)
     
#------Divisao v principal

        vbox_main = gtk.VBox(False, 2)
        self.w_locar.vbox.add(vbox_main)   
#------Frame cadastra

        frame_dados = gtk.Frame("Locação")
        vbox_main.pack_start(frame_dados, False, True, 2)
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)
        
        vbox_label = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_label, False, True, 2)
       
        vbox_entry = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_entry, True, True, 2)

        vbox_label.pack_start(label_cliente, False, True, 8)
        vbox_entry.pack_start(entry_cliente, False, True, 2)

        vbox_label.pack_start(label_dvd, False, True, 8)
        vbox_entry.pack_start(entry_dvd, False, True, 2)

#-------area de notificacao
        amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
        self.hboxnotify = gtk.HBox(False)
        vbox_main.pack_start(self.hboxnotify, False, True, 2)
        event_box = gtk.EventBox()

        self.hboxnotify.pack_start(event_box, True, True, 2)        
        
        close_button = gtk.Button()
        close_button.connect("clicked", self.close_notification)
        close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.add(close)
        #close_button.set_relief(gtk.RELIEF_NONE)
        close_button.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

        self.hboxnotify.pack_start(close_button, False, True, 2)
        
        self.notify = gtk.Label()
        event_box.add(self.notify)

        event_box.realize()
        #event_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)
#-------Botoes     

        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra, entry_cliente, entry_dvd)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_locar.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()

        self.w_locar.show_all()
        self.hboxnotify.hide()
        self.w_locar.show()

#-----------------------------------------------------

class Devolver:
    def set_controle(self, controle):
        self.controle = controle
    
    def close_notification(self, widget):
        self.hboxnotify.hide()
        
    def close(self,w):
        self.w_devolver.destroy()

    def cadastra (self, widget, entry_dvd):
        cod_dvd = entry_dvd.get_text()
        try:
            self.controle.devolucao(cod_dvd)
        except:
            pass
        status = self.controle.notify()
        if status[0] == True:
            Loja.show_notify = True
            Loja.notify_text = status[1]
            self.w_devolver.hide()
        else:
            self.notify.set_text(status[1])
            self.hboxnotify.show()  
            
    def __init__(self,controle):
        self.w_devolver = gtk.Dialog()
        self.w_devolver.set_position(gtk.WIN_POS_CENTER)
        self.w_devolver.connect("destroy", self.close)
        self.w_devolver.set_title("CEF SHOP - Locar")
        self.w_devolver.set_size_request(450,250)
        self.w_devolver.set_border_width(8)
        self.controle = controle

#-------Elementos       
        
        label_dvd = gtk.Label("Codigo do DvD :")
        entry_dvd = gtk.Entry(0)

#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_devolver.vbox.add(vbox_main)      
#------Frame cadastra

        frame_dados = gtk.Frame("Devolução")
        vbox_main.pack_start(frame_dados, False, True, 2)
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)
        
        vbox_label = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_label, False, True, 2)
       
        vbox_entry = gtk.VBox(False, 4)
        vbox_labelentry.pack_start(vbox_entry, True, True, 2)

        vbox_label.pack_start(label_dvd, False, True, 8)
        vbox_entry.pack_start(entry_dvd, False, True, 2)
        
#-------area de notificacao
        amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
        self.hboxnotify = gtk.HBox(False)
        vbox_main.pack_start(self.hboxnotify, False, True, 2)
        event_box = gtk.EventBox()

        self.hboxnotify.pack_start(event_box, True, True, 2)        
        
        close_button = gtk.Button()
        close_button.connect("clicked", self.close_notification)
        close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.add(close)
        #close_button.set_relief(gtk.RELIEF_NONE)
        close_button.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)

        self.hboxnotify.pack_start(close_button, False, True, 2)
        
        self.notify = gtk.Label()
        event_box.add(self.notify)

        event_box.realize()
        #event_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)
#-------Botoes     

        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra,entry_dvd)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_devolver.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()


        self.w_devolver.show_all()
        self.hboxnotify.hide()
        self.w_devolver.show()
        
#-----------------------------------------------------

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

class popup:

    def close(self,w):
        self.w_popup.destroy()

    def __init__(self):
        self.w_popup = gtk.Dialog()
        self.w_popup.connect("destroy", self.close)
        self.w_popup.set_title("CEF - SHOP - Dialog")
        self.w_popup.set_border_width(0)
        self.w_popup.set_size_request(300, 100)

        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.close)
        self.w_popup.action_area.pack_start(button_ok, True, True, 0)
       
        label = gtk.Label("Registro gravado com sucesso!")
        self.w_popup.vbox.pack_start(label, True, True, 0)

        label.show()
        button_ok.show()
        self.w_popup.show()

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
            titulo = self.controle.listar_titulo_filme(locado[1])
            codvd = str(locado[1]) +' - '+ str(titulo[0][1])
            codcliente = str(locado[2]) +' - '+ str(locado[3])
            lista.append([codvd, codcliente, locado[4], locado[5]])
           
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
        for atrasado in atrasados:
            titulo = self.controle.listar_titulo_filme(atrasado[1])
            codvd = str(atrasado[1]) +' - '+ str(titulo[0][1])
            codcliente = str(atrasado[2]) +' - '+ str(atrasado[3])
            lista.append([codvd, codcliente, atrasado[4], atrasado[5]])

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

def iconMenuItem(title, stock):
    mItem = gtk.ImageMenuItem(title)
    im = gtk.Image()
    try:
        im.set_from_stock(stock, gtk.ICON_SIZE_MENU)
        mItem.set_image(im)
    except AttributeError:
        pass
    return mItem