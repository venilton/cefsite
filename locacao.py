# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel
from kiwi.ui.comboentry import ComboEntry


class Locar:
    class Dvd:
        def __init__(self, cod, title, valor):
            self.cod = cod
            self.title = title
            self.valor = currency(valor)
        def __repr__(self):
            return '<Titulo %s>' % self.title
    
    def set_controle(self, controle):
        self.controle = controle
        
    def close(self,w):
        self.controle.main_status = False
        self.w_locar.destroy()
        
    def sensitive(self,is_sensitive = False):
        pass
        #self.entry_nome_cliente.set_sensitive(is_sensitive)
        #self.entry_cod_dvd.set_sensitive(is_sensitive)
        
    def localizado(self, widget, focus):
        pass
    #    dadoscliente = self.controle.cliente_localizado()
      #  if dadoscliente[0] == True:
        #    self.entry_cod_cliente.set_text(str(dadoscliente[1][0][0]))
          #  self.entry_nome_cliente.set_text(dadoscliente[1][0][1])
            #self.sensitive(True)
            #self.entry_cod_dvd.grab_focus()

    def receber (self,  widget):
        pass
        #itens = self.controle.receber_locacao(self.lista)
        #Receber(self.controle, self.w_locar, itens)
        
    def cadastra (self, widget, focus):
        recebido = self.controle.get_receber_status()
        if recebido == True:
            self.controle.set_receber_status(False)
            cod_cliente = self.entry_cod_cliente.get_text()
            for iten in self.lista:
                cod_dvd = int(iten.cod)
                self.controle.alugar(cod_cliente, cod_dvd)
                
            status = self.controle.notify()
            if status == True:
                    self.notify_box.show()
            else:
                self.w_locar.hide()
                self.controle.main_status = True

    def remover_item(self, w):
        item = self.lista.get_selected_row_number()
        for itens in self.lista:
            if itens == self.lista[item]:
                self.lista.remove(itens)
        atributo = 'cod'
        self.lista.emit('cell-edited', self.lista, atributo)
        
    def popular_lista_dvds(self, w):
        cod = self.entry_cod_dvd.get_text()
        try:
            dvd = self.controle.listar_dvd(cod, self.quant_itens, self.lista)
        except:
            pass
        status = self.controle.notify()
        if status == True:
            codigo = dvd[0][0]
            titulo = dvd[0][1]
            valor = dvd[0][2]
            self.lista.append(Locar.Dvd(codigo, titulo, valor))
            atributo = 'cod'
            self.lista.emit('cell-edited', self.lista, atributo)
            self.notify_box.hide()
        else:
            self.notify_box.show()
        self.entry_cod_dvd.set_text('')

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
        self.w_locar.connect("focus_in_event", self.cadastra)
        self.w_locar.connect("focus_in_event", self.localizado)
        self.w_locar.set_title("CEF SHOP - Locar")
        self.w_locar.set_size_request(650,400)
        self.w_locar.set_border_width(8)
        self.controle = controle
        self.quant_itens = 0
     
#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_locar.vbox.add(vbox_main)   

#------Elementos
        self.data = []
        columns = [
            Column('cod', data_type =int, sorted=True,  title="Código"),
            Column('title', data_type = str, title="Titulo"),
            Column('valor', data_type = currency, title="Valor") 
        ]
        self.lista = ObjectList(columns, mode=gtk.SELECTION_MULTIPLE)
        self.lista.extend(self.data)
    
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

        #self.entry_nome_cliente = gtk.Entry(0) 
        self.entry_nome_cliente = ComboEntry()
        self.entry_nome_cliente.set_size_request(500, 26)
        
        tabelacombo = self.controle.clientes
        itens = tabelacombo.combo()
        self.entry_nome_cliente.prefill(itens)
        
        #self.entry_nome_cliente.set_editable(False)
        f_cliente.put(self.entry_nome_cliente,122, 4)
        
        #button_localizar_cliente = gtk.Button(stock=gtk.STOCK_FIND)
        #button_localizar_cliente.connect("clicked", localizar_cliente, self.w_locar, self.controle)
        #f_cliente.put(button_localizar_cliente,524, 0)
    
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
        frame_filmes = gtk.Frame("Lista de Locações")
        hbox_body.pack_start(frame_filmes, True, True, 2)
        vbox_lista = gtk.VBox(False, 2)

        frame_filmes.add(vbox_lista)
        vbox_lista.pack_start(self.lista, True, True, 2)
        
        label = SummaryLabel(klist=self.lista, column='valor', label='<b>Total:</b>',
                     value_format='<b>%s</b>')
        vbox_lista.pack_start(label, False, False, 4)

