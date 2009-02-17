# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel

from notify import notify_area


class Receber():
    class Item:
        def __init__(self,item, valor):
            self.item = item
            self.valor = currency(valor)
        def __repr__(self):
            return '<Titulo %s>' % self.item
    
    def close(self,w):
        self.w_receber.destroy()
        
    def recebido(self, widget):
        self.controle.set_receber_status(True)   
        self.w_receber.destroy()
        
    def __init__(self, controle, window, itens):
        self.w_receber = gtk.Dialog("CEF SHOP - Recebimento", window, gtk.DIALOG_MODAL)
        self.w_receber.set_position(gtk.WIN_POS_CENTER)
        self.w_receber.set_size_request(550,450)
        self.w_receber.connect("destroy", self.close)
        self.controle = controle

#------Divisao v principal
        vbox_main = gtk.VBox(False, 2)
        self.w_receber.vbox.add(vbox_main)   

#------Elementos
        self.data = []
        columns = [
            Column('item', data_type = str, title="Item"),
            Column('valor', data_type = currency, title="Valor") 
        ]
        self.lista = ObjectList(columns)
        for iten in itens:
            item = iten[0]
            valor = iten[1]
            self.data.append(Receber.Item(item, valor))
        self.lista.extend(self.data)

        
#------lista de filmes       
        frame_filmes = gtk.Frame("Lista de Locações")
        vbox_main.pack_start(frame_filmes, True, True, 2)
        vbox_lista = gtk.VBox(False, 2)

        frame_filmes.add(vbox_lista)
        vbox_lista.pack_start(self.lista, True, True, 2)
        
        label = SummaryLabel(klist=self.lista, column='valor', label='<b>Total:</b>',
                     value_format='<b>%s</b>')
        vbox_lista.pack_start(label, False, False, 4)
        
        
#-------area de notificacao
        #self.notify_box = notify_area(self.controle)
        #self.w_receber.vbox.pack_start(self.notify_box,False, True, 4)

#-------Botoes
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.recebido)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)
        bbox.add(button_ok)
        self.w_receber.action_area.pack_start(bbox, False, True, 0)
    
#------Mostra tudo
        self.w_receber.show_all()
        #self.notify_box.hide()
        self.w_receber.show()

