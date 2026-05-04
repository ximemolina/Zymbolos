# pruebas/runner.py
import unittest
from tests.test_hojas import PruebasHojas
from tests.test_internos import PruebasInternos

suites = [
    PruebasHojas,
    PruebasInternos,
]  # agregar mas conforme se vayan creando nuevas clases de pruebas

for clase in suites:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(clase)

    ok = sum(1 for t in suite if unittest.TestResult().wasSuccessful())

    ok = 0
    fail = 0
    for test in suite:
        result = unittest.TestResult()
        test.run(result)
        if result.wasSuccessful():
            ok += 1
        else:
            fail += 1

    estado = "✅" if fail == 0 else "❌"
    print(
        f"  {estado} {clase.__name__:<30} {ok} pasadas  {fail} fallidas  {ok+fail} total"
    )

print(f"\n{'─'*40}\n")
