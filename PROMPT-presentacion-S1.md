# Prompt para generar la presentación — Semana 1: DS Fundamentals

## Instrucción principal

Crea una presentación completa para un bootcamp de Data Science. La presentación cubre la **Semana 1** y se divide en **4 clases** de aproximadamente **1.5–2 horas** cada una. Los estudiantes son principiantes absolutos en programación y Data Science. El tono debe ser didáctico, motivador y con ejemplos del mundo real. Usa emojis con moderación para hacer el contenido más amigable.

---

## Contexto del curso

- **Bootcamp:** Data Science Fundamentals
- **Semana:** 1 de 8
- **Herramientas:** Python, Google Colab
- **Perfil del alumno:** Sin experiencia en programación. Pueden ser profesionales de otras áreas que quieren entrar al mundo de los datos.
- **Estilo:** Diapositivas limpias, pocas palabras por slide, mucho código visible, ejemplos cotidianos.

---

## Clase 1 — Introducción al Data Science y Google Colab

**Duración estimada:** 1.5–2 horas

**Objetivos de aprendizaje:**
- Entender qué es Data Science y por qué es relevante hoy
- Conocer el ciclo de vida de un proyecto de datos
- Configurar y usar Google Colab con confianza

**Contenido de los slides:**

1. **Portada de la clase**
   - Título: "Bienvenidos al Bootcamp de Data Science"
   - Subtítulo: "Clase 1 — Introducción y herramientas"

2. **¿Qué es Data Science?**
   - Definición simple: "extraer información útil de los datos"
   - El diagrama de Venn clásico (estadística + programación + dominio)
   - Ejemplos reales: Netflix, Spotify, Uber, Mercado Libre

3. **¿Por qué Data Science ahora?**
   - Estadística de datos generados por día
   - Demanda laboral y salarios
   - Industrias que lo usan (salud, fintech, retail, agronomía)

4. **El ciclo de vida de un proyecto DS**
   - 6 pasos: Definir problema → Recopilar → Limpiar → Modelar → Comunicar → Desplegar
   - Diagrama circular con cada etapa
   - Ejemplo de caso real: "¿Por qué este cliente va a abandonar el servicio?"

5. **Herramientas del Bootcamp**
   - Python, pandas, matplotlib, scikit-learn, XGBoost
   - Google Colab como entorno de trabajo

6. **¿Por qué Python?**
   - Simplicidad de sintaxis vs Java/C++
   - Popularidad en DS (Stack Overflow survey)
   - Ecosistema de librerías

7. **Google Colaboratory — ¿Qué es?**
   - Jupyter en la nube
   - Sin instalación, GPU gratuita, fácil de compartir
   - Comparación: Colab vs Jupyter local vs VS Code

8. **Tour por la interfaz de Colab**
   - Tipos de celdas: código vs texto (Markdown)
   - Barra de herramientas
   - Cómo guardar en Drive

9. **Atajos de teclado esenciales**
   - Tabla con los 6 atajos más usados
   - Shift+Enter, Ctrl+M B, Ctrl+M M, etc.

10. **🔹 Actividad 0 — Mi primer notebook**
    - Paso a paso: crear notebook, escribir `print("¡Hola Data Science!")`, agregar celda de texto

---

## Clase 2 — Variables y Tipos de Datos

**Duración estimada:** 1.5–2 horas

**Objetivos de aprendizaje:**
- Declarar y usar variables en Python
- Conocer los tipos de datos básicos y convertir entre ellos
- Aplicar operadores aritméticos

**Contenido de los slides:**

1. **Portada de la clase**
   - Título: "Variables y Tipos de Datos"
   - Analogía visual: variable como una "caja con etiqueta"

2. **¿Qué es una variable?**
   - Definición: almacena un valor, le asigna un nombre
   - Sintaxis: `nombre = valor`
   - Reglas de nombres (válidos e inválidos)
   - Ejemplo con 4 variables: nombre, edad, altura, es_estudiante

3. **Tipos de datos básicos**
   - Tabla: `int`, `float`, `str`, `bool` con ejemplos
   - `type()` para identificar el tipo
   - Por qué importa el tipo (no se puede sumar str + int)

4. **Números: int y float**
   - Diferencia entre `7` y `7.0`
   - Ejemplos: edad vs precio, año vs temperatura

5. **Strings**
   - Comillas simples vs dobles (ambas válidas)
   - Concatenación con `+`
   - Multiplicación: `"ha" * 3 → "hahaha"`

6. **Booleanos**
   - Solo dos valores: `True` / `False`
   - Resultan de comparaciones
   - Truthy / Falsy: `0`, `""`, `None` son falsy

7. **Conversión de tipos (Casting)**
   - `int()`, `float()`, `str()`, `bool()`
   - Cuándo usar cada uno
   - Error común: `"tengo" + 25 + " años"` → solución

8. **Operadores Aritméticos**
   - Tabla completa: `+`, `-`, `*`, `/`, `//`, `%`, `**`
   - Énfasis en `//` (división entera) y `%` (módulo)
   - Orden de precedencia: PEMDAS

