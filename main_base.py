# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
        
def notify_area(controle, main_notify = False):
    amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
    event_box = gtk.EventBox()
    hboxnotify = gtk.HBox(False)
    event_box.add(hboxnotify)
    
    notify = gtk.Label()
    hboxnotify.pack_start(notify, True, True, 2)
    if main_notify == False:
        controle.get_notify_label(notify)
    else:
        controle.get_main_notify_label(notify)
    
    close_button = gtk.Button()
    close_button.connect("clicked",lambda w: event_box.hide())
    close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
    close_button.add(close)
    close_button.set_relief(gtk.RELIEF_NONE)
    hboxnotify.pack_start(close_button, False, True, 2)
    
    event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)
    return event_box

def iconMenuItem(title, stock):
    mItem = gtk.ImageMenuItem(title)
    im = gtk.Image()
    try:
        im.set_from_stock(stock, gtk.ICON_SIZE_MENU)
        mItem.set_image(im)
    except AttributeError:
        pass
    return mItem
    
def localizar_cliente(self, window, controle, notify):
    notify.hide()
    w_localiza_clientes = gtk.Dialog("CEF SHOP - Localizar Cliente", window, gtk.DIALOG_MODAL)
    w_localiza_clientes.set_position(gtk.WIN_POS_CENTER)
    w_localiza_clientes.set_size_request(480,220)
    w_localiza_clientes.connect("destroy", lambda w: w_localiza_clientes.hide())
#------Lista
    vpaned = gtk.VPaned()
    w_localiza_clientes.vbox.add(vpaned)

    frame_locados = gtk.Frame("Clientes")
    vpaned.add(frame_locados)

    liststore = create_list_localizar_cliente(controle, w_localiza_clientes)
    frame_locados.add(liststore)
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
    
def create_list_localizar_cliente(controle, w_localiza_clientes):
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    lista = gtk.ListStore(str, str)
    tree_view = gtk.TreeView(lista)
    scrolled_window.add_with_viewport (tree_view)

    clientes = controle.locate_clientes()
    for cliente in clientes:
        codigo = cliente[0]
        nome = cliente[1]
        lista.append([codigo, nome])
       
    cell1 = gtk.CellRendererText()
    column1 = gtk.TreeViewColumn("Codigo", cell1, text=0)
    
    cell2 = gtk.CellRendererText()
    column2 = gtk.TreeViewColumn("Nome", cell2, text=1)
    
    tree_view.append_column(column1)
    tree_view.append_column(column2)
    
    tree_view.connect("row_activated",  localizar_cliente_selecionado, lista, controle, w_localiza_clientes)
    return scrolled_window
    

def localizar_cliente_selecionado( treeview, path, view_column, lista, controle, w_localiza_clientes):
    treeiter = lista.get_iter(path)
    value = int(lista.get_value(treeiter, 0))
    dadoscliente = controle.listar_cliente(value)
    controle.cliente_encontrado = True
    controle.dadoscliente = dadoscliente
    w_localiza_clientes.hide()
    
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
        menuitem.connect('activate', gtk.main_quit)
        menu.add(menuitem)
    
    def notification (self, widget, focus):
        status = self.controle.main_notify()
        if status == True:
            self.notify_box.show()
    
    def close_notification(self, widget):
        self.controle.main_status = False
        self.notify_box.hide()

    def open_cad_clientes (self, widget):
        Cadastro_clientes(self.controle)
        self.close_notification(widget)
    
    def open_locar(self, widget):
        Locar(self.controle)
        self.close_notification(widget)
        
    def open_devolver(self, widget):
        Devolver(self.controle)
        self.close_notification(widget)
        
    def logoff(self,widget):
        self.controle.main_status = False
        self.notify_box.hide()
        self.w_loja.destroy()
        self.controle.logoff()
        
    def __init__(self,controle):
        self.w_loja = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w_loja.set_position(gtk.WIN_POS_CENTER)
        self.w_loja.connect("delete_event", lambda w,e: gtk.main_quit())
        self.w_loja.connect("focus_in_event", self.notification)
        self.w_loja.set_title("CEF SHOP - Loja")
        self.w_loja.set_size_request(580,280)
        self.controle = controle
        self.notify_box = notify_area(self.controle, True)

