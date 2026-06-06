from analizador.nodo import Asa
from generador.visitadores import VisitantePython

class Generador:

    asa: Asa
    visitador: VisitantePython

    ambiente_estandar = """
# ==========================================
# Ambiente estándar de Zymbolos
# ==========================================

def imprimir(*valores):
    print(*valores)

def leer():
    return input()

def leer_numero():
    return float(input())

def leer_entero():
    return int(input())

"""

    def __init__(self, asa):
        self.asa = asa
        self.visitador = VisitantePython()

    def imprimir_asa(self):
        '''
        Imprimer el árbol de análisis sintáctico abstracto (ASA)
        '''
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.mostrar_asa(self.asa.raiz)

    def generar(self):
        '''
        Generar código Python a partir del ASA
        '''
        codigo_generado = self.visitador.visitar(self.asa.raiz)

        return self.ambiente_estandar + "\n\n" + codigo_generado
