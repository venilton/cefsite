# coding: utf-8

import pygtk
import gtk
from controle import *
from kiwi.ui.objectlist import Column, ObjectList

class SelectDialog:
    """ Classe que implementa uma janela de pesquisa de registros dentro de uma tabela. """

    def __init__(self, recordset, campos_retorno = []):
        """ Inicializa o objeto SelectDialog.
            recordset é o objeto Recordset que contém a lista a ser exibida e 
            campos_retorno é a lista de campos do registro selecionado que serão retornados (por padrão, todos os campos do recordset).
        """
        self.recordset = recordset
        self.view_items = self.recordset.items
        self.campos_retorno = campos_retorno or [col.attribute for col in self.recordset.columns]

        self.clear()

    def clear(self):
        """ Limpa (ou inicializa) as variáveis de interface. """
        self.dialog = None
        self.lista = None
        self.entry_pesq = None

    def activate(self, titulo = "", parent = None):
        """ Exibe o diálogo para a seleção do registro.
            Retorna None se o diálogo foi cancelado ou a tupla com campos_retorno caso tenha escolhido um item. """
        self.dialog = self.create_dialog(titulo or "Pesquisa", parent)
        self.lista.add_list(self.view_items)

        ret = None
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            selected = self.lista.get_selected()
            ret = [getattr(selected, campo) for campo in self.campos_retorno]
        self.dialog.hide()
        return ret

    def create_dialog(self, titulo, parent):
        dialog = gtk.Dialog(titulo, parent, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_size_request(520, 470)
        dialog.set_border_width(8)

        frame_pesq = gtk.Frame("Pesquisar")
        hbox = gtk.HBox(False, 2)
        label_pesq = gtk.Label("Pesquisar por:")
        self.entry_pesq = gtk.Entry(0)

        hbox.set_border_width(8)
        hbox.pack_start(label_pesq, False, True, 2)
        hbox.add(self.entry_pesq)
        frame_pesq.add(hbox)

        self.lista = ObjectList(self.recordset.columns)
        #scrolled_window = gtk.ScrolledWindow()
        #scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #scrolled_window.add(self.lista)

        self.entry_pesq.connect("backspace", self.do_search)

        dialog.vbox.pack_start(frame_pesq, False, True, 2)
        dialog.vbox.add(self.lista)
        dialog.show_all()
        return dialog

    def do_search(self, entry):
        text = self.entry_pesq.get_text().lower()
        if text:
            self.view_items = [item for item in self.recordset.items
                if text in getattr(item, 'nome')]
        else:
            self.view_items = self.recordset.items
        self.lista.add_list(self.view_items)

""" ToDo:
X Criar a interface (campo de pesquisa, lista e botões)
- Realizar a busca (por palavras) e posicionar
X Retornar os campos do registro escolhido
"""