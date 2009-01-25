# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.ui.objectlist import Column, ObjectList

from notify import notify_area
from iconmenu import iconMenuItem
from clientes import localizar_cliente

def popular_lista_dvds_devolucao(widget,button_adicionar, entry_cod_dvd, entry_cod_cliente, entry_nome_cliente,  controle, data, notify_box, quant_itens, lista):
    cod = entry_cod_dvd.get_text()
    try:
        dvds = controle.listar_dvds_locados(cod, quant_itens, data)
    except:
        pass
    status = controle.notify()
    if status == True:
        listado =controle.dvd_listado_check()
        if listado == False:
            cod_cliente = controle.cliente_devolucao()
            cliente = controle.listar_cliente(cod_cliente)
            entry_cod_cliente.set_text(str(cod_cliente))
            entry_nome_cliente.set_text(cliente[0][1])
            
            for dvd in dvds:
                codigo = dvd[0][0]
                titulo = dvd[0][1]
                if codigo == int(cod):
                    data.append(Dvd(codigo, titulo, True))
                else:
                    data.append(Dvd(codigo, titulo))
            lista.extend(data)
        else:
            lista.grab_focus()
    else:
        notify_box.show()
    entry_cod_dvd.set_text('')
    entry_cod_dvd.grab_focus()

