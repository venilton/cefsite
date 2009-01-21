# coding: utf-8

import pygtk
pygtk.require('2.0')
import gtk

def iconMenuItem(title, stock):
    mItem = gtk.ImageMenuItem(title)
    im = gtk.Image()
    try:
        im.set_from_stock(stock, gtk.ICON_SIZE_MENU)
        mItem.set_image(im)
    except AttributeError:
        pass
    return mItem
