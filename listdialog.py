# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

from kiwi.datatypes import currency, converter
from kiwi.ui.objectlist import Column, ObjectList, SummaryLabel
from kiwi.ui.widgets.entry import ProxyEntry
from kiwi.ui.comboentry import ComboEntry
from kiwi.ui.dialogs import yesno
from kiwi.utils import gsignal, quote


class FieldType:
    """ Classe que define um campo no diálogo ListDialog. """
    def __init__(self, field_name, titulo, tipo = str, tamanho = 0, mask = "", show_in_list = True, show_field = True, searchable = False,  identificador = False, requerido = False, tabelacombo=""):
        self.field_name = field_name
        self.titulo = titulo or field_name
        self.tipo = tipo
        self.tamanho = tamanho
        self.mask = mask 
        self.show_in_list = show_in_list
        self.show_field = show_field
        self.label = None
        self.entry = None
        self.searchable = searchable
        self.identificador = identificador
        self.requerido = requerido
        self.tabelacombo = tabelacombo

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
        self.button.set_stock_id(self.stock_id)
        if action:
            self.button.connect("clicked", action)

class ListItem:
    """ Representa um item da lista. """
    def __init__(self):
        self.new_item = False

class ListDialog:
    """ Diálogo de edição de uma tabela com botões padrão e uma lista de campos. """
    def __init__(self, controle, tabela, titulo):
        """ controle é um objeto da classe Controle.
            tabela é o nome de uma instancia de Classe no Controle que referencia um tabela no Modelo.
            titulo é nome de leitura da tabela sendo editada (ex. 'Categorias') """
        self.controle = controle
        self.tabela = getattr(self.controle, tabela)
        self.fields = []
        self.data = []
        self.buttons = []
        self.new_method = self.create_new_record
        self.save_method = self.salvar
        self.populate_method = self.populate
        self.titulo = titulo or self.tabela.nome_tabela
        self.edit_mode = False
        self.editing_new = False
        self.editing = False
        self.selection = None
        self.do_nothing = False

    def make_widget(self, fields, custom_buttons = []):
        """ Cria e retorna o widget que contém o toolbar, a lista e os campos para edição.
            fields é uma lista de FieldType.
            custom_buttons é uma lista de ListToolButton que substitui os botões padrão. """
#-------Campos
        self.fields = []
        
        for field in fields:
            if field.show_field:
                field.label = gtk.Label(field.titulo + ":")
                if field.tabelacombo:
                    field.entry = ComboEntry()
                    tabelacombo = getattr(self.controle, field.tabelacombo)
                    itens = tabelacombo.combo()
                    field.entry.prefill(itens)
                else:
                    field.entry = ProxyEntry(field.tipo)
                    field.entry.set_mask(field.mask)
            self.fields.append(field)
        
        vbox_main = gtk.VBox()
        hbox_topo = gtk.HBox()
        
        self.widget = gtk.EventBox()
#-------Toolbar
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        if not custom_buttons:
            self.tb_novo = ListToolButton(self.default_new, gtk.STOCK_NEW)
            self.tb_edit = ListToolButton(self.default_edit, gtk.STOCK_EDIT)
            self.custom_buttons = [self.tb_novo, self.tb_edit]
        else:
            self.custom_buttons = custom_buttons 

        for tool_button in self.custom_buttons:
            toolbar.insert(tool_button.button, -1)
        
#-------Lista
        vbox_lista = gtk.VBox()
        hbox_entry = gtk.HBox()
        
        self.entry_localizar = gtk.Entry()
        self.entry_localizar.connect('activate', self.localizar)
        label = gtk.Label('Localizar')
        
        frame_lista = gtk.Frame(self.titulo)
        self.listview = self.create_list()
        self.listview.connect("row_activated", self.on_row_activated)
        self.listview.connect('selection-changed',self.on_selection_changed)
        
#-------Frame
        frame_dados = gtk.Frame("Informações")
        hbox_dados = gtk.HBox(False, 6)
        vbox_label = gtk.VBox(True, 4)
        vbox_entry = gtk.VBox(True, 4)
         
        for field in self.fields:
            if field.show_field:
                vbox_label.pack_start(field.label, False, True, 8)
                vbox_entry.pack_start(field.entry, False, True, 8)
        
        #Botões
        self.button_save = gtk.Button(stock=gtk.STOCK_SAVE)
        self.button_save.connect("clicked", self.save_method)
        self.button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.button_cancel.connect("clicked", self.cancel)
        
        vbox_dados_buttons = gtk.VButtonBox()
        vbox_dados_buttons.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox_dados_buttons.add(self.button_save)
        vbox_dados_buttons.add(self.button_cancel)
        
