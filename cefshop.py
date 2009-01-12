#!/usr/bin/env python

if __name__ == "__main__":
    
    from querys import Modelo
    from controle import Controle    
    from main_base import Login
    
    modelo = Modelo()
    controle = Controle()    
    interface = Login()
    
    controle.set_modelo(modelo)
    controle.set_interface(interface)
    interface.set_controle(controle)
    
    controle.start()