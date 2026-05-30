import enum
from .nodo import Nodo, TipoNodo


class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]

    def abrir_bloque(self):
        self.ambitos.append({})

    def cerrar_bloque(self):
        self.ambitos.pop()

    def nuevo_registro(self, nombre, tipo):
        self.ambitos[-1][nombre] = tipo

    def obtener(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None


class Visitador:
    """Clase base para visitantes del ASA.

    Implementa `visit(node)` que despacha a `visit_<TIPONODO>(node)` si existe,
    y un `generic_visit` que recorre los nodos hijos.
    """

    def __init__(self):
        self.tabla_simbolos = TablaSimbolos()
        self.errores = []

    def visitar(self, node):
        method = getattr(self, f"visitar_{node.tipo.name}", None)
        if callable(method):
            return method(node)
        return self.generic_visit(node)

    def generic_visit(self, node):
        for child in getattr(node, "nodos", []) or []:
            if hasattr(child, "accept"):
                child.visitar(self)

    def visitar_CADENA(self, node):
        return "CCC"

    def visitar_BOOL(self, node):
        return "BBB"

    def visitar_NUMERO(self, node):
        return "NNN"

    def visitar_TIPO(self, node):
        return node.tipo

    def visitar_COMPARATIVO(self, node):
        return node.valor

    def visitar_FRASE(self, node):
        nombre = node.valor
        tipo = self.tabla_simbolos.obtener(nombre)
        if tipo is None:
            self.errores.append(
                f"Variable '{nombre}' no declarada en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None
        return tipo

    def visitar_TERMINO(self, node):
        if node.nodos:
            return node.nodos[0].visitar(self)
        else:
            self.errores.append(
                f"Término vacío en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

    def visitar_COMPUERTA_LOGICA(self, node):
        return node.valor

    def visitar_SIMBOLO(self, node):
        return node.valor

    def visitar_ASIGNACIONELEMENTOLISTA(self, node):
        tipo_lista = node.nodos[0].visitar(self)
        tipo_valor = node.nodos[1].visitar(self)

        if tipo_lista != "OOO":
            self.errores.append(
                f"Error de tipos: se esperaba acceso a elemento de lista pero se obtuvo {tipo_lista} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        if tipo_valor is None:
            return None

        return "LLL"

    def visitar_ACCESOLISTA(self, node):
        tipo_lista = node.nodos[0].visitar(self)
        tipo_indice = node.nodos[1].visitar(self)

        if tipo_lista != "LLL":
            self.errores.append(
                f"Error de tipos: se esperaba una lista pero se obtuvo {tipo_lista} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        if tipo_indice != "NNN":
            self.errores.append(
                f"Error de tipos: el índice de acceso a lista debe ser numérico, pero se obtuvo {tipo_indice} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        return "OOO"  # como nuestras listas no son tipadas, es un valor genérico de término para este caso

    def visitar_INDICE(self, node):
        tipo_indice = node.nodos[0].visitar(self)

        if tipo_indice != "NNN":
            self.errores.append(
                f"Error de tipos: el índice debe ser numérico, pero se obtuvo {tipo_indice} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        return "NNN"

    def visitar_LISTA(self, node):
        for termino in node.nodos:
            tipo_termino = termino.visitar(self)
            if tipo_termino is None:
                self.errores.append(
                    f"Elemento inválido en lista en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                )
        return "LLL"

    def visitar_VALOR(self, node):
        if node.nodos:
            return node.nodos[0].visitar(self)
        else:
            self.errores.append(
                f"Valor vacío en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

    def visitar_ASIGNACION(self, node):

        nombre = node.nodos[0].valor
        tipo_valor = node.nodos[1].visitar(self)

        tipo_existente = self.tabla_simbolos.obtener(nombre)

        if tipo_existente is None:
            # si no existe aún, se crea
            self.tabla_simbolos.nuevo_registro(nombre, tipo_valor)
        else:
            # si ya existe, verificamos que el tipo coincida
            if tipo_existente != tipo_valor:
                self.errores.append(
                    f"Error de tipos en asignación: variable '{nombre}' es de tipo {tipo_existente} pero se intenta asignar {tipo_valor} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                )
        return tipo_valor

    def visitar_CONDICIONALES(self, node):
        nodos = node.nodos
        i = 0
        while i < len(nodos):

            if nodos[i].tipo.name == "COMPARACIONES":
                tipo_comparacion = nodos[i].visitar(self)
                if tipo_comparacion != "BBB":
                    self.errores.append(
                        f"Error de tipos en condicional: se esperaba una comparación booleana pero se obtuvo {tipo_comparacion} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                    )
                i += 1

                if i < len(nodos) and nodos[i].tipo.name == "BLOQUE":
                    nodos[i].visitar(self)
                    i += 1
            elif nodos[i].tipo.name == "BLOQUE":
                # else
                nodos[i].visitar(self)
                i += 1
            else:
                i += 1
        return None

    def visitar_BUCLES(self, node):
        if len(node.nodos) >= 1:
            tipo_comparacion = node.nodos[0].visitar(self)
            if tipo_comparacion != "BBB":
                self.errores.append(
                    f"Error de tipos en bucle: se esperaba una comparación booleana pero se obtuvo {tipo_comparacion} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                )
        if len(node.nodos) >= 2:
            node.nodos[1].visitar(self)
        return None