#---Botoes
        button_clientes = gtk.Button("Clientes")
        button_clientes.connect("clicked", self.open_cad_clientes)
    
        button_retirada = gtk.Button("Retirada")
        button_retirada.connect("clicked",self.open_locar)
      
        button_devolucao = gtk.Button("Devolução")
        button_devolucao.connect("clicked",self.open_devolver)
   
        button_venda = gtk.Button("Venda")
        #button_venda.connect("clicked", , None)

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
        vbox_main.pack_start(self.notify_box,False, True, 4)
        
#-------area de notificacao
        #amarelo_pastel = gtk.gdk.color_parse("#e4e3a9")
        #self.event_box = gtk.EventBox()
        #hboxnotify = gtk.HBox(False)
        #self.event_box.add(hboxnotify)
        
        #self.notify = gtk.Label()
        #hboxnotify.pack_start(self.notify, True, True, 2)
        #controle.get_notify_label(self.notify)
        
        #close_button = gtk.Button()
        #close_button.connect("clicked",self.close_notification)
        #close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        #close_button.add(close)
        #close_button.set_relief(gtk.RELIEF_NONE)
        #hboxnotify.pack_start(close_button, False, True, 2)
        
        #self.event_box.modify_bg(gtk.STATE_NORMAL, amarelo_pastel)
        #vbox_main.pack_start(self.event_box,False, True, 4)
        
#-------Mostra tudo
        self.w_loja.show_all()
        self.notify_box.hide()
        self.w_loja.show()

#-----------------------------------------------------
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
#-----------------------------------------------------
class Locar:
    def set_controle(self, controle):
        self.controle = controle
        
    def close(self,w):
        Loja.show_notify = False
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
        
        #cell3 = gtk.CellRendererText()
        #column3 = gtk.TreeViewColumn("Devolver em", cell3, text=2)
        
        self.tree_view.append_column(column1)
        self.tree_view.append_column(column2)
        #self.tree_view.append_column(column3)
        #self.tree_view.connect("row_activated",  self.remover_item_selecionado)

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
class Devolver:
    def set_controle(self, controle):
        self.controle = controle
    
    def close_notification(self, widget):
        self.hboxnotify.hide()
        
    def close(self,w):
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

    def popular_lista_dvds(self, w):
        #Fixme
        cod = self.entry_cod_dvd.get_text()
        try:
            dvds = self.controle.listar_dvds_locados(cod, self.quant_itens, self.lista)
        except:
            pass
        status = self.controle.notify()
        if status == True:
            cod_cliente = self.controle.cliente_devolucao()
            cliente = self.controle.listar_cliente(cod_cliente)
            self.entry_cod_cliente.set_text(str(cod_cliente))
            self.entry_nome_cliente.set_text(cliente[0][1])
            
            for dvd in dvds:
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
        
        #cell3 = gtk.CellRendererText()
        #column3 = gtk.TreeViewColumn("Devolver em", cell3, text=2)
        
        self.tree_view.append_column(column1)
        self.tree_view.append_column(column2)
        #self.tree_view.append_column(column3)
        #self.tree_view.connect("row_activated",  self.remover_item_selecionado)
        return scrolled_window
        
    def cadastra (self, widget, entry_dvd):
        cod_dvd = entry_dvd.get_text()
        try:
            self.controle.devolucao(cod_dvd)
        except:
            pass
        status = self.controle.notify()
        
        #if status == True:
        self.notify_box.show()
        #else:
            #self.w_devolver.hide()
            #self.controle.main_status = True

    def __init__(self,controle):
        self.w_devolver = gtk.Dialog()
        self.w_devolver.set_position(gtk.WIN_POS_CENTER)
        self.w_devolver.connect("destroy", self.close)
        self.w_devolver.set_title("CEF SHOP - Devolver")
        self.w_devolver.set_size_request(650,400)
        self.w_devolver.set_border_width(8)
        self.controle = controle
        self.notify_box = notify_area(self.controle)
        self.quant_itens = 0

#-------Elementos       
        label_dvd = gtk.Label("Codigo do DvD :")
        entry_dvd = gtk.Entry(0)

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
#-----------------------------------------------------
