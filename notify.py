# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

class Notify(gtk.HBox):
    def __init__(self):    
        super(Notify, self).__init__()
        
        self.icons = []
        self.__contents = None
        self.__changing_style = False
        
        self.__main_hbox = gtk.HBox(False, 8) 
        self.__main_hbox.set_border_width(4)

        self.__icon_area = gtk.HBox(True, 2)
        self.__main_hbox.pack_start (self.__icon_area, False, True, 2)

        self.__msg_area = gtk.HBox(True, 2)
        self.__main_hbox.pack_start (self.__msg_area, False, True, 0)

        self.__action_area = gtk.HBox(True, 2)
        self.__main_hbox.pack_end (self.__action_area, False, True, 0)

        self.pack_start(self.__main_hbox, True, True, 0)

        self.set_app_paintable(True)

        self.connect("expose-event", self.__paint)
        
        self.__main_hbox.connect("style-set", self.__on_style_set)
        
    def add_icon(self, icon):
        """Adiciona um icone ao notify"""
        self.remove_icon()
        
        if icon == 'erro':
            self.erro = gtk.image_new_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
            self.icons.append(self.erro)
            self.__icon_area.pack_start (self.erro, False, True, 2)
        elif icon == 'apply':
            self.apply = gtk.image_new_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
            self.icons.append(self.apply)
            self.__icon_area.pack_start (self.apply, False, True, 2)
        elif icon == 'info':
            self.info = gtk.image_new_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_MENU)
            self.icons.append(self.info)
            self.__icon_area.pack_start (self.info, False, True, 2)
        elif icon == 'warning':
            self.warning = gtk.image_new_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)
            self.icons.append(self.warning)
            self.__icon_area.pack_start (self.warning, False, True, 2)
            
    def remove_icon(self):
        for icon in self.icons:
            self.__icon_area.remove (icon)
        self.icons = []
        
    def add_msg(self):
        """Adiciona um label ao notify"""
        self.msg = gtk.Label()
        self.__msg_area.pack_start (self.msg, False, True, 0)
        return self.msg
            
    def add_button(self):
        """Adiciona botão de fechar ao notify"""
        close_button = gtk.Button()
        close = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.add(close)
        close_button.set_relief(gtk.RELIEF_NONE)
        self.__action_area.pack_start (close_button, False, True, 0)
        return close_button
        
    def __paint(self, w, event):
        """Aplica um style no objeto para que ele tenha borda com a cor do tooltip"""
        gtk.Style.paint_flat_box(w.style,
                                 w.window,
                                 gtk.STATE_NORMAL,
                                 gtk.SHADOW_OUT,
                                 None,
                                 w,
                                 "tooltip",
                                 w.allocation.x + 1,
                                 w.allocation.y + 1,
                                 w.allocation.width - 2,
                                 w.allocation.height - 2)
        return False

    def __on_style_set(self, w, style):
        """Implementa um hack necessario para usar as cores de fundo do tooltip"""
        if self.__changing_style:
            return
        window = gtk.Window(gtk.WINDOW_POPUP);
        window.set_name("gtk-tooltip")
        window.ensure_style()
        style = window.get_style()

        self.__changing_style = True
        self.set_style(style)
        self.__changing_style = False

        window.destroy()
        self.queue_draw()
