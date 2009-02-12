# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
from kiwi.ui.objectlist import Column, ObjectList

from notify import notify_area
from iconmenu import iconMenuItem


def entry_activate_cb(entry, lista, data):
    text = entry.get_text()
    clientes = [cliente for cliente in data
                        if text.lower() in cliente.nome.lower()]
    lista.add_list(clientes)
    print 

def on_row_activated( list, cliente, controle, w_localiza_clientes):
    dadoscliente = controle.listar_cliente(cliente.cod)
    controle.cliente_encontrado = True
    controle.dadoscliente = dadoscliente
    w_localiza_clientes.hide()

def localizar_cliente(self, window, controle, notify):
    notify.hide() #Fixme
    w_localiza_clientes = gtk.Dialog("CEF SHOP - Localizar Cliente", window, gtk.DIALOG_MODAL)
    w_localiza_clientes.set_position(gtk.WIN_POS_CENTER)
    w_localiza_clientes.set_size_request(580,300)
    w_localiza_clientes.connect("destroy", lambda w: w_localiza_clientes.hide())

#------Lista

    frame_locados = gtk.Frame("Clientes")
    w_localiza_clientes.vbox.add(frame_locados)
    
    vbox = gtk.VBox()
    frame_locados.add(vbox)
    
    columns = [
    Column('cod', data_type =int, sorted=True),
    Column('nome', data_type = str),
    ]
    data =[]
    dadoscliente = controle.locate_clientes()
    for cliente in dadoscliente:
        codigo = cliente[0]
        nome = cliente[1]
        data.append(Cliente(codigo, nome))

    lista = ObjectList(columns)
    lista.extend(data)
    lista.connect("row_activated",  on_row_activated,  controle, w_localiza_clientes)
    
    entry = gtk.Entry()
    entry.connect('activate', entry_activate_cb, lista, data )
    vbox.pack_start(entry, False, False, 6)

    vbox.pack_start(lista)
    
    #-------Botoes     
    button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
    button_cancel.connect("clicked", lambda w: w_localiza_clientes.hide())
    #button_ok = gtk.Button(stock=gtk.STOCK_OK)
    #button_ok.connect("clicked", self.localizar_selecionado)

    bbox = gtk.HButtonBox ()
    bbox.set_layout(gtk.BUTTONBOX_END)
    w_localiza_clientes.action_area.pack_start(bbox, False, True, 0)
    
    bbox.add(button_cancel)
    button_cancel.set_flags(gtk.CAN_DEFAULT)

    #bbox.add(button_ok)
    button_cancel.grab_default()

    w_localiza_clientes.show_all()
    w_localiza_clientes.show()
    
class Cliente:
    def __init__(self, cod, nome):
        self.nome = nome
        self.cod = cod

    def __repr__(self):
        return '<Cliente %s>' % self.nome

