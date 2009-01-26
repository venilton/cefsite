# coding: utf-8

import pygtk
import gtk
#from controle import Recordset

pygtk.require('2.0')

class SelectDialog:
    """ Classe que implementa uma janela de pesquisa de registros dentro de uma tabela. """

    def __init__(self, recordset, campos_retorno = []):
        """ Inicializa o objeto SelectDialog.
            recordset é o objeto Recordset que contém a lista a ser exibida e 
            campos_retorno é a lista de campos do registro selecionado que serão retornados (por padrão, todos os campos do recordset).
        """
        self.recordset = recordset
        self.campos_retorno = campos_retorno or [campo[0] for campo in self.recordset.campos]

        self.clear()

    def clear(self):
        """ Limpa (ou inicializa) as variáveis de interface. """
        self.dialog = None
        self.lista = None
        self.tree_view = None

    def activate(self, titulo = "", parent = None):
        """ Exibe o diálogo para a seleção do registro.
            Retorna None se o diálogo foi cancelado ou a tupla com campos_retorno caso tenha escolhido um item. """
        self.dialog = self.create_dialog(titulo or "Pesquisa", parent)

        for row in self.recordset.rows:
            self.lista.append(row)

        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            return
        else:
            self.dialog.hide()
            return None

    def create_dialog(self, titulo, parent):
        dialog = gtk.Dialog(titulo, parent, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_size_request(520, 470)
        dialog.set_border_width(8)

        frame_pesq = gtk.Frame("Pesquisar")
        hbox = gtk.HBox(False, 2)
        label_pesq = gtk.Label("Pesquisar por:")
        entry_pesq = gtk.Entry(0)

        hbox.set_border_width(8)
        hbox.pack_start(label_pesq, False, True, 2)
        hbox.add(entry_pesq)
        frame_pesq.add(hbox)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        # A coisa mais tosca que eu já fiz no universo
        if self.recordset.col_count() == 1:
            self.lista = gtk.ListStore(str)
        elif self.recordset.col_count() == 2:
            self.lista = gtk.ListStore(str, str)
        elif self.recordset.col_count() == 3:
            self.lista = gtk.ListStore(str, str, str)
        elif self.recordset.col_count() == 4:
            self.lista = gtk.ListStore(str, str, str, str)
        elif self.recordset.col_count() == 5:
            self.lista = gtk.ListStore(str, str, str, str, str)
        else:
            self.lista = gtk.ListStore(str, str, str, str, str, str)
        # Máximo 6 colunas

        self.tree_view = gtk.TreeView(self.lista)
        scrolled_window.add_with_viewport(self.tree_view)

        count = 0
        for titulo in self.recordset.titulos:
            cell = gtk.CellRendererText()
            column = gtk.TreeViewColumn(titulo, cell, text=count)
            self.tree_view.append_column(column)
            count += 1

        entry_pesq.connect("insert-at-cursor", self.do_search)

        dialog.vbox.pack_start(frame_pesq, False, True, 2)
        dialog.vbox.add(scrolled_window)
        dialog.show_all()
        return dialog

    def do_search(self, object):
		
        pass

""" ToDo:
X Criar a interface (campo de pesquisa, lista e botões)
- Realizar a busca (por palavras) e posicionar
- Retornar os campos do registro escolhido
"""