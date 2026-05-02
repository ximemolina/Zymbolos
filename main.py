import sys
from explorador.Explorador import lexer
from analizador.analizador import Analizador
from analizador.tipo_token import TipoToken


def convertir_token_a_enum(token):
    """Convierte un token del lexer (con tipo string) a enum TipoToken"""

    mapeo = {
        "STRUCT": TipoToken.STRUCT,
        "IDENTIFICADOR": TipoToken.IDENTIFICADOR,
        "IO_OP": TipoToken.IO_OP,
        "TIPO": TipoToken.TIPO,
        "NUMERO": TipoToken.NUMERO,
        "ARITH_OP": TipoToken.ARITH_OP,
        "REL_OP": TipoToken.REL_OP,
        "BOOL": TipoToken.BOOL,
        "STRING": TipoToken.STRING,
        "LOGIC_OP": TipoToken.LOGIC_OP,
        "DELIM": TipoToken.DELIM,
        "ASSIGN": TipoToken.ASSIGN,
        "INCREMENT": TipoToken.INCREMENT,
    }

    class TokenConvertido:
        def __init__(self, tipo, valor, linea, columna):
            self.tipo = tipo
            self.valor = valor
            self.linea = linea
            self.columna = columna

    tipo_enum = mapeo.get(token.tipo, TipoToken.IDENTIFICADOR)
    return TokenConvertido(tipo_enum, token.valor, token.linea, token.columna)


def mostrar_asa(nodo, nivel=0):

    if nodo is None:
        return

    indent = "  " * nivel
    if hasattr(nodo, "valor") and nodo.valor:
        print(f"{indent}{nodo.tipo.value} -> {nodo.valor}")
    else:
        print(f"{indent}{nodo.tipo.value}")

    if hasattr(nodo, "nodos") and nodo.nodos:
        for hijo in nodo.nodos:
            mostrar_asa(hijo, nivel + 1)


if len(sys.argv) != 2:
    print("Uso: python main.py <archivo>")
    sys.exit(1)

archivo = sys.argv[1]

try:

    todos_los_tokens = []

    print("EXPLORACION \n")

    with open(archivo, "r", encoding="utf-8") as file:
        for numero_linea, linea in enumerate(file, start=1):
            tokens_linea = lexer(linea, numero_linea)
            todos_los_tokens.extend(tokens_linea)

    tokens_convertidos = [convertir_token_a_enum(token) for token in todos_los_tokens]

    if tokens_convertidos:
        print("\n \n \n ANALISI \n")

        analizador = Analizador(tokens_convertidos[1:], tokens_convertidos[0])

        analizador.analizar()

        if analizador.asa.raiz:

            mostrar_asa(analizador.asa.raiz)
        else:
            print("Error en el análisis sintáctico")
    else:
        print("No hay tokens para analizar")

except FileNotFoundError:
    print(f"ERROR: No se pudo abrir el archivo '{archivo}'")
except Exception as e:
    print(f"ERROR INESPERADO: {e}")
    import traceback

    traceback.print_exc()
