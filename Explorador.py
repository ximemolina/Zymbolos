import sys
import re

Tokens = [
    ('COMENTARIO_MULT', r'__.*?__'),
    ('COMENTARIO_SOLO', r'_[^\n]*'),

    ('IO_OP', r'>>>|<<<|>>|<<'),
    ('REL_OP', r'<=|>=|==|<|>'),
    ('LOGIC_OP', r'&&|\|\|'),
    ('INCREMENT', r'\+\+'),

    ('STRUCT', r'[.:@!#°¿?]'),
    ('DELIM', r'[\[\]{},()]'),
    ('ASSIGN', r'\+=|-=|\*=|/=|='),
    ('ARITH_OP', r'[+\-*/%^]'),

    ('STRING', r'"[^"\n]*"'),
    ('NUMERO', r'-?\d+(\.\d+)?'),
    ('BOOL', r'\b(VV|FF)\b'),
    ('TIPO', r'\b(NNN|CCC|BBB|OOO|EEE|LLL|STR)\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'),

    ('SALTO', r'[ \t]+'),
    ('CONFUSION', r'.'),
]

tok_regex = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in Tokens)


def print_token(tipo_token, valor, linea, col):
    print(f'<"{tipo_token}","{valor}","line={linea},col={col}">')


def lexer(linea, numero_linea):
    for mo in re.finditer(tok_regex, linea):
        tipo = mo.lastgroup
        valor = mo.group()
        columna = mo.start() + 1

        if tipo in ('SALTO', 'COMENTARIO_SOLO', 'COMENTARIO_MULT'):
            continue

        elif tipo == 'CONFUSION':
            print(f'ERROR LEXICO: símbolo inválido "{valor}" en línea {numero_linea}, columna {columna}')
            #sys.exit(1) para que no se cierre con el primer error.


        else:
            print_token(tipo, valor, numero_linea, columna)


def main():
    if len(sys.argv) != 2:
        print("Uso: python Explorador.py <archivo>")
        sys.exit(1)

    archivo = sys.argv[1]

    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            for numero_linea, linea in enumerate(file, start=1):
                lexer(linea, numero_linea)
    except FileNotFoundError:
        print(f"ERROR: No se pudo abrir el archivo '{archivo}'")
        #sys.exit(1)  para que no se cierre con el primer error.


if __name__ == "__main__":
    main()