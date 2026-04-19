import unittest
from explorador.Explorador import Token
from analizador.nodo import TipoNodo
from analizador.analizador import Analizador
from analizador.tipo_token import TipoToken

############################################################################################
### Pruebas unitarias para los componentes internos del asa (aquellos que agrupan hojas) ###
############################################################################################

"""!!!!! PD: chat me dijo q podría ser buena idea separar las pruebas asi:
tests/
├── test_hojas.py        → NUMERO, BOOL, TIPO, FRASE, SIMBOLO, COMPARATIVO, COMPUERTA_LOGICA,CADENA
└── test_internos.py     → TERMINO, EXPRESIONES_MATEMATICAS, COMPARACION, COMPARACIONES, VALOR
└── test_estructuras.py  → BLOQUE, CONDICIONALES, BUCLES, DECLARACION_VARIABLES, ASIGNACION
└── test_programa.py     → MAIN, DECLARACION_FUNCION, PROGRAMA
"""


class PruebasInternos(unittest.TestCase):

    def crear_analizador(self, tokens):
        lista = tokens[1:]
        return Analizador(lista, tokens[0])

    def acceder(self, analizador, metodo):
        return getattr(analizador, f"_Analizador__{metodo}")

    # ─────────────────────────────────────────────
    def test_termino_numero(self):
        a = self.crear_analizador([Token(TipoToken.NUMERO, "42", 1, 1)])
        nodo = self.acceder(a, "analizar_termino")()
        self.assertEqual(nodo.tipo, TipoNodo.TERMINO)
        self.assertEqual(nodo.nodos_hijos[0].tipo, TipoNodo.NUMERO)
        self.assertEqual(nodo.nodos_hijos[0].contenido, "42")

    def test_termino_frase(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "miVar", 1, 1)])
        nodo = self.acceder(a, "analizar_termino")()
        self.assertEqual(nodo.tipo, TipoNodo.TERMINO)
        self.assertEqual(nodo.nodos_hijos[0].tipo, TipoNodo.FRASE)
        self.assertEqual(nodo.nodos_hijos[0].contenido, "miVar")

    def test_termino_cadena(self):
        a = self.crear_analizador([Token(TipoToken.STRING, '"hola"', 1, 1)])
        nodo = self.acceder(a, "analizar_termino")()
        self.assertEqual(nodo.tipo, TipoNodo.TERMINO)
        self.assertEqual(nodo.nodos_hijos[0].tipo, TipoNodo.CADENA)

    def test_termino_invalido(self):
        a = self.crear_analizador([Token(TipoToken.BOOL, "VV", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_termino")()


if __name__ == "__main__":
    unittest.main()
