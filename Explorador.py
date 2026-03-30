import sys
import re

TOKEN_SPECIFICATION = [
    ('COMENTARIO_MULT', r'__.*?__'),
    ('COMENTARIO_SOLO', r'_[^\n]*'),

    ('IO_OP', r'>>>|<<<|>>'),
    ('REL_OP', r'<=|>=|=='),
    ('LOGIC_OP', r'&&|\|\|'),
    ('INCREMENT', r'\+\+'),

    ('STRUCT', r'[.:@!#°¿?]'),
    ('DELIM', r'[{},()]'),
    ('ASSIGN', r'\+=|-=|\*=|/=|%='),
    ('ARITH_OP', r'[+\-*/%^<>]'),

    ('STRING', r'"[^"\n]*"'),
    ('NUMERO', r'-?\d+(\.\d+)?'),
    ('BOOL', r'\b(VV|FF)\b'),
    ('TIPO', r'\b(NNN|CCC|BBB|OOO|EEE)\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('SALTO', r'[ \t]+'),
    ('CONFUSION', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)


def print_token(token_type, value, line, col):
    print(f'<"{token_type}","{value}","line={line},col={col}">')


def lexer(line, line_number):
    for mo in re.finditer(tok_regex, line):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() + 1

        if kind in ('SALTO', 'COMENTARIO_SOLO', 'COMENTARIO_MULT'):
            continue

        elif kind == 'CONFUSION':
            print(f'ERROR LEXICO: símbolo inválido "{value}" en línea {line_number}, columna {column}')
            sys.exit(1)

        else:
            print_token(kind, value, line_number, column)


def main():
    if len(sys.argv) != 2:
        print("Uso: python Explorador.py <archivo>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                lexer(line, line_number)
    except FileNotFoundError:
        print(f"ERROR: No se pudo abrir el archivo '{filename}'")
        sys.exit(1)


if __name__ == "__main__":
    main()