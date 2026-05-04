import unittest
from explorador.Explorador import Token
from analizador.nodo import TipoNodo
from analizador.analizador import Analizador
from analizador.tipo_token import TipoToken

###################################################################################
### Pruebas unitarias para las hojas del asa (aquellos que son tokens directos) ###
###################################################################################


class PruebasHojas(unittest.TestCase):

    def crear_analizador(self, tokens):
        lista = tokens[1:]
        return Analizador(lista, tokens[0])

    def acceder(self, analizador, metodo):
        return getattr(analizador, f"_Analizador__{metodo}")

    # ─────────────────────────────────────────────
    def test_numero_valido(self):
        a = self.crear_analizador([Token(TipoToken.NUMERO, "42", 1, 1)])
        nodo = self.acceder(a, "analizar_numero")()
        self.assertEqual(nodo.tipo, TipoNodo.NUMERO)
        self.assertEqual(nodo.contenido, "42")

    def test_numero_invalido(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "hola", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_numero")()

    # ─────────────────────────────────────────────
    def test_bool_vv(self):
        a = self.crear_analizador([Token(TipoToken.BOOL, "VV", 1, 1)])
        nodo = self.acceder(a, "analizar_bool")()
        self.assertEqual(nodo.tipo, TipoNodo.BOOL)
        self.assertEqual(nodo.contenido, "VV")

    def test_bool_ff(self):
        a = self.crear_analizador([Token(TipoToken.BOOL, "FF", 1, 1)])
        nodo = self.acceder(a, "analizar_bool")()
        self.assertEqual(nodo.tipo, TipoNodo.BOOL)
        self.assertEqual(nodo.contenido, "FF")

    def test_bool_invalido(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "verdadero", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_bool")()

    # ─────────────────────────────────────────────
    def test_tipo_nnn(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "NNN", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "NNN")

    def test_tipo_ccc(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "CCC", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "CCC")

    def test_tipo_bbb(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "BBB", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "BBB")

    def test_tipo_ooo(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "OOO", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "OOO")

    def test_tipo_eee(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "EEE", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "EEE")

    def test_tipo_lll(self):
        a = self.crear_analizador([Token(TipoToken.TIPO, "LLL", 1, 1)])
        nodo = self.acceder(a, "analizar_tipo")()
        self.assertEqual(nodo.tipo, TipoNodo.TIPO)
        self.assertEqual(nodo.contenido, "LLL")

    def test_tipo_invalido(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "int", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_tipo")()

    # ─────────────────────────────────────────────
    def test_simbolo_suma(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "+", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "+")

    def test_simbolo_resta(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "-", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "-")

    def test_simbolo_division(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "/", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "/")

    def test_simbolo_modulo(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "%", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "%")

    def test_simbolo_multiplicacion(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "*", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "*")

    def test_simbolo_potencia(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "^", 1, 1)])
        nodo = self.acceder(a, "analizar_simbolo")()
        self.assertEqual(nodo.tipo, TipoNodo.SIMBOLO)
        self.assertEqual(nodo.contenido, "^")

    def test_simbolo_invalido(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "x", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_simbolo")()

    # ─────────────────────────────────────────────
    def test_comparativo_igual(self):
        a = self.crear_analizador([Token(TipoToken.REL_OP, "==", 1, 1)])
        nodo = self.acceder(a, "analizar_comparativo")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPARATIVO)
        self.assertEqual(nodo.contenido, "==")

    def test_comparativo_menor(self):
        a = self.crear_analizador([Token(TipoToken.REL_OP, "<", 1, 1)])
        nodo = self.acceder(a, "analizar_comparativo")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPARATIVO)
        self.assertEqual(nodo.contenido, "<")

    def test_comparativo_mayor(self):
        a = self.crear_analizador([Token(TipoToken.REL_OP, ">", 1, 1)])
        nodo = self.acceder(a, "analizar_comparativo")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPARATIVO)
        self.assertEqual(nodo.contenido, ">")

    def test_comparativo_menor_igual(self):
        a = self.crear_analizador([Token(TipoToken.REL_OP, "<=", 1, 1)])
        nodo = self.acceder(a, "analizar_comparativo")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPARATIVO)
        self.assertEqual(nodo.contenido, "<=")

    def test_comparativo_mayor_igual(self):
        a = self.crear_analizador([Token(TipoToken.REL_OP, ">=", 1, 1)])
        nodo = self.acceder(a, "analizar_comparativo")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPARATIVO)
        self.assertEqual(nodo.contenido, ">=")

    def test_comparativo_invalido(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "+", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_comparativo")()

    # ─────────────────────────────────────────────
    def test_compuerta_and(self):
        a = self.crear_analizador([Token(TipoToken.LOGIC_OP, "&&", 1, 1)])
        nodo = self.acceder(a, "analizar_compuerta_logica")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPUERTA_LOGICA)
        self.assertEqual(nodo.contenido, "&&")

    def test_compuerta_or(self):
        a = self.crear_analizador([Token(TipoToken.LOGIC_OP, "||", 1, 1)])
        nodo = self.acceder(a, "analizar_compuerta_logica")()
        self.assertEqual(nodo.tipo, TipoNodo.COMPUERTA_LOGICA)
        self.assertEqual(nodo.contenido, "||")

    def test_compuerta_invalida(self):
        a = self.crear_analizador([Token(TipoToken.ARITH_OP, "+", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_compuerta_logica")()

    # ─────────────────────────────────────────────
    def test_frase_valida(self):
        a = self.crear_analizador([Token(TipoToken.IDENTIFICADOR, "miVariable", 1, 1)])
        nodo = self.acceder(a, "analizar_frase")()
        self.assertEqual(nodo.tipo, TipoNodo.FRASE)
        self.assertEqual(nodo.contenido, "miVariable")

    def test_frase_invalida(self):
        a = self.crear_analizador([Token(TipoToken.NUMERO, "123", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_frase")()

    # ─────────────────────────────────────────────
    def test_cadena_string(self):
        a = self.crear_analizador([Token(TipoToken.STRING, '"hola mundo"', 1, 1)])
        nodo = self.acceder(a, "analizar_cadena")()
        self.assertEqual(nodo.tipo, TipoNodo.CADENA)
        self.assertEqual(nodo.contenido, '"hola mundo"')

    def test_cadena_invalida(self):
        a = self.crear_analizador([Token(TipoToken.BOOL, "VV", 1, 1)])
        with self.assertRaises(Exception):
            self.acceder(a, "analizar_cadena")()


if __name__ == "__main__":
    unittest.main()
