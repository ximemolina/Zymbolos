from enum import Enum

###################################################################
### Clase para definir los tipos de tokens que procesará el asa ###
### PD: Estos tipos son los que generó el explorador            ###
###################################################################


class TipoToken(Enum):
    IO_OP = "IO_OP"
    REL_OP = "REL_OP"
    LOGIC_OP = "LOGIC_OP"
    INCREMENT = "INCREMENT"

    STRUCT = "STRUCT"
    DELIM = "DELIM"
    ASSIGN = "ASSIGN"
    ARITH_OP = "ARITH_OP"

    STRING = "STRING"
    NUMERO = "NUMERO"
    BOOL = "BOOL"
    TIPO = "TIPO"
    IDENTIFICADOR = "IDENTIFICADOR"


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
