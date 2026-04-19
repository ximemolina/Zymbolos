from .tipo_token import TipoToken  # enum con tipos de nodos
from .nodo import Nodo, Asa, TipoNodo

#########################################################################
### Clase que se encarga de construir el árbol de análisis sintáctico ###
#########################################################################


class Analizador:

    def __init__(self, lista_componentes, token_actual):
        self.lista_componentes = lista_componentes
        self.token_actual = token_actual
        self.asa = Asa()

    def analizar(self):
        self.asa.raiz = self.__analizar_programa()

    def __analizar_programa(self):
        """#!!!!!!!!!creo q esto sirve (se podrá probar hasta terminar todos los módulos)!!!!!!!"""
        return

    def __avanzar(self):
        """#!!!!!!!!!creo q esto sirve (se podrá probar hasta terminar todos los módulos)!!!!!!!"""
        if self.lista_componentes:
            self.token_actual = self.lista_componentes.pop(0)
        else:
            self.token_actual = None

    def __analizar_termino(self):
        nodos_nuevos = []

        if self.token_actual.tipo == TipoToken.NUMERO:
            nodos_nuevos += [self.__analizar_numero()]
        elif self.token_actual.tipo == TipoToken.STRING:
            nodos_nuevos += [self.__analizar_cadena()]
        elif self.token_actual.tipo == TipoToken.IDENTIFICADOR:
            nodos_nuevos += [self.__analizar_frase()]
        else:
            raise Exception(
                f"ERROR: se esperaba una cadena, número o frase en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

        return Nodo(TipoNodo.TERMINO, nodos=nodos_nuevos)

    def __analizar_compuerta_logica(self):
        if self.token_actual.tipo == TipoToken.LOGIC_OP:
            nodo = Nodo(TipoNodo.COMPUERTA_LOGICA, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba una compuerta lógica: && , ||, en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_simbolo(self):
        if self.token_actual.tipo == TipoToken.ARITH_OP:
            nodo = Nodo(TipoNodo.SIMBOLO, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba un símbolo aritmético: +, -, /, %, &, *, ^, en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_cadena(self):
        if self.token_actual.tipo == TipoToken.STRING:
            nodo = Nodo(TipoNodo.CADENA, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba una cadena en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_frase(self):
        if self.token_actual.tipo == TipoToken.IDENTIFICADOR:
            nodo = Nodo(TipoNodo.FRASE, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba una frase en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_bool(self):
        if self.token_actual.tipo == TipoToken.BOOL:
            nodo = Nodo(TipoNodo.BOOL, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba un booleano en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_numero(self):
        if self.token_actual.tipo == TipoToken.NUMERO:
            nodo = Nodo(TipoNodo.NUMERO, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba un número en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_comparativo(self):
        if self.token_actual.tipo == TipoToken.REL_OP:
            nodo = Nodo(TipoNodo.COMPARATIVO, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba un operador de comparación: ==, !=, <, >, <=, >=, en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )

    def __analizar_tipo(self):
        if self.token_actual.tipo == TipoToken.TIPO:
            nodo = Nodo(TipoNodo.TIPO, valor=self.token_actual.valor)
            self.__avanzar()
            return nodo
        else:
            raise Exception(
                f"ERROR: se esperaba un tipo de dato: NNN, CCC, BBB, OOO, EEE, LLL, en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            )
