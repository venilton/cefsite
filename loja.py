# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from notify import notify_area
from iconmenu import iconMenuItem
from clientes import Cadastro_clientes
from locacao import Locar, Devolver

class Loja:   
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
        #menuitem.connect('activate', self.close) # FixMe : fechar implica passar para a classe login destroy event
        menu.add(menuitem)

    def notification (self, widget, focus):
        status = self.controle.main_notify()
        if status == True:
            self.notify_box.show()
    
    def close_notification(self, widget):
        self.controle.main_status = False
        self.notify_box.hide()

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
        self.controle.main_status = False
        self.notify_box.hide()
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
        self.notify_box = notify_area(self.controle, True,  'apply')

#---Botoes
        button_clientes = gtk.Button("Clientes")
        button_clientes.connect("clicked", self.open_cad_clientes)
    
        button_retirada = gtk.Button("Retirada")
        button_retirada.connect("clicked",self.open_locar)
      
        button_devolucao = gtk.Button("Devolução")
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
        vbox_main.pack_start(self.notify_box,False, True, 4)
        
#-------Mostra tudo
        self.w_loja.show_all()
        self.notify_box.hide()
        self.w_loja.show()
