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

    def __verificar(self, esperado):
        """
        Verifica que el componente actual sea el esperado.
        Si coincide, avanza al siguiente token.
        Si no coincide, lanza un error de sintaxis.
        """
        if self.token_actual.valor == esperado:
            # Avanzar al siguiente token
            self.__avanzar()
        else:
            raise SyntaxError(
                f"""Error de sintaxis en linea '{self.token_actual.linea}', 
                columna '{self.token_actual.columna}': se esperaba '{esperado}' 
                pero se encontró '{self.token_actual.valor}'"""
            )

#! ------------Las declaré para que no me dé algo raro cuando llame a una función que no existe--------------------------------
    def __analizar_bloque(self):
        """Bloque::=  ( Bucles | Condicionales | FuncionesPredeterminadas | 
        DeclaraciónVariables | Comentarios | LlamadaFuncion | Asignacion | AsignacionElementoLista)+"""

    def __analizar_expresiones_matematicas(self):
        """ExpresionesMatematicas ::=  Termino (Simbolo Termino)*"""

#! --------------------------------------------        

    def __analizar_condicionales(self):

        """Condicionales ::=  ¿(~)? Comparaciones ! Bloque  (¿”?” Comparaciones !  Bloque)* (“?” Bloque)? ¿!"""

        nodos_nuevos = []

        try:
            # Verificar apertura del condicional
            self.__verificar("¿")

            # Negación opcionar
            if self.token_actual.valor == "~":
                self.__verificar("~")

            # Primera comparación obligatoria
            nodos_nuevos += [self.__analizar_comparaciones()]
            self.__verificar('!')

            # Primer bloque obligatorio
            nodos_nuevos += [self.__analizar_bloque()]

            # Posibles ramas adicionales con ¿"?" Comparaciones ! Bloque
            while (True):
                if self.token_actual.valor == "¿":
                    self.__verificar("¿")
                    # Para validar que no es un cierre de condicional
                    if self.token_actual.valor == "!":
                        break
                    if self.token_actual.valor == "?":
                        self.__verificar("?")
                        nodos_nuevos += [self.__analizar_comparaciones()]

                        self.__verificar("!")
                        nodos_nuevos += [self.__analizar_bloque()]
                # Significa que no hay ramas adicionales
                else:
                    break

            # Rama opcional final: "? Bloque"
            if self.token_actual.valor == '?':
                self.__verificar('?')
                nodos_nuevos += [self.__analizar_bloque()]

            # Cierre de condicional
            self.__verificar('¿')
            self.__verificar('!')
            
            return Nodo(TipoNodo.CONDICIONALES, nodos=nodos_nuevos)
        
        except SyntaxError as e:
            print(f"Error de sintaxis en condicional: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en condicional: {e}")
            return None

    def __analizar_bucles(self):
        """Bucles ::= “@” (Comparaciones | Bool) ! Bloque “@”  “!”"""

        nodos_nuevos = []

        try:
            #Verificar apertura del bucle
            self.__verificar("@")

            #if self.token_actual.valor == ""

        except SyntaxError as e:
            print(f"Error de sintaxis en condicional: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en condicional: {e}")
            return None

    def __analizar_asignacion(self):
        """Asignacion ::= “\” Frase "=" (Frase | Numero | Bool | ExpresionesMatematicas 
        | Comparaciones | Lista | Cadena) "!" """

        nodos_nuevos = []

        try:
            #! Hay ambigúedad
            return None
        
        except SyntaxError as e:
            print(f"Error de asignación: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado de asignación: {e}")
            return None

    def __analizar_asignacion_elemento_lista(self):
        """AsignacionElementoLista ::= AccesoLista "=" Termino"""

        nodos_nuevos = []

        try:
            # Verificar acceso a lista que inicia con ¨
            if self.token_actual.valor == "¨":
                nodos_nuevos += [self.__analizar_acceso_lista()]
            else:
                raise Exception (
                    f"""Se esperaba un acceso a lista en línea {self.token_actual.linea}, 
                    columna {self.token_actual.columna}"""
                )
            
            # Verifcar componente obligatoria
            self.__verificar("=")

            # Verificar termino
            if self.token_actual.tipo == TipoToken.NUMERO or self.token_actual.tipo == TipoToken.IDENTIFICADOR or self.token_actual.tipo == TipoToken.STRING:  
                nodos_nuevos += [self.__analizar_termino()]

            return Nodo(TipoNodo.ASIGNACIONELEMENTOLISTA, nodos=nodos_nuevos)

        except SyntaxError as e:
            print(f"Error de sintaxis en la asignación en lista: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en asignación en lista: {e}")
            return None

    def __analizar_comparaciones(self):
        """Comparaciones ::=  Comparacion (CompuertasLogicas Comparacion)*"""

        nodos_nuevos = []

        try:
            #! Hay ambigúedad
            return None
        
        except SyntaxError as e:
            print(f"Error en comparaciones: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en comparaciones: {e}")
            return None

    def __analizar_comparacion(self):
        """Comparacion ::=  Valor Comparativos Valor"""

        nodos_nuevos = []

        try:
            #! Hay ambigúedad
            return None
        
        except SyntaxError as e:
            print(f"Error en comparación: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en comparación: {e}")
            return None

    def __analizar_lista(self):
        """Lista::=  "{" (Termino ("," Termino)*)? "}" """

        nodos_nuevos = []

        try:
            # Verificar apertura de la lista
            self.__verificar("{")

            # Verificar existencia de elemento opcional
            if self.token_actual.tipo == TipoToken.NUMERO or self.token_actual.tipo == TipoToken.IDENTIFICADOR or self.token_actual.tipo == TipoToken.STRING:
                # Primer elemento
                nodos_nuevos += [self.__analizar_termino()]
                # Demás elementos
                while (self.token_actual.valor == ","):
                    self.__verificar(",")
                    nodos_nuevos += [self.__analizar_termino()]

            # Verificar cierre de la lista
            self.__verificar("}")

            return Nodo(TipoNodo.LISTA, nodos=nodos_nuevos)

        except SyntaxError as e:
            print(f"Error de sintaxis en lista: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en lista: {e}")
            return None

    def __analizar_acceso_lista(self):
        """AccesoLista ::= “¨” Frase “[" Indice “]” """

        nodos_nuevos = []

        try:
            # Verificar apertura del acceso de lista
            self.__verificar("¨")

            # Verificar que sigue una frase
            if self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                nodos_nuevos += [self.__analizar_frase()]
            else:
                raise Exception (
                    f"""Se esperaba una frase en línea {self.token_actual.linea}, 
                    columna {self.token_actual.columna}"""
                )
            
            # Verificar componente de apertura obligatoria
            self.__verificar("[")

            # Verificar que tenga un indice 
            #! Falta el caso de usar una expresion matematica, pero hay ambiguedad
            if self.token_actual.tipo == TipoToken.NUMERO or self.token_actual.tipo == TipoToken.IDENTIFICADOR: 
                nodos_nuevos += [self.__analizar_indice()]
            else:
                raise Exception (
                    f"""Se esperaba un índice en línea {self.token_actual.linea}, 
                    columna {self.token_actual.columna}"""
                )
            
            # Verificar componente de cierre obligatoria
            self.__verificar("]")

            return Nodo(TipoNodo.ACCESOLISTA, nodos=nodos_nuevos)

        except SyntaxError as e:
            print(f"Error de sintaxis en el acceso de lista: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado en el acceso de lista: {e}")
            return None

    def __analizar_valor(self):
        """Valor ::=  Cadena | Numero | Frase | Bool | ExpresionesMatematicas"""

        nodos_nuevos = []

        try:
            #! Hay ambigúedad
            return None
        
        except SyntaxError as e:
            print(f"Error de valor: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado de valor: {e}")
            return None

    def __analizar_indice(self):
        """Indice ::= Numero | Frase | ExpresionesMatematicas"""

        nodos_nuevos = []

        try:
            # Si es número
            if self.token_actual.tipo == TipoToken.NUMERO:
                nodos_nuevos += [self.__analizar_numero()]
            # Si es Frase
            elif self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                nodos_nuevos += [self.__analizar_frase()]
            # Si es Expresión matemática
            #! Hay ambiguedad


        except SyntaxError as e:
            print(f"Error de índice: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado de índice: {e}")
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
