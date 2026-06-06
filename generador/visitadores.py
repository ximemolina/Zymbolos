class VisitantePython:

    def __init__(self):
        self.indentacion = 0

    def visitar(self, nodo):
        metodo = getattr(
            self,
            f"visitar_{nodo.tipo.name}",
            self.generic_visit
        )
        return metodo(nodo)

    def generic_visit(self, nodo):
        return "\n".join(
            self.visitar(hijo)
            for hijo in nodo.nodos
        )

    def tab(self):
        return "    " * self.indentacion
    
    def visitar_PROGRAMA(self, nodo):
        '''
        Programa ::= ( Include | Declaracion | LlamadaFuncion | Comentarios )*
        '''
        lineas = []

        for hijo in nodo.nodos:
            codigo = self.visitar(hijo)

            if codigo:
                lineas.append(codigo)

        return "\n\n".join(lineas)
    
    def visitar_INCLUDE(self, nodo):
        '''
        Include ::=  # Frase!
        '''
        modulo = nodo.nodos[0].valor

        return f"import {modulo}"
    
    def visitar_DECLARACIONFUNCION(self, nodo):
        '''
        DeclaraciónFunción ::= “.” Frase >> Tipo? << (Tipo Frase)*! Bloque “.” !
        '''
        nombre = nodo.nodos[0].valor

        parametros = []
        bloque = None

        i = 1

        while i < len(nodo.nodos):

            actual = nodo.nodos[i]

            if actual.tipo.name == "BLOQUE":
                bloque = actual
                break

            if (
                actual.tipo.name == "TIPO"
                and i + 1 < len(nodo.nodos)
                and nodo.nodos[i + 1].tipo.name == "FRASE"
            ):
                parametros.append(
                    nodo.nodos[i + 1].valor
                )
                i += 2
                continue

            i += 1

        cuerpo = self.visitar(bloque)

        return (
            f"def {nombre}({', '.join(parametros)}):\n"
            f"{cuerpo}"
        )
    
    def visitar_BLOQUE(self, nodo):
        '''
        Bloque::=  ( Bucles | Condicionales | FuncionesPredeterminadas | DeclaraciónVariables | Comentarios | LlamadaFuncion | Asignacion | AsignacionElementoLista)*
        '''
        self.indentacion += 1

        lineas = []

        for hijo in nodo.nodos:

            codigo = self.visitar(hijo)

            if codigo:
                lineas.append(
                    self.tab() + codigo
                )

        self.indentacion -= 1

        if not lineas:
            return self.tab() + "pass"

        return "\n".join(lineas)
    
    def visitar_LLAMADAFUNCION(self, nodo):
        '''
        LlamadaFuncion ::=  Frase Término* !
        '''
        nombre = nodo.nodos[0].valor

        argumentos = [
            self.visitar(arg)
            for arg in nodo.nodos[1:]
        ]

        return (
            f"{nombre}({', '.join(argumentos)})"
        )
    
    def visitar_DECLARACIONVARIABLES(self, nodo):
        '''
        DeclaraciónVariables ::=  : Frase Tipo = (Termino | Bool | Lista | Expresionesmatematicas)!
        '''
        nombre = nodo.nodos[0].valor
        valor = self.visitar(nodo.nodos[2])

        return f"{nombre} = {valor}"
    
    def visitar_EXPRESIONESMATEMATICAS(self, nodo):
        '''
        ExpresionesMatematicas ::=  Termino (Simbolo Termino)*
        '''
        resultado = self.visitar(nodo.nodos[0])

        i = 1

        while i < len(nodo.nodos):

            operador = self.visitar(nodo.nodos[i])

            if operador == "^":
                operador = "**"

            derecho = self.visitar(
                nodo.nodos[i + 1]
            )

            resultado += (
                f" {operador} {derecho}"
            )

            i += 2

        return resultado
    
    def visitar_COMPARACION(self, nodo):
        '''
        Comparacion ::=  Valor (Comparativos Valor)*
        '''

        resultado = self.visitar(
            nodo.nodos[0]
        )

        i = 1

        while i < len(nodo.nodos):

            operador = self.visitar(
                nodo.nodos[i]
            )

            valor = self.visitar(
                nodo.nodos[i + 1]
            )

            resultado += (
                f" {operador} {valor}"
            )

            i += 2

        return resultado
    
    def visitar_COMPARACIONES(self, nodo):
        '''
        Comparaciones ::=  Comparacion (CompuertasLogicas Comparacion)*
        '''
        resultado = self.visitar(
            nodo.nodos[0]
        )

        i = 1

        while i < len(nodo.nodos):

            compuerta = self.visitar(
                nodo.nodos[i]
            )

            expresion = self.visitar(
                nodo.nodos[i + 1]
            )

            if compuerta == "&&":
                compuerta = "and"

            elif compuerta == "||":
                compuerta = "or"

            resultado += (
                f" {compuerta} {expresion}"
            )

            i += 2

        return resultado

