class Visitor:
    """Clase base para visitantes del ASA.

    Implementa `visit(node)` que despacha a `visit_<TIPONODO>(node)` si existe,
    y un `generic_visit` que recorre los nodos hijos.
    """

    def visit(self, node):
        method = getattr(self, f"visit_{node.tipo.name}", None)
        if callable(method):
            return method(node)
        return self.generic_visit(node)

    def generic_visit(self, node):
        for child in getattr(node, "nodos", []) or []:
            if hasattr(child, "accept"):
                child.accept(self)



