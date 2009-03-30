#coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from controle import * #FixME: all to controle
from iconmenu import iconMenuItem
from clientes import Cadastro_clientes
from locacao import Locar, Devolver
from guicommon import SelectDialog

from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel, ColoredColumn
from listdialog import FieldType, ListDialog

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


    def open_cad_clientes (self, widget):
        Cadastro_clientes(self.controle)
        self.close_notification(widget)
    
    def open_locar(self, widget):
        Locar(self.controle)
        self.close_notification(widget)

    def open_venda(self, widget):
        Venda(self.controle)
        self.close_notification(widget)

    def open_devolver(self, widget):
        Devolver(self.controle)
        self.close_notification(widget)
        
    def logoff(self,widget):
        self.controle.main_status = False
        self.w_loja.destroy()
        self.controle.logoff()
        
    def __init__(self, controle):
        self.w_loja = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_loja.set_position(gtk.WIN_POS_CENTER)
        self.w_loja.connect("delete_event", lambda w,e: gtk.main_quit())
        #self.w_loja.connect("focus_in_event", self.notification)
        self.w_loja.set_title("CEF SHOP - Loja")
        self.w_loja.set_size_request(580,280)
        #self.controle = controle

#---Botoes
        button_clientes = gtk.Button("Clientes")
        button_clientes.connect("clicked", self.open_cad_clientes)
    
        button_retirada = gtk.Button("Retirada")
        button_retirada.connect("clicked",self.open_locar)
      
        button_devolucao = gtk.Button("Devolução")
        button_devolucao.connect("clicked",self.open_devolver)
   
        button_venda = gtk.Button("Venda")
        button_venda.connect("clicked", self.open_venda)

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
       
        
#-------Mostra tudo
        self.w_loja.show_all()

        self.w_loja.show()

class Venda:
    """ Janela de venda de produtos. """

    def __init__(self, controle):
        self.controle = controle
        self.w_venda = gtk.Dialog()
        self.w_venda.set_position(gtk.WIN_POS_CENTER)
        self.w_venda.connect("destroy", self.close)
        self.w_venda.set_title("CEF SHOP - Venda")
        self.w_venda.set_border_width(8)
        
        hbox_main = gtk.HBox(False, 2)
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        hbox_main.add(self.notebook)
        self.newpage()

        #-Botões
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)
        button_close.set_flags(gtk.CAN_DEFAULT)
        button_close.grab_default()
        button_novo = gtk.Button(stock=gtk.STOCK_NEW)
        #button_novo.connect("clicked", self.cadastra,entry_dvd)
        button_save = gtk.Button(stock=gtk.STOCK_SAVE)
        #button_save.connect("clicked", self.cadastra,entry_dvd)
        button_cancel = gtk.Button(stock=gtk.STOCK_DELETE)

        bbox = gtk.HButtonBox()
        bbox.set_layout(gtk.BUTTONBOX_END)

        bbox.add(button_novo)
        bbox.add(button_save)
        bbox.add(button_cancel)
        bbox.add(button_close)

        self.w_venda.action_area.pack_start(bbox, False, True, 0)
        self.w_venda.vbox.add(hbox_main)

        self.w_venda.show_all()
        #self.notify_box.hide()
        self.w_venda.show()

    def close(self, widget):
        self.controle.main_status = False
        self.w_venda.destroy()
    
    def newpage(self):
        """ Inicia uma nova venda. """
        pagina = PaginaPedido()
        self.notebook.append_page(pagina.child) #, "Pedido #" + str(1))

class PaginaPedido:
    """ Classe que contém uma página de venda. """

    def __init__(self):
        self.cod_pedido = 0
        self.child = None
        vbox_main = gtk.VBox(False, 2)

        #-Cliente
        frame_cliente = gtk.Frame("Cliente")
        vbox_main.pack_start(frame_cliente, False, True, 2)

        hbox_cliente = gtk.HBox(False, 2)
        hbox_cliente.set_border_width(2)
        frame_cliente.add(hbox_cliente)
        f_cliente = gtk.Fixed()
    
        label_cod_cliente = gtk.Label("Código:")
        f_cliente.put(label_cod_cliente, 2, 8)

        self.entry_cod_cliente = gtk.Entry(0)
        self.entry_cod_cliente.set_size_request(60, 28)
        #self.entry_cod_cliente.connect("activate", self.localizar_cliente_cod)
        f_cliente.put(self.entry_cod_cliente, 60, 4)

        self.entry_nome_cliente = gtk.Entry(0)
        self.entry_nome_cliente.set_size_request(400,28)
        self.entry_nome_cliente.set_editable(False)
        f_cliente.put(self.entry_nome_cliente, 122, 4)
        
        """ button_localizar_cliente = gtk.Button(stock=gtk.STOCK_FIND)
        button_localizar_cliente.connect("clicked", localizar_cliente, self.w_locar, self.controle, self.notify_box)
        f_cliente.put(button_localizar_cliente, 524, 0) """
    
        hbox_cliente.pack_start(f_cliente, False, True, 4)

#---divisao h
        hbox_body = gtk.HBox(False, 2)
        vbox_main.pack_start(hbox_body, True, True, 2)
        
