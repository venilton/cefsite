# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk


class Admin:
    def createMenus(self, vbox):
        self.menubar = gtk.MenuBar()
        vbox.pack_start(self.menubar, expand=False)

        topmenuitem = gtk.MenuItem('_Menu')
        self.menubar.add(topmenuitem)
    
        menu = gtk.Menu()
        topmenuitem.set_submenu(menu)
 
        menuitem =self.controle.icon_menu(('_Logoff'), gtk.STOCK_QUIT)
        menu.add(menuitem)
        menuitem.connect('activate', self.logoff)

        menuitem =self.controle.icon_menu(('_Fechar'),gtk.STOCK_CLOSE)
        #menuitem.connect('activate', gtk.main_quit())
        menu.add(menuitem)
    
    def open_categorias_dvd(self, widget):
        self.controle.open.categorias_dvd(self.controle)
    
    def open_generos(self, widget):
        self.controle.open.generos(self.controle)
        
    def open_filmes(self, widget):
        self.controle.open.filmes(self.controle)

    def open_dvds(self, widget):
        self.controle.open.dvds(self.controle)

    def open_locados(self, widget):
        self.controle.open.locados(self.controle)

    def open_atrasados(self, widget):
        self.controle.open.atrasados(self.controle)
        
    def open_categorias(self, widget):
        self.controle.open.categorias(self.controle)
    
    def open_contas(self, widget):
        self.controle.open.contas(self.controle)
        
    def open_produtos(self, widget):
        self.controle.open.produtos(self.controle)

    def logoff(self,widget):
        self.w_admin.destroy()
        self.controle.logoff()
    
    def __init__(self, controle):
        self.w_admin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_admin.set_position(gtk.WIN_POS_CENTER)
        self.w_admin.connect("delete_event", lambda w,e: gtk.main_quit())
        self.w_admin.set_title("CEF SHOP - Administração")
        self.w_admin.set_size_request(580,350)
        self.controle = controle

#---Botoes
        button_generos = gtk.Button("Generos")
        button_generos.connect("clicked", self.open_generos)
        
        button_categorias_dvd = gtk.Button("Categorias")
        button_categorias_dvd.connect("clicked", self.open_categorias_dvd)
        
        button_filmes = gtk.Button("Filmes")
        button_filmes.connect("clicked",self.open_filmes)
       
        button_dvds = gtk.Button("DvDs")
        button_dvds.connect("clicked",self.open_dvds)
       
        button_locados = gtk.Button("Locados")
        button_locados.connect("clicked",self.open_locados)
       
        button_atrasados = gtk.Button("Atrasados")
        button_atrasados.connect("clicked",self.open_atrasados)

        #--Loja
        button_categorias = gtk.Button("Categorias")
        button_categorias.connect("clicked",self.open_categorias)
        
        button_contas = gtk.Button("Contas")
        button_contas.connect("clicked",self.open_contas)
        
        button_produtos = gtk.Button("Produtos")
        button_produtos.connect("clicked",self.open_produtos)

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
        vbox2 = gtk.VBox(True, 1)
     
#------Frame cadastro
        frame_cad = gtk.Frame("Locadora")

        vbox_cad=gtk.VButtonBox()
        vbox_cad.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_cad.set_spacing(10)

#------Frame Controle
        frame_controle = gtk.Frame("Controle")
 
        vbox_controle=gtk.VButtonBox()
        vbox_controle.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_controle.set_spacing(10)
        
#------Frame Loja
        frame_loja = gtk.Frame("Loja")
        
        vbox_loja = gtk.VButtonBox()
        vbox_loja.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_loja.set_spacing(10)

        #--------
        vbox_cad.add(button_categorias_dvd)
        vbox_cad.add(button_generos)
        vbox_cad.add(button_filmes)
	vbox_cad.add(button_dvds)
        frame_cad.add(vbox_cad)
        vbox1.pack_start(frame_cad, True, True, 2)
        
        vbox_controle.add(button_locados)
        vbox_controle.add(button_atrasados)
        frame_controle.add(vbox_controle)
        vbox1.pack_start(frame_controle, True, True, 2)
        
        vbox_loja.add(button_categorias)
        vbox_loja.add(button_contas)
        vbox_loja.add(button_produtos)
        frame_loja.add(vbox_loja)
        vbox2.pack_start(frame_loja, True, True, 2)

        hbox_main.pack_start(vbox1, True, True, 2)
        hbox_main.pack_start(vbox2, True, True, 2)
#-------area de notificacao
        #vbox_main.pack_start(self.notify_box,False, True, 4)

#-------Mostra tudo
        self.w_admin.show_all()
        #self.notify_box.hide()
        self.w_admin.show()
#-----------------------------------------------------
