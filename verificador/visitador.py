import enum
from analizador.nodo import Nodo, TipoNodo
from colorama import init, Fore, Style

init(autoreset=True)


class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]

    def abrir_bloque(self):
        self.ambitos.append({})

    def cerrar_bloque(self):
        self.ambitos.pop()

    def nuevo_registro(self, nombre, tipo, def_node=None):

        if nombre in self.ambitos[-1]:
            return False  # señal de redeclaración
        # almacenamos un registro con tipo y referencia al nodo de definición
        self.ambitos[-1][nombre] = {"tipo": tipo, "def_node": def_node}
        return True

    def actualizar(self, nombre, tipo):
        """Actualiza el tipo de una variable ya existente en cualquier ámbito."""
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                # ambito almacena un registro dict
                if isinstance(ambito[nombre], dict):
                    ambito[nombre]["tipo"] = tipo
                else:
                    ambito[nombre] = {"tipo": tipo, "def_node": None}
                return True
        return False

    def obtener(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                registro = ambito[nombre]
                # devolver tipo para compatibilidad con código existente
                if isinstance(registro, dict):
                    return registro.get("tipo")
                return registro
        return None

    def obtener_registro(self, nombre):
        """Devuelve el registro completo (dict) o None si no existe."""
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                registro = ambito[nombre]
                if isinstance(registro, dict):
                    return registro
                return {"tipo": registro, "def_node": None}
        return None


class Visitador:
    """Clase base para visitantes del ASA.

    Implementa `visit(node)` que despacha a `visit_<TIPONODO>(node)` si existe,
    y un `generic_visit` que recorre los nodos hijos.
    """

    def __init__(self):
        self.tabla_simbolos = TablaSimbolos()
        self.errores = []
        self.funciones = {}
        self.funcion_actual = None

        self._funcion_tiene_retorno = False

    def imprimir_tabla_parcial(self, accion, nombre=None):
        """Imprime la tabla de símbolos cada vez que cambia.
        accion: descripción breve del cambio (abrir, cerrar, declarar, asignar, param)
        nombre: nombre de la variable afectada (opcional)
        """
        print(f"\n[Tabla de símbolos] acción: {accion}{' - '+nombre if nombre else ''}")
        for i, ambito in enumerate(self.tabla_simbolos.ambitos):
            print(f" Ámbito {i}:")
            for var, registro in ambito.items():
                if isinstance(registro, dict):
                    tipo = registro.get("tipo")
                    def_node = registro.get("def_node")
                    if def_node and def_node.atributos:
                        loc = f"(línea {def_node.atributos.get('linea')}, col {def_node.atributos.get('columna')})"
                    else:
                        loc = ""
                    print(f"    {var} : {tipo} {loc}")
                else:
                    print(f"    {var} : {registro}")
        print("")

    def visitar(self, node):
        method = getattr(self, f"visitar_{node.tipo.name}", None)
        if callable(method):
            return method(node)
        return self.generic_visit(node)

    def generic_visit(self, node):
        for child in getattr(node, "nodos", []) or []:
            if hasattr(child, "visitar"):
                child.visitar(self)

    # ------------------------------------------------------------------ #
    #  Terminales                                                          #
    # ------------------------------------------------------------------ #

    def visitar_CADENA(self, node):
        return "CCC"

    def visitar_BOOL(self, node):
        return "BBB"

    def visitar_NUMERO(self, node):
        return "NNN"

    def visitar_TIPO(self, node):
        return node.valor

    def visitar_COMPARATIVO(self, node):
        return node.valor

    def visitar_COMPUERTA_LOGICA(self, node):
        return node.valor

    def visitar_SIMBOLO(self, node):
        return node.valor

    def visitar_COMENTARIOS(self, node):
        return None

    # ------------------------------------------------------------------ #
    #  Identificadores y términos                                          #
    # ------------------------------------------------------------------ #

    def visitar_FRASE(self, node):
        nombre = node.valor
        tipo = self.tabla_simbolos.obtener(nombre)
        if tipo is None:
            self.errores.append(
                f"Variable '{nombre}' no declarada en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None
        # decorar referencia con info de definición si existe
        registro = self.tabla_simbolos.obtener_registro(nombre)
        if registro and registro.get("def_node"):
            node.atributos["ref"] = {"nombre": nombre, "tipo": registro.get("tipo")}
        return tipo

    def visitar_TERMINO(self, node):
        if node.nodos:
            return node.nodos[0].visitar(self)
        else:
            self.errores.append(
                f"Término vacío en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

    # ------------------------------------------------------------------ #
    #  Listas y acceso                                                     #
    # ------------------------------------------------------------------ #

    def visitar_LISTA(self, node):
        for termino in node.nodos:
            tipo_termino = termino.visitar(self)
            if tipo_termino is None:
                self.errores.append(
                    f"Elemento inválido en lista en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                )
        return "LLL"

    def visitar_INDICE(self, node):
        tipo_indice = node.nodos[0].visitar(self)
        if tipo_indice != "NNN":
            self.errores.append(
                f"Error de tipos: el índice debe ser numérico, pero se obtuvo {tipo_indice} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None
        return "NNN"

    def visitar_ACCESOLISTA(self, node):
        tipo_lista = node.nodos[0].visitar(self)
        tipo_indice = node.nodos[1].visitar(self)
        if tipo_lista not in ("LLL", "CCC"):
            self.errores.append(
                f"Error de tipos: se esperaba una lista o cadena pero se obtuvo {tipo_lista} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None
        if tipo_indice != "NNN":
            self.errores.append(
                f"Error de tipos: el índice de acceso a lista debe ser numérico, pero se obtuvo {tipo_indice} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None
        return "OOO" if tipo_lista == "LLL" else "CCC"

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

    # ------------------------------------------------------------------ #
    #  Expresiones                                                         #
    # ------------------------------------------------------------------ #

    def visitar_VALOR(self, node):
        if node.nodos:
            return node.nodos[0].visitar(self)
        else:
            self.errores.append(
                f"Valor vacío en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

    def visitar_EXPRESIONESMATEMATICAS(self, node):
        if not node.nodos:
            self.errores.append(
                f"Expresión matemática vacía en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        tipo_actual = node.nodos[0].visitar(self)
        i = 1
        while i < len(node.nodos):
            operador = node.nodos[i].visitar(self)
            tipo_derecho = node.nodos[i + 1].visitar(self)
            tipo_actual = self._resolver_tipo_aritmetico(
                tipo_actual, operador, tipo_derecho, node.atributos
            )
            i += 2
        return tipo_actual

    def visitar_COMPARACION(self, node):
        if not node.nodos:
            self.errores.append(
                f"Comparación vacía en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        tipo_actual = node.nodos[0].visitar(self)
        i = 1
        while i < len(node.nodos):
            operador = node.nodos[i].visitar(self)
            tipo_derecho = node.nodos[i + 1].visitar(self)

            if tipo_actual is not None and tipo_derecho is not None:
                if operador in ["<", ">", "<=", ">="]:
                    if tipo_actual != tipo_derecho or tipo_actual not in ["NNN", "CCC"]:
                        self.errores.append(
                            f"Error de tipos en comparación: operador '{operador}' no soporta {tipo_actual} y {tipo_derecho} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                        )
                elif operador in ["==", "!="]:
                    if (
                        tipo_actual != tipo_derecho
                        and tipo_actual != "OOO"
                        and tipo_derecho != "OOO"
                    ):
                        self.errores.append(
                            f"Error de tipos en comparación: no se pueden comparar {tipo_actual} con {tipo_derecho} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                        )
                else:
                    self.errores.append(
                        f"Operador de comparación desconocido '{operador}' en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                    )
            tipo_actual = "BBB"
            i += 2
        return tipo_actual

    def visitar_COMPARACIONES(self, node):
        if not node.nodos:
            self.errores.append(
                f"Comparaciones vacías en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return None

        tipo_actual = node.nodos[0].visitar(self)
        if tipo_actual != "BBB":
            self.errores.append(
                f"Error de tipos en comparación compuesta: se esperaba BBB pero se obtuvo {tipo_actual} en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )

        i = 1
        while i < len(node.nodos):
            node.nodos[i].visitar(self)  # compuerta lógica
            tipo_izq = node.nodos[i + 1].visitar(self)
            if tipo_izq != "BBB":
                self.errores.append(
                    f"Error de tipos en comparación compuesta: se esperaba BBB pero se obtuvo {tipo_izq} en línea {node.nodos[i + 1].atributos.get('linea')} columna {node.nodos[i + 1].atributos.get('columna')}"
                )
            i += 2

        return "BBB"

    # ------------------------------------------------------------------ #
    #  Asignaciones y declaraciones                                        #
    # ------------------------------------------------------------------ #

    def visitar_ASIGNACION(self, node):
        nombre = node.nodos[0].valor
        tipo_valor = node.nodos[1].visitar(self)

        tipo_existente = self.tabla_simbolos.obtener(nombre)

        if tipo_existente is None:
            # Variable nueva: registrar con el tipo inferido
            registrado = self.tabla_simbolos.nuevo_registro(
                nombre, tipo_valor, def_node=None
            )
            if registrado:
                self.imprimir_tabla_parcial("asignacion_nueva", nombre)
        else:
            if (
                tipo_valor is not None
                and tipo_valor != "OOO"
                and tipo_existente != tipo_valor
            ):
                self.errores.append(
                    f"Error de tipos en asignación: variable '{nombre}' es de tipo {tipo_existente} "
                    f"pero se intenta asignar {tipo_valor} en línea {node.atributos.get('linea')} "
                    f"columna {node.atributos.get('columna')}"
                )
        return tipo_valor

    def visitar_DECLARACIONVARIABLES(self, node):
        nombre = node.nodos[0].valor
        tipo_declarado = node.nodos[1].valor
        tipo_asignado = node.nodos[2].visitar(self)

        if (
            tipo_asignado is not None
            and tipo_asignado != "OOO"
            and tipo_declarado != tipo_asignado
        ):
            self.errores.append(
                f"Error de tipos en declaración de variable '{nombre}': se declaró {tipo_declarado} "
                f"pero se asignó {tipo_asignado} en línea {node.atributos.get('linea')} "
                f"columna {node.atributos.get('columna')}"
            )

        registrado = self.tabla_simbolos.nuevo_registro(
            nombre, tipo_declarado, def_node=node
        )
        if not registrado:
            self.errores.append(
                f"Variable '{nombre}' ya fue declarada en este ámbito en línea {node.atributos.get('linea')} "
                f"columna {node.atributos.get('columna')}"
            )
        else:
            # decorar nodo de declaración con referencia a sí mismo
            node.atributos.setdefault("def", {"nombre": nombre, "tipo": tipo_declarado})
            # imprimir cambio en la tabla
            self.imprimir_tabla_parcial("declarar", nombre)
        return tipo_declarado

    # ------------------------------------------------------------------ #
    #  Estructuras de control                                              #
    # ------------------------------------------------------------------ #

    def visitar_BUCLES(self, node):
        if len(node.nodos) >= 1:
            tipo_comparacion = node.nodos[0].visitar(self)
            if tipo_comparacion != "BBB":
                self.errores.append(
                    f"Error de tipos en bucle: se esperaba BBB pero se obtuvo {tipo_comparacion} "
                    f"en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                )
        if len(node.nodos) >= 2:
            node.nodos[1].visitar(self)
        return None

    def visitar_CONDICIONALES(self, node):
        nodos = node.nodos
        i = 0
        while i < len(nodos):
            if nodos[i].tipo.name == "COMPARACIONES":
                tipo_comparacion = nodos[i].visitar(self)
                if tipo_comparacion != "BBB":
                    self.errores.append(
                        f"Error de tipos en condicional: se esperaba BBB pero se obtuvo "
                        f"{tipo_comparacion} en línea {nodos[i].atributos.get('linea')} "
                        f"columna {nodos[i].atributos.get('columna')}"
                    )
                i += 1
                if i < len(nodos) and nodos[i].tipo.name == "BLOQUE":
                    nodos[i].visitar(self)
                    i += 1
            elif nodos[i].tipo.name == "BLOQUE":
                # bloque else sin condición
                nodos[i].visitar(self)
                i += 1
            else:
                i += 1
        return None

    # ------------------------------------------------------------------ #
    #  Funciones predeterminadas (>>, <<, >>>, <<<)                        #
    # ------------------------------------------------------------------ #

    def visitar_FUNCIONESPREDETERMINADAS(self, node):
        operador = node.valor
        tipos_argumentos = [arg.visitar(self) for arg in node.nodos]

        if operador == ">>":
            if len(tipos_argumentos) != 1:
                self.errores.append(
                    f"'{operador}' espera exactamente 1 argumento pero recibió "
                    f"{len(tipos_argumentos)} en línea {node.atributos.get('linea')} "
                    f"columna {node.atributos.get('columna')}"
                )
            else:
                # Verificar tipo de retorno de la función actual
                if self.funcion_actual:
                    firma = self.funciones.get(self.funcion_actual)
                    if firma and firma["return"] is not None:
                        tipo_retorno = tipos_argumentos[0]
                        if (
                            tipo_retorno is not None
                            and tipo_retorno != firma["return"]
                            and tipo_retorno != "OOO"
                        ):
                            self.errores.append(
                                f"Error de tipos en retorno de '{self.funcion_actual}': "
                                f"se esperaba {firma['return']} pero se devuelve {tipo_retorno} "
                                f"en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
                            )
                # Marcar que esta función sí tiene retorno
                self._funcion_tiene_retorno = True

        # << (input): debe recibir exactamente 1 argumento; devuelve el tipo de la variable destino
        elif operador == "<<":
            if len(tipos_argumentos) != 1:
                self.errores.append(
                    f"'{operador}' espera exactamente 1 argumento pero recibió "
                    f"{len(tipos_argumentos)} en línea {node.atributos.get('linea')} "
                    f"columna {node.atributos.get('columna')}"
                )

        # >>> (print con salto / print especial): acepta 1 o más argumentos de cualquier tipo
        elif operador == ">>>":
            if len(tipos_argumentos) < 1:
                self.errores.append(
                    f"'{operador}' espera al menos 1 argumento en línea {node.atributos.get('linea')} "
                    f"columna {node.atributos.get('columna')}"
                )

        # <<< (input especial): debe recibir exactamente 1 argumento
        elif operador == "<<<":
            if len(tipos_argumentos) != 1:
                self.errores.append(
                    f"'{operador}' espera exactamente 1 argumento pero recibió "
                    f"{len(tipos_argumentos)} en línea {node.atributos.get('linea')} "
                    f"columna {node.atributos.get('columna')}"
                )

        return None

    # ------------------------------------------------------------------ #
    #  Llamadas a funciones                                                #
    # ------------------------------------------------------------------ #

    def visitar_LLAMADAFUNCION(self, node):
        nombre = node.nodos[0].valor
        firma = self.funciones.get(nombre)
        if firma is None:
            self.errores.append(
                f"Función '{nombre}' no declarada en línea {node.atributos.get('linea')} "
                f"columna {node.atributos.get('columna')}"
            )
            return None

        return_type, param_types = firma["return"], firma["params"]
        argumentos = node.nodos[1:]

        if len(argumentos) != len(param_types):
            self.errores.append(
                f"Cantidad incorrecta de argumentos para '{nombre}': se esperaban "
                f"{len(param_types)} pero se recibieron {len(argumentos)} en línea "
                f"{node.atributos.get('linea')} columna {node.atributos.get('columna')}"
            )
            return return_type

        for indice, (argumento, tipo_esperado) in enumerate(
            zip(argumentos, param_types), start=1
        ):
            tipo_argumento = argumento.visitar(self)
            if tipo_argumento is None:
                continue
            if tipo_argumento != tipo_esperado and tipo_argumento != "OOO":
                self.errores.append(
                    f"Error de tipos en llamada a '{nombre}': argumento {indice} es de tipo "
                    f"{tipo_argumento} pero se esperaba {tipo_esperado} en línea "
                    f"{argumento.atributos.get('linea')} columna {argumento.atributos.get('columna')}"
                )
        return return_type

    # ------------------------------------------------------------------ #
    #  Bloque, programa y declaración de funciones                        #
    # ------------------------------------------------------------------ #

    def visitar_BLOQUE(self, node):
        self.tabla_simbolos.abrir_bloque()
        # imprimir estado tras abrir ámbito
        self.imprimir_tabla_parcial("abrir_ambito")
        for child in node.nodos:
            child.visitar(self)
        self.tabla_simbolos.cerrar_bloque()
        # imprimir estado tras cerrar ámbito
        self.imprimir_tabla_parcial("cerrar_ambito")
        return None

    def visitar_PROGRAMA(self, node):
        # Registrar todas las funciones antes de evaluar llamadas (referencias adelante)
        for child in node.nodos:
            if child.tipo == TipoNodo.DECLARACIONFUNCION:
                self._registrar_funcion(child)

        for child in node.nodos:
            child.visitar(self)
        return None

    def visitar_INCLUDE(self, node):
        nombre = node.nodos[0].valor if node.nodos else "desconocido"
        # Advertencia informativa; no bloquea la verificación semántica
        self.errores.append(
            f"Advertencia: include '{nombre}' no fue verificado (módulo externo) "
            f"en línea {node.atributos.get('linea')} columna {node.atributos.get('columna')}"
        )
        return None

    def visitar_DECLARACIONFUNCION(self, node):
        nombre = node.nodos[0].valor
        firma = self.funciones.get(nombre)
        if firma is None:
            firma = self._registrar_funcion(node)

        return_type, parametros, nombres = self._extraer_firma_funcion(node)

        self.tabla_simbolos.abrir_bloque()
        # imprimir tras abrir bloque de función
        self.imprimir_tabla_parcial("abrir_ambito_funcion", nombre)
        for nombre_param, tipo_param in zip(nombres, parametros):
            registrado = self.tabla_simbolos.nuevo_registro(
                nombre_param, tipo_param, def_node=node
            )
            if registrado:
                self.imprimir_tabla_parcial("parametro", nombre_param)

        funcion_anterior = self.funcion_actual
        self.funcion_actual = nombre

        self._funcion_tiene_retorno = False

        if node.nodos and node.nodos[-1].tipo == TipoNodo.BLOQUE:
            node.nodos[-1].visitar(self)

        if return_type is not None and not self._funcion_tiene_retorno:
            self.errores.append(
                f"Función '{nombre}' declara tipo de retorno {return_type} pero no contiene "
                f"ninguna instrucción '>>' de retorno en línea {node.atributos.get('linea')} "
                f"columna {node.atributos.get('columna')}"
            )

        self.funcion_actual = funcion_anterior
        self._funcion_tiene_retorno = False
        self.tabla_simbolos.cerrar_bloque()
        # imprimir tras cerrar bloque de función
        self.imprimir_tabla_parcial("cerrar_ambito_funcion", nombre)
        return None

    # ------------------------------------------------------------------ #
    #  Helpers privados                                                    #
    # ------------------------------------------------------------------ #

    def _registrar_funcion(self, node):
        nombre = node.nodos[0].valor
        if nombre in self.funciones:
            self.errores.append(
                f"Función '{nombre}' ya declarada en línea {node.atributos.get('linea')} "
                f"columna {node.atributos.get('columna')}"
            )
            return None

        return_type, parametros, nombres = self._extraer_firma_funcion(node)
        self.funciones[nombre] = {
            "return": return_type,
            "params": parametros,
            "param_names": nombres,
        }
        return self.funciones[nombre]

    def _extraer_firma_funcion(self, node):
        return_type = None
        parametros = []
        nombres = []
        idx = 1

        if idx < len(node.nodos) and node.nodos[idx].tipo == TipoNodo.TIPO:
            if idx + 1 == len(node.nodos) or node.nodos[idx + 1].tipo != TipoNodo.FRASE:
                return_type = node.nodos[idx].valor
                idx += 1

        while (
            idx + 1 < len(node.nodos)
            and node.nodos[idx].tipo == TipoNodo.TIPO
            and node.nodos[idx + 1].tipo == TipoNodo.FRASE
        ):
            parametros.append(node.nodos[idx].valor)
            nombres.append(node.nodos[idx + 1].valor)
            idx += 2

        return return_type, parametros, nombres

    def _resolver_tipo_aritmetico(self, tipo_izq, operador, tipo_derecho, atributos):
        if tipo_izq is None or tipo_derecho is None:
            return None

        if operador == "+":
            if tipo_izq == tipo_derecho and tipo_izq in ["NNN", "CCC", "LLL"]:
                return tipo_izq
            self.errores.append(
                f"Error de tipos en operación aritmética: no se puede sumar {tipo_izq} con "
                f"{tipo_derecho} en línea {atributos.get('linea')} columna {atributos.get('columna')}"
            )
            return None

        if operador in ["-", "*", "/", "%", "^"]:
            if tipo_izq == "NNN" and tipo_derecho == "NNN":
                return "NNN"
            self.errores.append(
                f"Error de tipos en operación aritmética: el operador '{operador}' requiere "
                f"números en línea {atributos.get('linea')} columna {atributos.get('columna')}"
            )
            return None

        if operador == "&":
            if tipo_izq == "NNN" and tipo_derecho == "NNN":
                return "NNN"
            self.errores.append(
                f"Error de tipos en operación aritmética: el operador '&' requiere números en "
                f"línea {atributos.get('linea')} columna {atributos.get('columna')}"
            )
            return None

        self.errores.append(
            f"Operador aritmético desconocido '{operador}' en línea {atributos.get('linea')} "
            f"columna {atributos.get('columna')}"
        )
        return None

    

    def imprimir_asa_decorado(self, nodo, nivel=0):
        if nodo is None:
            return

        prefijo = "│   " * nivel

        print(
            f"{prefijo}"
            f"{Fore.CYAN}├── "
            f"{Fore.WHITE}{nodo.tipo.value}"
            f"{Fore.YELLOW} ({nodo.valor})"
        )

        if nodo.atributos.get("def"):
            d = nodo.atributos["def"]
            print(
                f"{prefijo}{Fore.GREEN}│   Def: {d['nombre']} : {d['tipo']}"
            )

        if nodo.atributos.get("ref"):
            r = nodo.atributos["ref"]
            print(
                f"{prefijo}{Fore.MAGENTA}│   Ref: {r['nombre']} : {r['tipo']}"
            )

        for hijo in getattr(nodo, "nodos", []):
            self.imprimir_asa_decorado(hijo, nivel + 1)