# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

from notify import Notify


class Caixa():
    def __init__(self):
        pass

class Abertura():
    def close(self,w):
        self.w_open_caixa.destroy()
        
    def open_caixa(self, widget):
        inicial = self.entry.get_text()
        self.controle.open_caixa(inicial)
        self.w_open_caixa.destroy()
        
    def __init__(self, controle):
        self.w_open_caixa = gtk.Dialog()
        self.w_open_caixa.set_position(gtk.WIN_POS_CENTER)
        self.w_open_caixa.set_size_request(340,150)
        self.w_open_caixa.set_title("CEF SHOP - Abertura de caixa")
        self.w_open_caixa.connect("destroy", self.close)
        self.controle = controle
        
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        vbox.pack_start(hbox, True, True, 2)
        label = gtk.Label('Saldo inicial :')
        self.entry= gtk.Entry()
        hbox.pack_start(label, True, False, 2)
        hbox.pack_start(self.entry, True, False, 2)
        self.w_open_caixa.vbox.pack_start(vbox, True, False, 5)
        
#-------area de notificacao
        

#-------Botoes
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.open_caixa)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)
        bbox.add(button_ok)
        self.w_open_caixa.action_area.pack_start(bbox, False, True, 0)
    
#------Mostra tudo
        self.w_open_caixa.show_all()
        self.w_open_caixa.show()
        
class Fechamento():
    def __init__(self):
        pass