class Cadastro_clientes:
    def set_controle(self, controle):
        self.controle = controle
        
    def close(self,w):
        self.controle.main_status = False
        self.w_cad_clientes.destroy()
    
    def sensitive(self,is_sensitive):
        self.entry_nome.set_sensitive(is_sensitive)
        self.entry_telefone.set_sensitive(is_sensitive)
        self.entry_celular.set_sensitive(is_sensitive)
        self.entry_endereco.set_sensitive(is_sensitive)
        self.entry_bairro.set_sensitive(is_sensitive)
        self.entry_cidade.set_sensitive(is_sensitive)
        self.entry_estado.set_sensitive(is_sensitive)
        self.entry_cep.set_sensitive(is_sensitive)
    
    def localizado(self, widget, focus):
        dadoscliente = self.controle.cliente_localizado()       
        if dadoscliente[0] == True:
            self.cod = dadoscliente[1][0][0]
            self.entry_nome.set_text(dadoscliente[1][0][1])
            self.entry_telefone.set_text(dadoscliente[1][0][2])
            self.entry_celular.set_text(dadoscliente[1][0][3])
            self.entry_endereco.set_text(dadoscliente[1][0][4])
            self.entry_bairro.set_text(dadoscliente[1][0][5])
            self.entry_cidade.set_text(dadoscliente[1][0][6])
            self.entry_estado.set_text(dadoscliente[1][0][7])
            self.entry_cep.set_text(dadoscliente[1][0][8])
        
            self.is_sensitive = False
            self.sensitive(self.is_sensitive)
            self.tb_editar.set_sensitive(True)
        
    def novo(self, widget):
        self.is_sensitive = True
        self.sensitive(self.is_sensitive)
        self.editando = False
        self.tb_editar.set_sensitive(False)
        self.entry_nome.set_text("")
        self.entry_telefone.set_text("")
        self.entry_celular.set_text("")
        self.entry_endereco.set_text("")
        self.entry_bairro.set_text("")
        self.entry_cidade.set_text("")
        self.entry_estado.set_text("")
        self.entry_cep.set_text("")

    def editar(self, widget):
        self.is_sensitive = True
        self.sensitive(self.is_sensitive)
        self.editando = True
        
    def excluir(self, widget):
        pass
    
    def cadastra (self, widget):
        if self.is_sensitive is True:
            name = self.entry_nome.get_text()
            telefone = self.entry_telefone.get_text()
            celular = self.entry_celular.get_text()
            endereco = self.entry_endereco.get_text()
            bairro = self.entry_bairro.get_text()
            cidade = self.entry_cidade.get_text()
            estado = self.entry_estado.get_text()
            cep = self.entry_cep.get_text()
            
            if self.editando == True:
                try:
                    self.controle.cadastra_cliente(self.cod, name, telefone, celular, endereco, bairro, cidade, estado, cep, True)
                except:
                    pass  
                self.is_sensitive = False
                self.sensitive(self.is_sensitive)
            else:
                try:
                    self.controle.cadastra_cliente(None, name, telefone, celular, endereco, bairro, cidade, estado, cep, False)
                except:
                    pass
            status = self.controle.notify()
            if status == True:
                self.notify_box.show()
            else:
                self.w_cad_clientes.hide()
                self.controle.main_status = True
            
    def __init__(self,controle):
        self.w_cad_clientes = gtk.Dialog()
        self.w_cad_clientes.set_position(gtk.WIN_POS_CENTER)
        self.w_cad_clientes.set_size_request(580,460)
        #self.w_cad_clientes.set_border_width(8)
        self.w_cad_clientes.set_title("CEF SHOP - Cadastro de Clientes")
        self.w_cad_clientes.connect("destroy", self.close)
        self.w_cad_clientes.connect("focus_in_event", self.localizado)
        self.controle = controle
        self.is_sensitive = True
        self.editando = False
        self.cliente_selecionado = False
        self.dadoscliente = None
        self.notify_box = notify_area(self.controle)

#------Toolbar
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        self.w_cad_clientes.vbox.pack_start(toolbar, False, False, 5)

        tb_novo = gtk.ToolButton("Novo")
        tb_novo.set_stock_id(gtk.STOCK_NEW)
        tb_novo.connect("clicked", self.novo)
        toolbar.insert(tb_novo, -1)

        tb_procura = gtk.ToolButton("Localizar")
        tb_procura.set_stock_id(gtk.STOCK_FIND)
        tb_procura.connect("clicked", localizar_cliente, self.w_cad_clientes, self.controle, self.notify_box)
        toolbar.insert(tb_procura, -1)
        
        self.tb_editar = gtk.ToolButton("Editar")
        self.tb_editar.set_sensitive(False)
        self.tb_editar.set_stock_id(gtk.STOCK_EDIT)
        self.tb_editar.connect("clicked", self.editar)
        toolbar.insert(self.tb_editar, -1)
        
        #tb_delete = gtk.ToolButton("Excluir")
        #tb_delete.set_stock_id(gtk.STOCK_DELETE)
        #tb_delete.connect("clicked", self.excluir)
        #toolbar.insert(tb_delete, -1)

