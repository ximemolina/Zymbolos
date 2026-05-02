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

    def __avanzar(self):
        """#!!!!!!!!!creo q esto sirve (se podrá probar hasta terminar todos los módulos)!!!!!!!"""
        if self.lista_componentes:
            self.token_actual = self.lista_componentes.pop(0)
        else:
            self.token_actual = None

    def __manejar_error(self, mensaje):
        """
        Usamos el modo pánico
        nuestro simbolo terminal es !
        """
        print(f"ERROR SINTACTICO: {mensaje} \n ")
        while self.token_actual is not None and self.token_actual.valor != "!":
            self.__avanzar()
        if self.token_actual is not None and self.token_actual.valor == "!":
            self.__avanzar()

    def __verificar(self, esperado):
        """
        Verifica que el componente actual sea el esperado.
        Si coincide, avanza al siguiente token.
        Si no coincide, maneja el error y aplica modo pánico.
        """
        if self.token_actual is None:
            self.__manejar_error(
                f"Se esperaba '{esperado}' pero llegó al final del archivo"
            )
            return
        if self.token_actual.valor == esperado:
            self.__avanzar()
        else:
            self.__manejar_error(
                f"En línea {self.token_actual.linea}, columna {self.token_actual.columna}: se esperaba '{esperado}' pero se encontró '{self.token_actual.valor}'"
            )

    #! ------------Las declaré para que no me dé algo raro cuando llame a una función que no existe--------------------------------

    def __analizar_programa(self):
        """#!!!!!!!!!creo q esto sirve (se podrá probar hasta terminar todos los módulos)!!!!!!!
        Programa ::= ( Include | Funcion | LlamadaFuncion | Comentarios )*
        """

        nodos_nuevos = []

        while True:

            try:
                # Verificar si hay más tokens
                if self.token_actual is None:
                    break

                """Includes"""
                if self.token_actual.valor == "#":
                    nodos_nuevos += [self.__analizar_include()]
                elif self.token_actual.valor == ".":
                    nodos_nuevos += [self.__analizar_declaracion_funcion()]
                elif self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                    nodos_nuevos += [
                        self.__analizar_llamada_funcion()
                    ]  # no hay que poner los comentarios o si? pq igual como el exploraor los ignora según yp
                elif self.token_actual.tipo == TipoToken.IO_OP:
                    nodos_nuevos += [self.__analizar_funciones_predeterminadas()]
                else:
                    break
            except Exception as e:
                self.__manejar_error(f"Error en programa: {e}")
                return None
        return Nodo(TipoNodo.PROGRAMA, nodos=nodos_nuevos)

    def __analizar_include(self):
        """Include ::= "#" Frase "!" """

        nodos_nuevos = []

        try:
            self.__verificar("#")

            nodos_nuevos += [self.__analizar_frase()]

            self.__verificar("!")

            return Nodo(TipoNodo.INCLUDE, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en include: {e}")
            return None

    def __analizar_declaracion_funcion(self):
        """DeclaraciónFunción ::= “.” Frase >> Tipo? << (Tipo Frase)*! Bloque “.” !"""

        nodos_nuevos = []

        try:
            self.__verificar(".")

            nodos_nuevos += [self.__analizar_frase()]

            self.__verificar(">>")

            if self.token_actual.tipo == TipoToken.TIPO:
                nodos_nuevos += [self.__analizar_tipo()]

            self.__verificar("<<")

            # a ver si hay parámetros
            while self.token_actual.tipo == TipoToken.TIPO:
                nodos_nuevos += [self.__analizar_tipo()]
                nodos_nuevos += [self.__analizar_frase()]

            self.__verificar("!")

            nodos_nuevos += [self.__analizar_bloque()]

            self.__verificar(".")
            self.__verificar("!")

            return Nodo(TipoNodo.DECLARACIONFUNCION, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en declaración de función: {e}")
            return None

    def __analizar_llamada_funcion(self):
        """LlamadaFuncion ::=  Frase Término* !"""

        nodos_nuevos = []

        try:
            nodos_nuevos += [self.__analizar_frase()]

            while (
                self.token_actual.tipo == TipoToken.NUMERO
                or self.token_actual.tipo == TipoToken.IDENTIFICADOR
                or self.token_actual.tipo == TipoToken.STRING
            ):
                nodos_nuevos += [self.__analizar_termino()]

            self.__verificar("!")

            return Nodo(TipoNodo.LLAMADAFUNCION, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en llamada de función: {e}")
            return None

    def __analizar_bloque(self, token_cierre=None):
        """Bloque::=  ( Bucles | Condicionales | FuncionesPredeterminadas |
        DeclaraciónVariables | Comentarios | LlamadaFuncion | Asignacion | AsignacionElementoLista)*
        """

        nodos_nuevos = []

        while True:
            try:
                if self.token_actual is None:
                    break

                # Ok, es que en un bloque o cosas que abren y cierren como bucles o condicionales el token de cierre es el que define que debe haber para ver cual termina por las anidaciones y eso
                # entonces hay que hacer estas cosas raras, en este caso ver que venga un ! dsp
                if token_cierre and self.token_actual.valor == token_cierre:
                    next_token = (
                        self.lista_componentes[0] if self.lista_componentes else None
                    )
                    if next_token is None:
                        break
                    if next_token.valor == "!":
                        break
                    # si no es un ! es pq no era de cierrre y mas bien abre uno anidado
                elif self.token_actual.valor == "@":
                    nodos_nuevos += [self.__analizar_bucles()]
                elif self.token_actual.valor == "¿":
                    nodos_nuevos += [self.__analizar_condicionales()]
                elif self.token_actual.tipo == TipoToken.IO_OP:
                    nodos_nuevos += [self.__analizar_funciones_predeterminadas()]
                elif self.token_actual.valor == ":":
                    nodos_nuevos += [self.__analizar_declaracion_variables()]
                elif self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                    nodos_nuevos += [self.__analizar_llamada_funcion()]
                elif self.token_actual.valor == "\\":
                    nodos_nuevos += [self.__analizar_asignacion()]
                elif self.token_actual.valor == "¨":
                    nodos_nuevos += [self.__analizar_asignacion_elemento_lista()]
                else:
                    break
            except Exception as e:
                self.__manejar_error(f"Error en bloque: {e}")
                return None
        return Nodo(TipoNodo.BLOQUE, nodos=nodos_nuevos)

    def __analizar_declaracion_variables(self):
        """DeclaraciónVariables ::=  : Frase Tipo = (Termino | Bool | Lista | ExpresionesMatematicas)!   EXPERIMENTO"""

        nodos_nuevos = []

        try:
            self.__verificar(":")

            nodos_nuevos += [self.__analizar_frase()]

            nodos_nuevos += [self.__analizar_tipo()]

            self.__verificar("=")

            if self.token_actual.tipo == TipoToken.BOOL:
                nodos_nuevos += [self.__analizar_bool()]
            elif self.token_actual.valor == "{":
                nodos_nuevos += [self.__analizar_lista()]
            else:
                nodos_nuevos += [self.__analizar_expresiones_matematicas()]

            self.__verificar("!")
            return Nodo(TipoNodo.DECLARACIONVARIABLES, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en declaración de variables: {e}")
            return None

    def __analizar_funciones_predeterminadas(self):
        """FuncionesPredeterminadas ::=  (<<< | >>> | >>| <<) (Termino | Tipo | Lista | Bool) + !"""
        nodos_nuevos = []
        try:
            if self.token_actual.tipo == TipoToken.IO_OP:
                funcion = self.token_actual.valor
                self.__avanzar()
            else:
                raise SyntaxError(
                    f"ERROR: se esperaba una función predeterminada: <<<, >>>, >>, << en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
                )

            while True:
                if (
                    self.token_actual.tipo == TipoToken.NUMERO
                    or self.token_actual.tipo == TipoToken.IDENTIFICADOR
                    or self.token_actual.tipo == TipoToken.STRING
                ):
                    nodos_nuevos += [self.__analizar_termino()]
                elif self.token_actual.tipo == TipoToken.TIPO:
                    nodos_nuevos += [self.__analizar_tipo()]
                elif self.token_actual.valor == "{":
                    nodos_nuevos += [self.__analizar_lista()]
                elif self.token_actual.tipo == TipoToken.BOOL:
                    nodos_nuevos += [self.__analizar_bool()]
                else:
                    break

            self.__verificar("!")

            return Nodo(
                TipoNodo.FUNCIONESPREDETERMINADAS, valor=funcion, nodos=nodos_nuevos
            )

        except Exception as e:
            self.__manejar_error(f"Error en función predeterminada: {e}")
            return None

    def __analizar_expresiones_matematicas(self):
        """ExpresionesMatematicas ::=  Termino (Simbolo Termino)*"""

        nodos_nuevos = []

        try:
            nodos_nuevos += [self.__analizar_termino()]

            while self.token_actual and self.token_actual.tipo == TipoToken.ARITH_OP:
                nodos_nuevos += [self.__analizar_simbolo()]
                nodos_nuevos += [self.__analizar_termino()]

            return Nodo(TipoNodo.EXPRESIONESMATEMATICAS, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en expresiones matemáticas: {e}")
            return None

    #! --------------------------------------------

    def __analizar_condicionales(self):
        """Condicionales ::=  ¿(~)? Comparaciones ! Bloque  (¿”?” Comparaciones !  Bloque)* (“?” Bloque)? ¿!"""

        nodos_nuevos = []

        try:
            # Verificar apertura del condicional
            self.__verificar("¿")

            # Negación opcional
            if self.token_actual.valor == "~":
                self.__verificar("~")

            # Primera comparación obligatoria
            nodos_nuevos += [self.__analizar_comparaciones()]
            self.__verificar("!")

            # Primer bloque obligatorio, pasando el token de cierre '¿' para anidación
            nodos_nuevos += [self.__analizar_bloque(token_cierre="¿")]

            # Posibles ramas adicionales con ¿"?" Comparaciones ! Bloque
            while True:
                if self.token_actual.valor == "¿":
                    self.__verificar("¿")
                    # Para validar que no es un cierre de condicional
                    if self.token_actual.valor == "!":
                        self.__verificar("!")
                        return Nodo(TipoNodo.CONDICIONALES, nodos=nodos_nuevos)
                    elif self.token_actual.valor == "?":
                        self.__verificar("?")
                        nodos_nuevos += [self.__analizar_comparaciones()]
                        self.__verificar("!")
                        nodos_nuevos += [self.__analizar_bloque(token_cierre="¿")]
                # Significa que no hay ramas adicionales
                else:
                    break

            # Rama opcional final: "? Bloque"
            if self.token_actual.valor == "?":
                self.__verificar("?")
                nodos_nuevos += [self.__analizar_bloque(token_cierre="¿")]

            # Cierre de condicional
            self.__verificar("¿")
            self.__verificar("!")

            return Nodo(TipoNodo.CONDICIONALES, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en condicional: {e}")
            return None

    def __analizar_bucles(self):
        """Bucles ::= “@” Comparaciones ! Bloque “@”  “!”"""

        nodos_nuevos = []

        try:

            # Verificar apertura del bucle
            self.__verificar("@")

            # Verificar comparaciones
            nodos_nuevos += [self.__analizar_comparaciones()]

            # Verficar componente obligatorio
            self.__verificar("!")

            # Verificar bloque
            nodos_nuevos += [self.__analizar_bloque(token_cierre="@")]

            # Verificar que no hayamos llegado al final
            if self.token_actual is None:
                raise SyntaxError("Final inesperado del archivo dentro del bucle")

            # Verifiar cierre de bucle
            self.__verificar("@")
            self.__verificar("!")

            return Nodo(TipoNodo.BUCLES, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en bucle: {e}")
            return None

    def __analizar_asignacion(self):
        """Asignacion ::= “\” Frase "=" (Bool | ExpresionesMatematicas | Lista | AccesoLista) "!" """

        nodos_nuevos = []

        try:
            # Verificar componente de apertura
            self.__verificar("\\")

            # Verificar frase
            nodos_nuevos += [self.__analizar_frase()]  # le puse ()

            # Verificar componente obligatorio
            self.__verificar("=")

            # Hay varios casos
            # Caso 1: Bool
            if self.token_actual.tipo == TipoToken.BOOL:
                nodos_nuevos += [self.__analizar_bool()]

            # Caso 2: Acceso a elemento de lista
            elif self.token_actual.valor == "¨":
                nodos_nuevos += [self.__analizar_acceso_lista()]

            # Caso 3: ExpresionesMatematicas
            elif (
                self.token_actual.tipo == TipoToken.NUMERO
                or self.token_actual.tipo == TipoToken.IDENTIFICADOR
                or self.token_actual.tipo == TipoToken.STRING
            ):
                nodos_nuevos += [self.__analizar_expresiones_matematicas()]

            # Caso 4: Lista
            elif self.token_actual.valor == "{":
                nodos_nuevos += [self.__analizar_lista()]

            # Verificar cierre de bloque
            self.__verificar("!")

            return Nodo(TipoNodo.ASIGNACION, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en asignación: {e}")
            return None

    def __analizar_asignacion_elemento_lista(self):
        """AsignacionElementoLista ::= AccesoLista "=" Termino "!"""

        nodos_nuevos = []

        try:
            # Verificar acceso a lista
            nodos_nuevos += [self.__analizar_acceso_lista()]

            # Verifcar componente obligatoria
            self.__verificar("=")

            # Verificar termino
            nodos_nuevos += [self.__analizar_termino()]

            # Verificar cierre de asignación
            self.__verificar("!")

            return Nodo(TipoNodo.ASIGNACIONELEMENTOLISTA, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en asignación en lista: {e}")
            return None

    def __analizar_comparaciones(self):
        """Comparaciones ::=  Comparacion (CompuertasLogicas Comparacion)*"""

        nodos_nuevos = []

        try:
            # Verificar primera Comparacion
            nodos_nuevos += [self.__analizar_comparacion()]

            # Verificar si hay mas comparaciones adicionales
            while self.token_actual and self.token_actual.tipo == TipoToken.LOGIC_OP:
                nodos_nuevos += [self.__analizar_compuerta_logica()]
                nodos_nuevos += [self.__analizar_comparacion()]

            return Nodo(TipoNodo.COMPARACIONES, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en comparaciones: {e}")
            return None

    def __analizar_comparacion(self):
        """Comparacion ::=  Valor (Comparativos Valor)*"""

        nodos_nuevos = []

        try:
            # Verificar Valor
            nodos_nuevos += [self.__analizar_valor()]

            # Verificar comparaciones adicionales
            while self.token_actual and self.token_actual.tipo == TipoToken.REL_OP:
                nodos_nuevos += [self.__analizar_comparativo()]
                nodos_nuevos += [self.__analizar_valor()]

            return Nodo(TipoNodo.COMPARACION, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en comparación: {e}")
            return None

    def __analizar_lista(self):
        """Lista::=  "{" (Termino ("," Termino)*)? "}" """

        nodos_nuevos = []

        try:
            # Verificar apertura de la lista
            self.__verificar("{")

            # Verificar existencia de elemento opcional
            if (
                self.token_actual.tipo == TipoToken.NUMERO
                or self.token_actual.tipo == TipoToken.IDENTIFICADOR
                or self.token_actual.tipo == TipoToken.STRING
            ):
                # Primer elemento
                nodos_nuevos += [self.__analizar_termino()]
                # Demás elementos
                while self.token_actual.valor == ",":
                    self.__verificar(",")
                    nodos_nuevos += [self.__analizar_termino()]

            # Verificar cierre de la lista
            self.__verificar("}")

            return Nodo(TipoNodo.LISTA, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en lista: {e}")
            return None

    def __analizar_acceso_lista(self):
        """AccesoLista ::= “¨” Frase “[" Indice “]”"""

        nodos_nuevos = []

        try:
            # Verificar apertura del acceso de lista
            self.__verificar("¨")

            # Verificar que sigue una frase
            nodos_nuevos += [self.__analizar_frase()]

            # Verificar componente de apertura obligatoria
            self.__verificar("[")

            # Verificar que tenga un indice
            nodos_nuevos += [self.__analizar_indice()]

            # Verificar componente de cierre obligatoria
            self.__verificar("]")

            return Nodo(TipoNodo.ACCESOLISTA, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error en el acceso de lista: {e}")
            return None

    def __analizar_valor(self):
        """Valor ::=  Bool | ExpresionesMatematicas | AccesoLista.        Experimento"""

        nodos_nuevos = []

        try:

            # Si es Bool
            if self.token_actual.tipo == TipoToken.BOOL:
                nodos_nuevos += [self.__analizar_bool()]

            # Si es AccesoLista
            elif self.token_actual.valor == "¨":
                nodos_nuevos += [self.__analizar_acceso_lista()]

            # Si es ExpresionesMatematicas
            elif (
                self.token_actual.tipo == TipoToken.NUMERO
                or self.token_actual.tipo == TipoToken.IDENTIFICADOR
                or self.token_actual.tipo == TipoToken.STRING
            ):
                nodos_nuevos += [self.__analizar_expresiones_matematicas()]

            else:
                raise Exception(
                    f"""Se esperaba un término o un boleano {self.token_actual.linea}, 
                    columna {self.token_actual.columna}"""
                )

            return Nodo(TipoNodo.VALOR, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error de valor: {e}")
            return None

    def __analizar_indice(self):
        """Indice ::= Indice ::= Numero | Frase"""

        nodos_nuevos = []

        try:
            if self.token_actual.tipo == TipoToken.NUMERO:
                nodos_nuevos += [self.__analizar_numero()]
            elif self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                nodos_nuevos += [self.__analizar_frase()]
            else:
                raise Exception(
                    f"ERROR: se esperaba un número o frase como índice en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
                )

            return Nodo(TipoNodo.INDICE, nodos=nodos_nuevos)

        except Exception as e:
            self.__manejar_error(f"Error de índice: {e}")
            return None

    def __analizar_termino(self):
        """Termino ::= Numero | Frase | Cadena"""

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
                f"ERROR: se esperaba un símbolo aritmético: +, -, /, %, *, ^, en línea {self.token_actual.linea}, columna {self.token_actual.columna}"
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
