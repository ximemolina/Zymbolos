# Zymbolos
Proyecto de **Compiladores e Intérpretes**

---

### Uso
Escribir en la terminal el siguiente comando
```bash
python main.py ejemplos/[nombreDeArchivoAProcesar].zy
```

---

### Sintaxis del Lenguaje

#### Tipos de datos

| Tipo | Descripción        |
|------|--------------------|
| `NNN` | Número entero o decimal |
| `CCC` | Cadena de texto    |
| `BBB` | Booleano           |
| `OOO` | Objeto             |
| `EEE` | Elemento           |
| `LLL` | Lista              |

#### Valores literales

| Literal | Descripción | Ejemplo |
|---------|-------------|---------|
| `"..."` | Cadena de texto | `"hola mundo"` |
| `VV` | Verdadero (true) | `VV` |
| `FF` | Falso (false) | `FF` |
| `123` / `3.14` | Número | `42` |
| `{a, b, c}` | Lista | `{1, 2, 3}` |

#### Operadores

| Operador | Tipo | Descripción |
|----------|------|-------------|
| `+` `-` `*` `/` `%` `^` | Aritmético | Operaciones matemáticas |
| `==` `!=` `<` `>` `<=` `>=` | Relacional | Comparaciones |
| `&&` `\|\|` | Lógico | Y / O |
| `=` | Asignación | Asignar valor |
| `+=` `-=` `*=` `/=` `%=` | Asignación compuesta | Modificar y asignar |
| `++` | Incremento | Incrementar en 1 |
| `~` | Negación | Negar condición |

#### Funciones de entrada/salida

| Símbolo | Descripción |
|---------|-------------|
| `<<<` | Imprimir en pantalla |
| `>>>` | Leer entrada del usuario |
| `<<` | Salida de valor |
| `>>` | Entrada de valor |

#### Comentarios

| Sintaxis | Descripción |
|----------|-------------|
| `_ comentario` | Comentario de una línea |
| `__ comentario __` | Comentario multilínea |



---

### Configuración de Sintaxis en VS Code
El repositorio incluye una extensión de VS Code que resalta la sintaxis de los archivos `.zy` con los colores del lenguaje Zymbolos.

#### Opción A — Instalar directo con el `.vsix` (más fácil)
1. Descargar el archivo `zymbolos-0.0.1.vsix`
2. En VS Code abrir el panel de extensiones (`Ctrl+Shift+X`)
3. Hacer clic en el menú `...` arriba a la derecha
4. Seleccionar **"Install from VSIX..."** y elegir el archivo

O desde la terminal:
```bash
code --install-extension zymbolos-0.0.1.vsix
```

> ⚠️ Después de instalar, VS Code puede pedir refrescar la ventana. Si no aparece la notificación automáticamente, usar `Ctrl+Shift+P` → escribir **"Reload Window"** → Enter.

#### Opción B — Compilar desde los archivos fuente
Si se quiere modificar la extensión, los archivos fuente están en la carpeta `vscode/`:

```
vscode/
├── package.json
├── language-configuration.json
└── syntaxes/
    └── zymbolos.tmLanguage.json
```

Para compilar y generar el `.vsix`:

```bash
# Instalar la herramienta de empaquetado (solo la primera vez)
npm install -g @vscode/vsce

# Entrar a la carpeta
cd vscode

# Generar el .vsix
npx vsce package --no-dependencies
```

Esto genera el archivo `zymbolos-0.0.1.vsix` en la misma carpeta. Instalarlo con los pasos de la Opción A.

#### Resultado esperado
Después de instalar y refrescar, abrir cualquier archivo `.zy` y VS Code mostrará el lenguaje **Zymbolos** en la barra inferior con resaltado de sintaxis automático.

---

### Desarrolladores
- Susana Feng
- Evelyn Ulate
- Natalia Orozco
- Daniel Mendez
- Ximena Molina