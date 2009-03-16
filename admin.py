# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from notify import Notify
from iconmenu import iconMenuItem
from locacao import Locados, Atrasados
from dvds import *

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
        #menuitem.connect('activate', gtk.main_quit())
        menu.add(menuitem)
    
    def open_categorias_dvd(self, widget):
        Categorias(self.controle)
    
    def open_generos(self, widget):
        Generos(self.controle)
        
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
        self.notify_box = Notify()

#---Botoes
        button_generos = gtk.Button("Generos")
        button_generos.connect("clicked", self.open_generos)
        
        button_categorias_dvd = gtk.Button("Categorias")
        button_categorias_dvd.connect("clicked", self.open_categorias_dvd)
        
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
        
        vbox_cad.add(button_categorias_dvd)
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
        
#-------area de notificacao
        vbox_main.pack_start(self.notify_box,False, True, 4)

#-------Mostra tudo
        self.w_admin.show_all()
        self.notify_box.hide()
        self.w_admin.show()
#-----------------------------------------------------
