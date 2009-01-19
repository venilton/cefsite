import unittest

import controle
from controle import Controle


class TestesCadastroClientes(unittest.TestCase):
    """    Testes Cadastro de Clientes    """
    metodo = Controle()
    
    def testCamposEmBranco(self):
        """Cadastro de Clientes Campo nome nao deve ficar em branco"""
        self.assertRaises(controle.EmBranco, self.metodo.cadastra_cliente, "", "", "", "", "", "", "", "", "", "")
        
class TestesLocacao(unittest.TestCase):
    """    Testes Locacao    """
    metodo = Controle()
    
    def testCodDVDEmBranco(self):
        """Locacao Campo Codigo DVD nao deve ficar em branco"""
        self.assertRaises(controle.EmBranco, self.metodo.alugar, "1", "", True)
    
    def testCodClienteEmBranco(self):
        """Locacao Campo Codigo Cliente nao deve ficar em branco"""
        self.assertRaises(controle.EmBranco, self.metodo.alugar, "","1", True)
    
    def testLetrasNoCodigoDVD(self):
        """Locacao Campo Codigo DVD nao deve conter letras"""
        self.assertRaises(controle.CodigoInvalido, self.metodo.alugar, "1","a", True)
    
    def testLetrasNoCodigoCliente(self):
        """Locacao Campo Codigo Cliente nao deve conter letras"""
        self.assertRaises(controle.CodigoInvalido, self.metodo.alugar, "a","1", True)
        
class TestesDevolucao(unittest.TestCase):
    """    Testes Devolucao    """
    metodo = Controle()
    
    def testCamposEmBranco(self):
        """Devolucao Campo nome nao deve ficar em branco"""
        self.assertRaises(controle.EmBranco, self.metodo.devolucao, "")

    def testLetrasNoCodigo(self):
        """Devolucao Campo Codigo nao deve conter letras"""
        self.assertRaises(controle.CodigoInvalido, self.metodo.devolucao, "a")
        



#-------Selecionar suites------------------------------------------
suite1 = unittest.TestLoader().loadTestsFromTestCase(TestesCadastroClientes)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestesLocacao)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestesDevolucao)
#alltests = unittest.TestSuite([suite1])
#alltests = unittest.TestSuite([suite1, suite2])
alltests = unittest.TestSuite([suite1, suite2, suite3])

unittest.TextTestRunner(verbosity=2).run(alltests)

#---------rodar todas--------
#if __name__ == "__main__":
#   unittest.main()