#------Frame Dados pessoais
        frame_dados = gtk.Frame("Dados Pessoais")
        self.w_cad_clientes.vbox.pack_start(frame_dados,False, True, 4)       
      
        vbox_labelentry = gtk.HBox(False, 4)
        vbox_labelentry.set_border_width(4)
        frame_dados.add(vbox_labelentry)

        f_campos = gtk.Fixed()
        #f_label = gtk.Fixed()
        
        label_nome = gtk.Label("Nome :")
        f_campos.put(label_nome, 2, 14)
        self.entry_nome = gtk.Entry(0)
        self.entry_nome.set_size_request(480,28)
        f_campos.put(self.entry_nome, 70, 10)
        
       # label_cpf = gtk.Label("CPF :")
        #f_campos.put(label_cpf, 2, 44)
        #self.entry_cpf = gtk.Entry(0)
        #self.entry_cpf.set_size_request(200,28)
        #f_campos.put(self.entry_cpf, 70, 40)

        label_telefone = gtk.Label("Telefone :")
        f_campos.put(label_telefone, 2, 74)
        self.entry_telefone = gtk.Entry(0)
        self.entry_telefone.set_size_request(200,28)
        f_campos.put(self.entry_telefone, 70, 70)
        
        label_celular = gtk.Label("Celular :")
        f_campos.put(label_celular, 280, 74)
        self.entry_celular = gtk.Entry(0)
        self.entry_celular.set_size_request(200,28)
        f_campos.put(self.entry_celular, 350, 70)
        
        label_endereco = gtk.Label("Endereco :")
        f_campos.put(label_endereco, 2, 134)
        self.entry_endereco = gtk.Entry(0)
        self.entry_endereco.set_size_request(200,28)
        f_campos.put(self.entry_endereco, 70, 130)
        
        label_bairro = gtk.Label("Bairro :")
        f_campos.put(label_bairro, 2, 164)
        self.entry_bairro = gtk.Entry(0)
        self.entry_bairro.set_size_request(200,28)
        f_campos.put(self.entry_bairro, 70, 160)
        
        label_cidade = gtk.Label("Cidade :")
        f_campos.put(label_cidade, 2, 194)
        self.entry_cidade = gtk.Entry(0)
        self.entry_cidade.set_size_request(200,28)
        f_campos.put(self.entry_cidade, 70, 190)
        
        label_estado = gtk.Label("Estado :")
        f_campos.put(label_estado, 2, 224)
        self.entry_estado = gtk.Entry(0)
        self.entry_estado.set_size_request(200,28)
        f_campos.put(self.entry_estado, 70, 220)
        
        label_cep = gtk.Label("Cep :")
        f_campos.put(label_cep, 2, 254)
        self.entry_cep = gtk.Entry(0)
        self.entry_cep.set_size_request(200,28)
        f_campos.put(self.entry_cep, 70, 250)
        
        vbox_labelentry.pack_start(f_campos, False, True, 4)

#-------area de notificacao
        self.w_cad_clientes.vbox.pack_start(self.notify_box,False, True, 4)
        
#-------Botoes
        button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        button_cancel.connect("clicked", self.close)
        button_ok = gtk.Button(stock=gtk.STOCK_OK)
        button_ok.connect("clicked", self.cadastra)

        bbox = gtk.HButtonBox ()
        bbox.set_layout(gtk.BUTTONBOX_END)
        self.w_cad_clientes.action_area.pack_start(bbox, False, True, 0)
        
        bbox.add(button_cancel)
        button_cancel.set_flags(gtk.CAN_DEFAULT)

        bbox.add(button_ok)
        button_cancel.grab_default()
    
#------Mostra tudo
        self.w_cad_clientes.show_all()
        self.notify_box.hide()
        self.w_cad_clientes.show()
