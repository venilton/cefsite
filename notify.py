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
