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


# Definir el nodo del árbol de análisis sintáctico abstracto (ASA)
class Nodo:
    def __init__(self, tipo, valor=None, nodos=None, atributos=None):
        self.tipo = tipo  # es un enum TipoNodo
        self.valor = valor  # es un string opcional (para los nodos hoja)
        self.nodos = nodos or []  # es una lista
        self.atributos = atributos or {}  # diccionario para línea, columna


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
