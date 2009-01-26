# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

def on_expose_event(self, widget, allocation,window, event_box, style ):
        #w, h = window.size_request()
        x = allocation.x
        y = allocation.y
        width = allocation.width
        height = allocation.height

        #style.paint_flat_box(widget.window, gtk.STATE_NORMAL,
           #                         gtk.SHADOW_OUT, None, None,
              #                      'tooltip', x, y, width,height)
                                    
        event_box.set_style(style)

def notify_area(controle, main_notify = False, icon = 'erro'):    
    apply = gtk.image_new_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
    erro = gtk.image_new_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
    info = gtk.image_new_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_MENU)
    warning = gtk.image_new_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)
    
    event_box = gtk.EventBox()
    hboxnotify = gtk.HBox(False)
    event_box.add(hboxnotify)
    b_icon = gtk.HButtonBox ()
    b_icon.set_layout(gtk.BUTTONBOX_END)

    if icon == 'erro':
        b_icon.add(erro)
        hboxnotify.pack_start(b_icon, False, True, 0)
    elif icon == 'apply':
        b_icon.add(apply)
        hboxnotify.pack_start(b_icon, False, True, 0)
    elif icon == 'info':
        b_icon.add(info)
        hboxnotify.pack_start(b_icon, False, True, 0)
    elif icon == 'warning':
        b_icon.add(warning)
        hboxnotify.pack_start(b_icon, False, True, 0)
        
    notify = gtk.Label()
    hboxnotify.pack_start(notify,True, True, 2)
    
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
   
    
    allocation = event_box.get_allocation()
    window = gtk.Window(gtk.WINDOW_POPUP)
    window.set_name("gtk-tooltip")
    window.ensure_style()
    style = window.get_style() 
    event_box.connect("expose-event", on_expose_event, allocation, window, event_box, style)
    
    
    #style = window.get_style() 
    
    
    
    #style.paint_flat_box(window.window, gtk.STATE_NORMAL,
       #                             gtk.SHADOW_OUT, None, event_box,
          #                          'tooltip', x, y, width,height)

    #__changing_style = True
    #event_box.set_style(style)
    #changing_style = False
    window.destroy()
    event_box.queue_draw() 
    
    return event_box
    
    
   