#------framecod dvds

        f_dvd = gtk.Fixed()
        frame_dvds = gtk.Frame("DvDs")
        hbox_body.pack_start(frame_dvds, False, True, 2)
        
        vbox_dvd = gtk.VBox(False, 2)
        vbox_dvd.set_border_width(2)
        frame_dvds.add(vbox_dvd)
        
        label_cod_dvd = gtk.Label("Codigo:")
        f_dvd.put(label_cod_dvd, 2, 8)
        self.entry_cod_dvd = gtk.Entry(0)
        self.entry_cod_dvd.set_size_request(60,28)
        #self.entry_cod_dvd.connect("activate", self.popular_lista_dvds)
        f_dvd.put(self.entry_cod_dvd, 60, 4)
        
        vbox_dvd.pack_start(f_dvd, False, True, 4)

        button_remover = gtk.Button(stock=gtk.STOCK_REMOVE)
        #button_remover.connect("clicked", self.remover_item)
        button_adicionar = gtk.Button(stock=gtk.STOCK_ADD)
        #button_adicionar.connect("clicked", self.popular_lista_dvds)

        bbox = gtk.VButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_START)
        vbox_dvd.pack_start(bbox, False, True, 4)
        
        bbox.add(button_adicionar)
        bbox.add(button_remover)

#------lista de filmes
        vpaned = gtk.VPaned()
        hbox_body.pack_start(vpaned, True, True, 2)
        
        frame_filmes = gtk.Frame("Lista de Locações")
        vpaned.add(frame_filmes)

        #liststore = self.create_list()
        #frame_filmes.add(liststore)
        
#-------area de notificacao
        #vbox_main.pack_start(self.notify_box, False, True, 2)
        self.child = gtk.EventBox()
        self.child.add(vbox_main)

class Categorias:
    def close(self,w):
        self.w_categorias.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_categorias = gtk.Dialog()
        self.w_categorias.set_position(gtk.WIN_POS_CENTER)
        self.w_categorias.connect("destroy", self.close)
        self.w_categorias.set_title("CEF SHOP - Cadastrar Categorias de produtos")
        self.w_categorias.set_size_request(600,450)
        self.w_categorias.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_categoria', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('nome', 'Nome', str, 0, None, searchable = True, requerido = True))
        fields.append(FieldType('cod_conta_padrao', 'Conta padrão', str, 0, None, searchable = True, requerido = False))
        
        listobject =  ListDialog(self.controle, 'categorias', 'Categorias')
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_categorias.action_area.pack_start(button_close, False, True, 0)        
        self.w_categorias.vbox.pack_start(widget,True, True, 2)
        
        self.w_categorias.show_all()
        self.w_categorias.show()

#-----------------------------------------------------    
class Contas:
    def close(self,w):
        self.w_contas.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_contas = gtk.Dialog()
        self.w_contas.set_position(gtk.WIN_POS_CENTER)
        self.w_contas.connect("destroy", self.close)
        self.w_contas.set_title("CEF SHOP - Cadastrar Contas")
        self.w_contas.set_size_request(600,450)
        self.w_contas.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_conta', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('nome', 'Nome', str, 0, None, searchable = True, requerido = True))
        fields.append(FieldType('faturar', '% fatura', float, 0, None, searchable = False, requerido = False))
        
        listobject =  ListDialog(self.controle, 'contas', 'Contas')
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_contas.action_area.pack_start(button_close, False, True, 0)        
        self.w_contas.vbox.pack_start(widget,True, True, 2)
        
        self.w_contas.show_all()
        self.w_contas.show()

#-----------------------------------------------------    
class Produtos:
    def close(self,w):
        self.w_produtos.destroy()

    def __init__(self, controle):
 #----Janela       
        self.w_produtos = gtk.Dialog()
        self.w_produtos.set_position(gtk.WIN_POS_CENTER)
        self.w_produtos.connect("destroy", self.close)
        self.w_produtos.set_title("CEF SHOP - Cadastrar Produtos")
        self.w_produtos.set_size_request(600,450)
        self.w_produtos.set_border_width(8)
        self.controle = controle
        
#-----ListObject
        fields=[]
        fields.append(FieldType('cod_produto', '#', int, 0, None, True, False, identificador = True,))
        fields.append(FieldType('cod_categoria', 'Categoria', int, 0, None, True, False, tabelacombo = "categorias"))
        fields.append(FieldType('nome', 'Nome', str, 0, None, searchable = True, requerido = True))
        fields.append(FieldType('descricao', 'Descrição', str, 0, None, searchable = True, requerido = False))
        fields.append(FieldType('preco', 'Preço', float, 0, None, searchable = True, requerido = True))
        fields.append(FieldType('ativo', 'Ativo', int, 0, None, show_in_list = False, searchable = True, requerido = False))
        
        listobject =  ListDialog(self.controle, 'produtos', 'Produtos')
        widget = listobject.make_widget(fields)
        
#-------Botoes     
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)

#-----Empacota e mostra
        self.w_produtos.action_area.pack_start(button_close, False, True, 0)        
        self.w_produtos.vbox.pack_start(widget,True, True, 2)
        
        self.w_produtos.show_all()
        self.w_produtos.show()
#-----------------------------------------------------    