class Locar:
    def set_controle(self, controle):
        self.controle = controle
        
    def close(self,w):
        self.controle.main_status = False
        self.w_locar.destroy()
        
    def sensitive(self,is_sensitive = False):
        self.entry_nome_cliente.set_sensitive(is_sensitive)
        self.entry_cod_dvd.set_sensitive(is_sensitive)
        
    def localizado(self, widget, focus):
        dadoscliente = self.controle.cliente_localizado()
        if dadoscliente[0] == True:
            self.entry_cod_cliente.set_text(str(dadoscliente[1][0][0]))
            self.entry_nome_cliente.set_text(dadoscliente[1][0][1])
            self.sensitive(True)
            self.entry_cod_dvd.grab_focus()

    def cadastra (self,widget):
        cod_cliente = self.entry_cod_cliente.get_text()
        for iten in range(self.quant_itens):
            treeiter = self.lista.get_iter(iten)
            cod_dvd = int(self.lista.get_value(treeiter, 0))
            self.controle.alugar(cod_cliente, cod_dvd)
            
        status = self.controle.notify()
        if status == True:
                self.notify_box.show()
        else:
            self.w_locar.hide()
            self.controle.main_status = True

    def remover_item(self, w):
        path = self.tree_view.get_cursor()
        if path !=(None, None):
            try:
                treeiter = self.lista.get_iter(path[0][0])
                self.lista.remove(treeiter)
                self.quant_itens -= 1
            except:
                pass

    def popular_lista_dvds(self, w):
        cod = self.entry_cod_dvd.get_text()
        try:
            dvd = self.controle.listar_dvd(cod, self.quant_itens, self.lista)
        except:
            pass
        status = self.controle.notify()
        if status == True:
            self.lista.append([dvd[0][0],dvd[0][1]])
            self.quant_itens += 1
            self.notify_box.hide()
        else:
            self.notify_box.show()
        self.entry_cod_dvd.set_text('')
        
    def create_list(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.lista = gtk.ListStore(str, str)
        self.tree_view = gtk.TreeView(self.lista)
        scrolled_window.add_with_viewport (self.tree_view)
    
        cell1 = gtk.CellRendererText()
        column1 = gtk.TreeViewColumn("Codigo - Dvd", cell1, text=0)
        
        cell2 = gtk.CellRendererText()
        column2 = gtk.TreeViewColumn("Titulo", cell2, text=1)
        
        self.tree_view.append_column(column1)
        self.tree_view.append_column(column2)

        return scrolled_window
        
    def localizar_cliente_cod(self, widget):
        cod = self.entry_cod_cliente.get_text()
        if cod is not "":
            try:
                cliente = self.controle.listar_cliente(cod)
            except:
                pass
            status = self.controle.notify()
            if status == True:
                self.entry_nome_cliente.set_text(cliente[0][1])
                self.sensitive(True)
                self.notify_box.hide()
                self.entry_cod_dvd.grab_focus()
            else:
                self.entry_nome_cliente.set_text('')
                self.sensitive(False)
                self.notify_box.show()
    
    def __init__(self,controle):
        self.w_locar = gtk.Dialog()
        self.w_locar.set_position(gtk.WIN_POS_CENTER)
        self.w_locar.connect("destroy", self.close)
        self.w_locar.connect("focus_in_event", self.localizado)
        self.w_locar.set_title("CEF SHOP - Locar")
        self.w_locar.set_size_request(650,400)
        self.w_locar.set_border_width(8)
        self.controle = controle
        self.notify_box = notify_area(self.controle)
        self.quant_itens = 0
     
#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_locar.vbox.add(vbox_main)   

#------Frame Clientes
        frame_cliente = gtk.Frame("Cliente")
        vbox_main.pack_start(frame_cliente, False, True, 2)
        
        hbox_cliente = gtk.HBox(False, 2)
        hbox_cliente.set_border_width(2)
        frame_cliente.add(hbox_cliente)
        
        f_cliente = gtk.Fixed()
    
        label_cod_cliente = gtk.Label("Codigo :")
        f_cliente.put(label_cod_cliente, 2, 8)
        
        self.entry_cod_cliente = gtk.Entry(0)        
        self.entry_cod_cliente.set_size_request(60,28)
        self.entry_cod_cliente.connect("activate", self.localizar_cliente_cod)
        f_cliente.put(self.entry_cod_cliente,60, 4)

        self.entry_nome_cliente = gtk.Entry(0)        
        self.entry_nome_cliente.set_size_request(400,28)
        self.entry_nome_cliente.set_editable(False)
        f_cliente.put(self.entry_nome_cliente,122, 4)
        
        button_localizar_cliente = gtk.Button(stock=gtk.STOCK_FIND)
        button_localizar_cliente.connect("clicked", localizar_cliente, self.w_locar, self.controle, self.notify_box)
        f_cliente.put(button_localizar_cliente,524, 0)
    
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
        
        label_cod_dvd = gtk.Label("Codigo :")
        f_dvd.put(label_cod_dvd, 2, 8)
        self.entry_cod_dvd = gtk.Entry(0)
        self.entry_cod_dvd.set_size_request(60,28)
        self.entry_cod_dvd.connect("activate", self.popular_lista_dvds)
        f_dvd.put(self.entry_cod_dvd, 60, 4)
        
        vbox_dvd.pack_start(f_dvd, False, True, 4)

        button_remover = gtk.Button(stock=gtk.STOCK_REMOVE)
        button_remover.connect("clicked", self.remover_item)
        button_adicionar = gtk.Button(stock=gtk.STOCK_ADD)
        button_adicionar.connect("clicked", self.popular_lista_dvds)

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

        liststore = self.create_list()
        frame_filmes.add(liststore)
        
#-------area de notificacao
        vbox_main.pack_start(self.notify_box, False, True, 2)

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_locar.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()
        
        self.sensitive()
        self.w_locar.show_all()
        self.notify_box.hide()
        self.w_locar.show()
#-----------------------------------------------------
class Dvd:
    def __init__(self, cod, title, check = False):
        self.check = check
        self.cod = cod
        self.title = title

    def __repr__(self):
        return '<Titulo %s>' % self.title
#----------------------------------------------------------
class Devolver:
    def set_controle(self, controle):
        self.controle = controle
    
    def close_notification(self, widget):
        self.hboxnotify.hide()
        
    def close(self,w):
        self.controle.main_status = False
        self.w_devolver.destroy()
    
    def remover_item(self, w):
        path = self.tree_view.get_cursor()
        if path !=(None, None):
            try:
                treeiter = self.lista.get_iter(path[0][0])
                self.lista.remove(treeiter)
                self.quant_itens -= 1
            except:
                pass

    def cadastra (self, widget, entry_dvd):
        for dvd in self.data:
            if dvd.check ==True:
                self.controle.devolucao(dvd.cod)
                
        status = self.controle.notify()
        if status == False:
            self.notify_box.show()
        else:
            self.w_devolver.hide()
            self.controle.main_status = True

    def __init__(self,controle):
        self.w_devolver = gtk.Dialog()
        self.w_devolver.set_position(gtk.WIN_POS_CENTER)
        self.w_devolver.connect("destroy", self.close)
        self.w_devolver.set_title("CEF SHOP - Devolução")
        self.w_devolver.set_size_request(650,400)
        self.w_devolver.set_border_width(8)
        self.controle = controle
        self.notify_box = notify_area(self.controle)
        self.quant_itens = 0

#-------Elementos       
        label_dvd = gtk.Label("Codigo do DvD :")
        entry_dvd = gtk.Entry(0)
        
        self.data = []
        columns = [
            Column('check', data_type=bool, editable=True, title="Conferido"), 
            Column('cod', data_type =int, sorted=True,  title="Código"),
            Column('title', data_type = str, title="Titulo")
        ]
        self.lista = ObjectList(columns, mode=gtk.SELECTION_MULTIPLE)
        self.lista.extend(self.data)

#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_devolver.vbox.add(vbox_main)      
 
#------Frame Clientes
        frame_cliente = gtk.Frame("Cliente")
        vbox_main.pack_start(frame_cliente, False, True, 2)
        
        hbox_cliente = gtk.HBox(False, 2)
        hbox_cliente.set_border_width(2)
        frame_cliente.add(hbox_cliente)
        
        f_cliente = gtk.Fixed()
    
        label_cod_cliente = gtk.Label("Codigo :")
        f_cliente.put(label_cod_cliente, 2, 8)
        
        self.entry_cod_cliente = gtk.Entry(0)        
        self.entry_cod_cliente.set_size_request(60,28)
        self.entry_cod_cliente.set_editable(False)
        self.entry_cod_cliente.set_sensitive(False)
        f_cliente.put(self.entry_cod_cliente,60, 4)

        self.entry_nome_cliente = gtk.Entry(0)        
        self.entry_nome_cliente.set_size_request(500,28)
        self.entry_nome_cliente.set_editable(False)
        self.entry_nome_cliente.set_sensitive(False)
        f_cliente.put(self.entry_nome_cliente,122, 4)

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
        
        button_adicionar = gtk.Button(stock=gtk.STOCK_ADD)
        
        label_cod_dvd = gtk.Label("Codigo :")
        f_dvd.put(label_cod_dvd, 2, 8)
        self.entry_cod_dvd = gtk.Entry(0)
        self.entry_cod_dvd.set_size_request(60,28)
        self.entry_cod_dvd.connect("activate", popular_lista_dvds_devolucao, button_adicionar, self.entry_cod_dvd, self.entry_cod_cliente, self.entry_nome_cliente,  self.controle, self.data, self.notify_box, self.quant_itens, self.lista)
        f_dvd.put(self.entry_cod_dvd, 60, 4)
        
        vbox_dvd.pack_start(f_dvd, False, True, 4)
        
        button_adicionar.connect("clicked", popular_lista_dvds_devolucao, button_adicionar, self.entry_cod_dvd, self.entry_cod_cliente, self.entry_nome_cliente,  self.controle, self.data, self.notify_box, self.quant_itens, self.lista)

        bbox = gtk.VButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_START)
        vbox_dvd.pack_start(bbox, False, True, 4)
        bbox.add(button_adicionar)

#------lista de filmes
        vpaned = gtk.VPaned()
        hbox_body.pack_start(vpaned, True, True, 2)
        
        frame_filmes = gtk.Frame("Lista de Locações")
        vpaned.add(frame_filmes)

        frame_filmes.add(self.lista)

#-------area de notificacao
        vbox_main.pack_start(self.notify_box,False, True, 4)

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
        self.notify_box.hide()
        self.w_devolver.show()
