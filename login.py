# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

from iconmenu import iconMenuItem

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
        #caixa_status = self.controle.get_caixa_status()
        #if caixa_status == 'Closed':
          #  Abertura(self.controle)
        #if caixa_status == 'NotClosed':
          #  self.controle.close_caixa()
            #Abertura(self.controle)
            
        #Loja(self.controle)
        
        self.controle.open_loja(self.controle)
        #list = ListDialog(self.controle, self.controle.modelo.categorias, [], 'Categoria')
        #list.prepare_dialog
        self.w_login.hide()

    def open_admin (self, widget):
        self.controle.open_admin(self.controle)
        #Admin(self.controle)
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
