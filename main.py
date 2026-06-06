import sys
import importlib.machinery

importlib.machinery.SOURCE_SUFFIXES.append(".zy")

from explorador.Explorador import lexer
from analizador.analizador import Analizador
from analizador.tipo_token import convertir_token_a_enum
from verificador.visitador import Visitador


def titulo(texto):
    print("\n" + "=" * 70)
    print(f" {texto}")
    print("=" * 70)


def exito(texto):
    print(f"✓ {texto}")


def error(texto):
    print(f"✗ {texto}")


if len(sys.argv) != 2:
    error("Uso: python main.py <archivo>")
    sys.exit(1)

archivo = sys.argv[1]

try:
    todos_los_tokens = []

    titulo("EXPLORACIÓN LÉXICA")

    with open(archivo, "r", encoding="utf-8") as file:
        for numero_linea, linea in enumerate(file, start=1):
            tokens_linea = lexer(linea, numero_linea)
            todos_los_tokens.extend(tokens_linea)

    exito(f"Tokens encontrados: {len(todos_los_tokens)}")

    tokens_convertidos = [convertir_token_a_enum(token) for token in todos_los_tokens]

    if not tokens_convertidos:
        error("No hay tokens para analizar")
        sys.exit(1)

    titulo("ANÁLISIS SINTÁCTICO")

    analizador = Analizador(tokens_convertidos[1:], tokens_convertidos[0])

    analizador.analizar()

    if not analizador.asa.raiz:
        error("Error en el análisis sintáctico")
        sys.exit(1)

    exito("Análisis sintáctico completado")

    titulo("ÁRBOL DE SINTAXIS ABSTRACTA (ASA)")
    analizador.asa.mostrar_asa(analizador.asa.raiz)

    titulo("VERIFICACIÓN SEMÁNTICA")

    visitador = Visitador()
    analizador.asa.raiz.visitar(visitador)

    if visitador.errores:
        error("Se encontraron errores semánticos:\n")

        for i, err in enumerate(visitador.errores, start=1):
            print(f"  [{i}] {err}")

    else:
        exito("No se encontraron errores semánticos")

        titulo("ASA DECORADO")
        visitador.imprimir_asa_decorado(analizador.asa.raiz)

    titulo("LISTO CALISTO")

except FileNotFoundError:
    error(f"No se pudo abrir el archivo '{archivo}'")

except Exception as e:
    error(f"Error inesperado: {e}")

    import traceback

    traceback.print_exc()