#-------area de notificacao

#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.receber)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_locar.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()
        
        self.sensitive()
        self.w_locar.show_all()
        self.w_locar.show()


class Devolver:
    class Dvd:
        def __init__(self, cod, title, valor, check = False):
            self.check = check
            self.cod = cod
            self.title = title
            self.valor = currency(valor)

        def __repr__(self):
            return '<Titulo %s>' % self.title   
        
    def popular_lista_dvds_devolucao(self, widget):
        cod = self.entry_cod_dvd.get_text()
        try:
            dvds = self.controle.listar_dvds_locados(cod, self.data)
        except:
            pass
        status = self.controle.notify()
        if status == True:
            listado =self.controle.dvd_listado_check()
            if listado == False:
                cod_cliente = self.controle.cliente_devolucao()
                cliente = self.controle.listar_cliente(cod_cliente)
                self.entry_cod_cliente.set_text(str(cod_cliente))
                self.entry_nome_cliente.set_text(cliente[0][1])
                
                for dvd in dvds:
                    codigo = dvd[0]
                    titulo = dvd[1]
                    valor = dvd[2]
                    if codigo == int(cod):
                        self.data.append(Devolver.Dvd(codigo, titulo, valor, True))
                    else:
                        self.data.append(Devolver.Dvd(codigo, titulo, valor))
                self.lista.extend(self.data)
                atributo = 'check'
                self.lista.emit('cell-edited', self.lista, atributo)
            else:
                self.lista.refresh(False)
            #self.notify_box.hide()
        else:
            pass
            #self.notify_box.show()
        self.entry_cod_dvd.set_text('')
        self.entry_cod_dvd.grab_focus()
        
    def set_controle(self, controle):
        self.controle = controle

    def close(self,w):
        self.controle.main_status = False
        self.w_devolver.destroy()
    
    def receber (self,  widget):
        itens = self.controle.receber_devolucao(self.lista)
        Receber(self.controle, self.w_devolver, itens)
    
    def cadastra (self, widget, focus):
        recebido = self.controle.get_receber_status()
        if recebido == True:
            self.controle.set_receber_status(False)
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
        self.w_devolver.connect("focus_in_event", self.cadastra)
        self.w_devolver.set_title("CEF SHOP - Devolução")
        self.w_devolver.set_size_request(650,400)
        self.w_devolver.set_border_width(8)
        self.controle = controle
        self.quant_itens = 0

#-------Elementos       
        label_dvd = gtk.Label("Codigo do DvD :")
        self.entry_dvd = gtk.Entry(0)
        
        self.data = []
        columns = [
            Column('check', data_type=bool, editable=True, title="Conferido"), 
            Column('cod', data_type =int, sorted=True,  title="Código"),
            Column('title', data_type = str, title="Titulo"),
            Column('valor', data_type = currency, title="Valor") 
        ]
        self.lista = ObjectList(columns, mode=gtk.SELECTION_NONE)
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
        self.entry_cod_dvd.connect("activate", self.popular_lista_dvds_devolucao)
        f_dvd.put(self.entry_cod_dvd, 60, 4)
        
        vbox_dvd.pack_start(f_dvd, False, True, 4)
        
        button_adicionar.connect("clicked", self.popular_lista_dvds_devolucao)

        bbox = gtk.VButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_START)
        vbox_dvd.pack_start(bbox, False, True, 4)
        bbox.add(button_adicionar)

#------lista de filmes
        frame_filmes = gtk.Frame("Lista de Locações")
        hbox_body.pack_start(frame_filmes, True, True, 2)
        vbox_lista = gtk.VBox(False, 2)

        frame_filmes.add(vbox_lista)
        vbox_lista.pack_start(self.lista, True, True, 2)
        
        label = SummaryLabel(klist=self.lista, column='valor', label='<b>Saldo Devedor:</b>',
                     value_format='<b>%s</b>')
        vbox_lista.pack_start(label, False, False, 4)
        
#-------area de notificacao


#-------Botoes     
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.receber)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_devolver.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()

        self.w_devolver.show_all()
        self.w_devolver.show()
        
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
        self.w_atrasados.set_size_request(650,350)
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
