# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.datatypes import currency
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel
from kiwi.ui.entry import KiwiEntry

from notify import notify_area
from iconmenu import iconMenuItem

from controle import Controle

class FieldType:
    """ Classe que define um campo no diálogo ListDialog. """
    
    def __init__(self, field_name, titulo, tipo, tamanho = 0, mask = "", show_in_list = False):
        self.field_name = field_name
        self.titulo = titulo or field_name
        self.tipo = tipo
        self.tamanho = tamanho
        self.mask = mask #Não usado ainda
        self.show_in_list = show_in_list
        self.label = None
        self.entry = None

class ListToolButton:
    """ Classe que define um botão no Toolbar. """
    
    def __init__(self, action, stock_id = 0, caption = ""):
        self.caption = caption
        self.stock_id = stock_id
        if self.stock_id == gtk.STOCK_NEW:
            self.caption = self.caption or "Novo"
        elif self.stock_id == gtk.STOCK_EDIT:
            self.caption = self.caption or "Editar"
        self.button = gtk.ToolButton(self.caption)
        if action:
            self.button.connect("clicked", action)

class ListDialog:
    """ Diálogo de edição de uma tabela com botões padrão e uma lista de campos. """
    
    def __init__(self, controle, tabela, fields, titulo):
        self.w_dialog = gtk.Dialog()
        self.w_dialog.set_position(gtk.WIN_POS_CENTER)
        self.w_dialog.connect("destroy", self.close)
        self.w_dialog.set_title("CEF SHOP - Cadastrar Categorias de Dvds ")
        self.w_dialog.set_size_request(600,450)
        self.w_dialog.set_border_width(8)

        self.controle = controle
        self.tabela = tabela
        self.fields = []
        self.data = []
        self.buttons = []
        self.titulo = titulo or self.tabela.nome_tabela

    def prepare_dialog(self, fields, data = [], custom_buttons = []):
        self.data = data
#-------Campos
        for field in fields:
            field.label = gtk.Label(field.titulo + ":")
            field.entry = gtk.Entry(field.tamanho)
            self.fields.append(field)

        hbox_topo = gtk.HBox()
        #self.w_dialog.vbox.pack_start(hbox_topo, True, True, 2)

#-------Toolbar
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        #if !custom_buttons:
        if custom_buttons == []:
            tb_novo = ListToolButton(self.default_new, gtk.STOCK_NEW)
            tb_editar = ListToolButton(self.default_edit, gtk.STOCK_EDIT)
            custom_buttons = [tb_novo, tb_editar]
        
        for tool_button in custom_buttons:
            toolbar.insert(tool_button.button, -1)

#-------Lista
        vbox_lista = gtk.VBox()
        hbox_entry = gtk.HBox()
        
        self.entry_localizar = gtk.Entry()
        self.entry_localizar.connect('activate', self.localizar)
        label = gtk.Label('Localizar')
        
        frame_lista = gtk.Frame(self.titulo)
        self.listview = self.create_list(data)

#-------Frame
        frame_dados = gtk.Frame("Informações")
        hbox_dados = gtk.HBox(False, 6)
        vbox_label = gtk.VBox(True, 4)
        vbox_entry = gtk.VBox(True, 4)
        for field in self.fields:
            vbox_label.pack_start(field.label, False, True, 8)
            vbox_entry.pack_start(field.entry, False, True, 8)

        #Botões
        button_save = gtk.Button(stock=gtk.STOCK_SAVE)
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        vbox_dados_buttons = gtk.VButtonBox()
        vbox_dados_buttons.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_dados_buttons.add(button_save)
        vbox_dados_buttons.add(button_cancel)

#-------Notify
        self.notify_box = notify_area(self.controle)

        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", self.close)
        button_close.set_flags(gtk.CAN_DEFAULT)
        hbox_buttons = gtk.HButtonBox()
        hbox_buttons.set_layout(gtk.BUTTONBOX_END)
        hbox_buttons.add(button_close)

#-------Posicionar todos
        frame_lista.add(self.listview)
        vbox_lista.pack_start(hbox_entry, False, False, 2)
        vbox_lista.pack_start(frame_lista, True, True, 2)
        hbox_entry.pack_end(self.entry_localizar, False, False, 2)
        hbox_entry.pack_end(label, False, False, 2)
        hbox_topo.pack_start(toolbar, False, False, 5)
        hbox_topo.pack_start(vbox_lista, True, True, 2)
        hbox_dados.pack_start(vbox_label, False, False, 2)
        hbox_dados.pack_start(vbox_entry, False, False, 2)
        hbox_dados.pack_start(vbox_dados_buttons, False, False, 2)
        frame_dados.add(hbox_dados)
        self.w_dialog.vbox.pack_start(hbox_topo, False, False, 2)
        self.w_dialog.vbox.pack_start(frame_dados, False, False, 2)
        self.w_dialog.vbox.pack_start(self.notify_box, False, True, 2)
        self.w_dialog.action_area.pack_start(hbox_buttons, False, True, 0)

    def create_list(self, data):
        columns = []
        for field in self.fields:
            if field.show_in_list:
                columns.append(Column(field.field_name, data_type = field.tipo, title = field.titulo))

        lista = ObjectList(columns)
        lista.extend(self.data)
        return lista

    def localizar(self, entry):
        text = self.entry_localizar.get_text().lower()
        #categoria_dvd = [categoria_dvd for categoria_dvd in self.data
        #                    if text.lower() in categoria_dvd.title.lower()]
        #self.listview.add_list(categoria_dvd)

    def show_dialog(self):
        self.w_dialog.show_all()
        self.notify_box.hide()
        self.w_dialog.show()

    def close(self, w):
        self.w_dialog.destroy()
        
    def default_new(self, sender):
        pass
    
    def default_edit(self, sender):
        pass


if __name__ == '__main__':
    controle = Controle()
    
    fields=[]
    fields.append(FieldType("nome", "Nome", int))
    tabela = []
    base =  ListDialog(controle, tabela, fields, "teste" )
    base.prepare_dialog(fields)
    base.show_dialog()
   
    gtk.main()
    
""" TODO:
- Novo, editar e excluir (?)
- Tratamentos com a lista (ao clicar em novo, editar e na lista)
- Todo o resto
"""


