import sys
from explorador.Explorador import lexer


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