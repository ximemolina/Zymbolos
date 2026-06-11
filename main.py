import sys
import importlib.machinery
import subprocess
import os

importlib.machinery.SOURCE_SUFFIXES.append(".zy")

from explorador.Explorador import lexer
from analizador.analizador import Analizador
from analizador.tipo_token import convertir_token_a_enum
from verificador.visitador import Visitador
from generador.generador import Generador


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

nombre_base = os.path.splitext(os.path.basename(archivo))[0]
carpeta_salida = "python"
os.makedirs(carpeta_salida, exist_ok=True)
archivo_salida = os.path.join(carpeta_salida, nombre_base + ".py")

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
        sys.exit(1)  # 👈 detiene todo aquí si hay errores

    exito("No se encontraron errores semánticos")

    titulo("ASA DECORADO")
    visitador.imprimir_asa_decorado(analizador.asa.raiz)

    titulo("GENERANDO CÓDIGO")

    generador = Generador(analizador.asa)
    codigo_python = generador.generar()

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(codigo_python)

    exito(f"Código generado en {archivo_salida}")

    titulo("EJECUTANDO CÓDIGO GENERADO")
    resultado = subprocess.run(
        [sys.executable, archivo_salida],
        capture_output=False
    )

    if resultado.returncode != 0:
        error(f"El código generado terminó con código de salida {resultado.returncode}")

    titulo("LISTO CALISTO")

except FileNotFoundError:
    error(f"No se pudo abrir el archivo '{archivo}'")

except Exception as e:
    error(f"Error inesperado: {e}")

    import traceback
    traceback.print_exc()