#-------Notify
        self.notify = self.controle.notify()
        self.notify_box = self.notify.get_widget()
        self.notify.show_notify('info','Clique em NOVO para adicionar um novo item')
        self.tabela.set_notify(self.notify)

#-------Posicionar todos
        frame_lista.add(self.listview)
        vbox_lista.pack_start(hbox_entry, False, False, 2)
        vbox_lista.pack_start(frame_lista, True, True, 2)
        hbox_entry.pack_end(self.entry_localizar, False, False, 2)
        hbox_entry.pack_end(label, False, False, 2)
        hbox_topo.pack_start(toolbar, False, False, 5)
        hbox_topo.pack_start(vbox_lista, True, True, 2)
        hbox_dados.pack_start(vbox_label, False, False, 2)
        hbox_dados.pack_start(vbox_entry, True, True, 2)
        hbox_dados.pack_start(vbox_dados_buttons, False, False, 2)
        frame_dados.add(hbox_dados)
        vbox_main.pack_start(hbox_topo, True, True, 2)
        vbox_main.pack_start(frame_dados, False, False, 2)
        vbox_main.pack_start(self.notify_box, False, True, 2)
        self.widget.add(vbox_main)
        
        self.set_edit_mode(False)
        return self.widget

    def create_list(self):
        columns = []
        for field in self.fields:
            if field.show_in_list:
                columns.append(Column(field.field_name, data_type = field.tipo, title = field.titulo))
        self.lista = ObjectList(columns)
        self.data = self.populate_method()
        self.lista.extend(self.data)
        return self.lista

    def localizar(self, entry):
        text = self.entry_localizar.get_text().lower()
        searches = text.split(" ")
        if not searches: #lista vazia
            lista = self.data
        else:
            lista = []
            for item in self.data:
                itemtext = ""
                #reúne o texto inteiro do item (separado por espaço):
                for field in self.fields:
                    if field.searchable:
                        itemtext += str(getattr(item, field.field_name)).lower() + " "
                contain_all = True
                for searchtext in searches:
                    if searchtext not in itemtext:
                        contain_all = False
                if contain_all:
                    lista.append(item)
        self.lista.add_list(lista)

    def set_edit_mode(self, edit_mode):
        """ Coloca ou tira os campos em modo de edição. """
        for field in self.fields:
            if field.entry:
                field.entry.set_sensitive(edit_mode)
        
        for tool_button in self.custom_buttons:
            tool_button.button.set_sensitive(not edit_mode)
        
        self.entry_localizar.set_sensitive(not edit_mode)
        self.button_save.set_sensitive(edit_mode)
        self.button_cancel.set_sensitive(edit_mode)
        self.editing = edit_mode
        
    def cancel(self, widget):
        """Cancela a edição de um item"""
        self.set_edit_mode(False)
        self.clear_entry()
        self.lista.refresh()
        if self.editing_new:
            self.lista.remove(self.newobj)
            self.editing_new = False
            
        self.notify.show_notify('info','Clique em NOVO para adicionar um novo item')
            
    def create_new_record(self):
        """Adiciona um item padrão a lista para depois ser editado"""
        self.notify.hide()
        obj = ListItem()
        for field in self.fields:
            if field.tipo == str or field.tabelacombo:
                setattr(obj, field.field_name, '')
            else:
                setattr(obj, field.field_name, converter.from_string(field.tipo, '0'))
        return obj

    def populate(self):
        """Popula a lista com os itens"""
        itens = self.tabela.listar()
        objetos = []
        for item in itens:
            obj = ListItem()
            for field in self.fields:
                if not field.tabelacombo:
                    setattr(obj, field.field_name, item[field.field_name])
                else:
                    tabelacombo = getattr(self.controle, field.tabelacombo)
                    descricao = tabelacombo.item_descricao(item[field.field_name])
                    try:
                        setattr(obj, field.field_name, descricao[0][0])
                    except:
                        setattr(obj, field.field_name, descricao)
            objetos.append(obj)
        return objetos
        
    def default_new(self, sender):
        self.newobj = self.new_method() #Chama new_method para criar um novo item
        self.data.append(self.newobj)
        self.listview.append(self.newobj)
        self.listview.refresh()
        self.listview.select(self.newobj)
        self.set_edit_mode(True)
        self.editing_new = True
        self.item = self.selection
        
    def default_edit(self, sender):
        if self.selection:
            self.populate_entry(self.selection)
            self.set_edit_mode(True)
            self.item = self.selection
        
    def on_row_activated(self, list, item):
        """Preenche os campos com os valores da coluna clicada e coloca em modo de edição"""
        self.item = item
        self.populate_entry(item)
        
    def populate_entry(self, item):
        """Preenche os campos com os itens"""
        self.notify.hide()
        for field in self.fields:
            if field.entry:
                if field.tabelacombo:
                    field.entry.select_item_by_label(str(getattr(item, field.field_name)))
                else:
                    field.entry.set_text(str(getattr(item, field.field_name)))
        self.set_edit_mode(True)
        
    def clear_entry(self):
        """Limpa os campos apos edicao ou cancelar"""
        for field in self.fields:
            if field.entry:
                field.entry.set_text('')
        self.set_edit_mode(False)
        
    def on_selection_changed(self, list, selection):
        """Verifica se o usuario editou os campos e não salvou"""
        if self.do_nothing:
            self.do_nothing = False
            return
            
        self.selection = selection
        response = False
        if self.editing == True:
            for field in self.fields:
                if field.entry:
                    if not field.identificador:
                        user_edited = field.entry.get_text()
                        
                        #Se for um novo item
                        if self.editing_new == True:
                            if user_edited:
                                response = self.ask_to_save(field)
                                if response == True:
                                    self.salvar(None)
                                else:
                                    self.cancel(None)
                            else:
                                if response:
                                        self.do_nothing = True
                                        self.listview.select(self.item)
                                else:
                                    self.cancel(None)

                        #Se editando item da lista
                        elif self.editing == True:
                            field_in_list = (str(getattr(self.item, field.field_name)))
                            if user_edited != field_in_list:
                                response = self.ask_to_save(field)
                                if response == True:
                                    self.salvar(None)
                                else:
                                    self.cancel(None)
                            else:
                                if response:
                                        self.do_nothing = True
                                        self.listview.select(self.item)
        
    def ask_to_save(self, field):
        """Pergunta ao usuario sobre a edicao de campos"""
        #Criando um novo
        if self.editing_new : 
            question =str('Deseja salvar %s ?')
            for field in self.fields:
                if field.searchable:
                    registro = quote(str(field.entry.get_text()))
        #Editando
        else:
            question =str('Deseja salvar alterações em %s ?')
            registro = quote(str(getattr(self.item, field.field_name)))
            
        response = yesno((question) % (registro,),
                         parent=None,
                         default=gtk.RESPONSE_OK,
                         buttons=((gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL),
                                  (gtk.STOCK_SAVE, gtk.RESPONSE_OK)))
        return response == gtk.RESPONSE_OK
        
    def salvar(self, widget):
        """Insere ou edita um registro na tabela"""
        record = {}
        #Insere novo
        if self.editing_new :
            record = self.tabela.insert(self.fields)
            if record :
                for field in self.fields:
                    if field.identificador:
                        setattr(self.newobj, field.field_name, record['last_id'])
                    elif field.tabelacombo:
                        tabelacombo = getattr(self.controle, field.tabelacombo)
                        descricao = tabelacombo.item_descricao(record[field.field_name])
                        setattr(self.newobj, field.field_name, descricao[0][0])
                    else:
                        setattr(self.newobj, field.field_name, record[field.field_name])
                self.editing_new = False
                self.lista.refresh()
                self.clear_entry()
                self.hide_notify()
         #Edita
        else:
            record = self.tabela.update(self.fields, self.item)
            if record:
                for field in self.fields:
                    if field.identificador:
                        pass
                    elif field.tabelacombo:
                        tabelacombo = getattr(self.controle, field.tabelacombo)
                        descricao = tabelacombo.item_descricao(record[field.field_name])
                        try:
                            setattr(self.item, field.field_name, descricao[0][0])
                        except:
                            setattr(self.item, field.field_name, descricao)
                    else:
                        setattr(self.item, field.field_name, record[field.field_name])
                self.lista.refresh()
                self.clear_entry()
                self.hide_notify()
        
    def hide_notify(self):
        self.notify.hide()
        
""" TODO:
- Excluir (?)
"""
