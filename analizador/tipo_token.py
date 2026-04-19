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
