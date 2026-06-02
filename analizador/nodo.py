from enum import Enum

##################################################################################
#### Clases para darle estructura a los nodos del árbol de análisis sintáctico ###
##################################################################################


# Definir el nodo raíz del árbol de análisis sintáctico abstracto (ASA)
class Asa:
    def __init__(self):
        self.raiz = None

    def mostrar_asa(self, nodo, nivel=0):

        if nodo is None:
            return

        indent = "  " * nivel

        print(f"{indent}< {nodo.tipo.value}, {nodo.valor}, {nodo.atributos} > \n")

        if hasattr(nodo, "nodos") and nodo.nodos:
            for hijo in nodo.nodos:
                self.mostrar_asa(hijo, nivel + 1)

    def walk(self, visitor):
        """Recorre el ASA llamando al visitante sobre la raíz."""
        if self.raiz is None:
            return None
        if hasattr(self.raiz, "accept"):
            return self.raiz.accept(visitor)
        # fallback: intentar que el visitor visite manualmente
        visit = getattr(visitor, "visit", None)
        if callable(visit):
            return visit(self.raiz)


# Definir el nodo del árbol de análisis sintáctico abstracto (ASA)
class Nodo:
    def __init__(self, tipo, valor=None, nodos=None, atributos=None):
        self.tipo = tipo  # es un enum TipoNodo
        self.valor = valor  # es un string opcional (para los nodos hoja)
        self.nodos = nodos or []  # es una lista
        self.atributos = atributos or {}  # diccionario para línea, columna

    def visitar(self, visitador):
        """Acepta un visitante: llama a `visitar_<TIPONODO>` si existe,
        si no, llama a `generic_visit` si está disponible, o recorre hijos.
        """
        method_name = f"visitar_{self.tipo.name}"
        method = getattr(visitador, method_name, None)
        if callable(method):
            return method(self)

        generic = getattr(visitador, "generic_visit", None)
        if callable(generic):
            return generic(self)

        # Por defecto, recorrer hijos
        for child in self.nodos:
            if hasattr(child, "visitar"):
                child.visitar(visitador)


# Definir los tipos de nodos que produce el analizador (son las reglas de la gramática)


class TipoNodo(Enum):
    TERMINO = "TERMINO"
    CADENA = "CADENA"
    NUMERO = "NUMERO"
    BOOL = "BOOL"
    TIPO = "TIPO"
    FRASE = "FRASE"
    COMPARATIVO = "COMPARATIVO"
    COMPUERTA_LOGICA = "COMPUERTA_LOGICA"
    SIMBOLO = "SIMBOLO"

    COMPARACION = "COMPARACION"
    COMPARACIONES = "COMPARACIONES"
    BUCLES = "BUCLES"
    CONDICIONALES = "CONDICIONALES"
    ASIGNACION = "ASIGNACION"
    VALOR = "VALOR"
    LISTA = "LISTA"
    INDICE = "INDICE"
    ACCESOLISTA = "ACCESOLISTA"
    ASIGNACIONELEMENTOLISTA = "ASIGNACIONELEMENTOLISTA"

    PROGRAMA = "PROGRAMA"
    DECLARACIONFUNCION = "DECLARACIONFUNCION"
    INCLUDE = "INCLUDE"
    BLOQUE = "BLOQUE"
    LLAMADAFUNCION = "LLAMADAFUNCION"
    DECLARACIONVARIABLES = "DECLARACIONVARIABLES"
    FUNCIONESPREDETERMINADAS = "FUNCIONESPREDETERMINADAS"
    EXPRESIONESMATEMATICAS = "EXPRESIONESMATEMATICAS"