9. **🔹 Mini-ejercicio 1 — Calculadora de IMC**
   - Enunciado: calcular IMC con peso=70, altura=1.75
   - Fórmula: `IMC = peso / altura²`
   - Imprimir resultado con 2 decimales usando f-string

---

## Clase 3 — Estructuras de Datos y Entrada/Salida

**Duración estimada:** 1.5–2 horas

**Objetivos de aprendizaje:**
- Manejar listas y diccionarios para agrupar datos
- Usar print() con distintos formatos (especialmente f-strings)
- Capturar input del usuario

**Contenido de los slides:**

1. **Portada de la clase**
   - Título: "Estructuras de Datos y I/O"

2. **Tipos de datos compuestos — visión general**
   - Tabla comparativa: `list`, `tuple`, `dict`, `set`
   - Cuándo usar cada uno

3. **Listas**
   - Definición: colección ordenada y mutable
   - Indexing: `lista[0]`, `lista[-1]`
   - Slicing: `lista[1:3]`, `lista[::2]`
   - Métodos: `append()`, `insert()`, `remove()`, `sort()`, `len()`

4. **Indexing visual**
   - Diagrama de una lista con índices positivos y negativos
   - Ejemplo animado: `frutas = ["manzana", "pera", "uva", "kiwi", "mango"]`

5. **Diccionarios**
   - Definición: pares llave → valor
   - Acceso: `dict["llave"]`
   - Agregar y modificar: `dict["nueva"] = valor`
   - Iterar con `.items()`, `.keys()`, `.values()`

6. **Strings — métodos útiles**
   - `.strip()`, `.lower()`, `.upper()`, `.replace()`, `.split()`
   - `.startswith()`, `.endswith()`, `in` para pertenencia
   - Caso de uso: limpiar datos de texto (anticipar pandas)

7. **Salida: print() en profundidad**
   - 4 formas de formatear: concatenación, comas, `%`, f-strings
   - Recomendar f-strings como estándar
   - Parámetros: `sep=`, `end=`

8. **Entrada: input()**
   - Siempre retorna string
   - Conversión obligatoria para números
   - Patrón `try/except` básico para validar (preview)

9. **🔹 Mini-ejercicio 2 — Mini-agenda**
   - Crear diccionario con 3 contactos
   - Imprimir con formato: `📞 Nombre: xxx-xxxx`

---

## Clase 4 — Lógica, Condicionales y Estructuras de Control

**Duración estimada:** 2 horas (incluye actividad final)

**Objetivos de aprendizaje:**
- Usar operadores lógicos y de comparación
- Construir flujos condicionales con if/elif/else
- Iterar con for y while
- Integrar todo en un programa completo

**Contenido de los slides:**

1. **Portada de la clase**
   - Título: "Lógica y Control de Flujo"

2. **Operadores de comparación**
   - Tabla: `==`, `!=`, `>`, `<`, `>=`, `<=`
   - Diferencia entre `=` (asignación) y `==` (comparación)
   - Todos retornan `bool`

3. **Operadores lógicos**
   - `and`, `or`, `not`
   - Tabla de verdad visual
   - Ejemplo: validar rango `x > 0 and x < 100`

4. **Condicional if / elif / else**
   - Diagrama de flujo
   - Sintaxis con indentación obligatoria (4 espacios)
   - Ejemplo: clasificar nota (Aprobado / Recuperación / Reprobado)

5. **Indentación en Python**
   - Por qué importa (define bloques, no las llaves `{}`)
   - Error común: `IndentationError`
   - Colab marca la indentación automáticamente

6. **🔹 Mini-ejercicio 3 — Clasificador de IMC**
   - Usar el IMC de clase 2 y clasificarlo con if/elif/else

7. **Estructura for**
   - Diagrama de flujo
   - Iterar sobre lista, string, range
   - `enumerate()` para índice + valor

8. **Estructura while**
   - Diferencia con for: condición vs cantidad fija
   - Riesgo del bucle infinito → siempre actualizar la variable de control
   - `break` y `continue`

9. **List Comprehensions (bonus)**
   - Forma compacta de crear listas
   - Comparación con for tradicional
   - Con y sin filtro

10. **🏁 Actividad Final — Analizador de notas**
    - Enunciado completo (ver notebook)
    - Integra: input, listas, for, while, if/elif/else, f-strings
    - Trabajo individual con apoyo del instructor

---

## Notas para el diseñador de slides

- **Colores:** usar paleta oscura tipo dark-mode (fondo `#1e1e2e`, texto claro) — es más cómoda para leer código
- **Fuente código:** `JetBrains Mono` o `Fira Code` para todos los snippets
- **Tamaño de fuente:** nunca menos de 18pt en el cuerpo, 14pt en código
- **Por slide:** máximo 5–7 bullets o un bloque de código de 10–15 líneas
- **Cada clase comienza** con una slide de agenda de la clase y **termina** con un resumen de lo aprendido
- **Insertar checkpoints** de comprensión: preguntas tipo "¿qué imprime este código?" antes de cada mini-ejercicio
- **Separadores entre clases:** slide de portada con número y título de clase
- **Total estimado:** ~40–50 slides para las 4 clases
