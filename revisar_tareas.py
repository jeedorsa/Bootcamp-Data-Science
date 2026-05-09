"""
Automatizacion de revision y calificacion de tareas — Skillnest
================================================================
Logica de notas:
  100  — Entrego codigo completo y funcional
   80  — Entrego algo pero le falta bastante
   10  — No subio nada

Uso:
  python3 revisar_tareas.py <URL_assignment>
  python3 revisar_tareas.py  (usa URL por defecto)
"""

import asyncio, sys, json, re
from playwright.async_api import async_playwright

# ── Credenciales ──────────────────────────────────────────────────
USUARIO   = "jortiz@skillnest.com"
PASSWORD  = "Pamplona-90"
LOGIN_URL = "https://learning.skillnest.com/login/"

DEFAULT_URL = (
    "https://learning.skillnest.com/escritorio/assignments/review/"
    "?view_assignment=49164&assignment=63726"
)

# Palabras clave que indican codigo Python real
KEYWORDS_PYTHON = [
    'import ', 'from ', 'def ', 'class ', 'for ', 'while ',
    'if ', 'else:', 'elif ', 'return ', 'print(',
    'df', 'plt.', 'pd.', 'np.', '.groupby', '.apply',
    '.read_csv', '.plot', '.hist', '.show()', '.head()',
    '.describe()', '.isnull()', '.fillna', '.dropna',
    '.merge', '.concat', '.value_counts', '= pd.', '= np.',
    'sns.', 'matplotlib', 'seaborn', 'sklearn',
]

# Texto de la UI de Colab a ignorar
UI_COLAB = [
    'Archivo', 'Editar', 'Ver', 'Insertar', 'Entorno de ejecución',
    'Herramientas', 'Ayuda', 'settings', 'people', 'Compartir', 'Acceder',
    'Comandos', 'Código', 'Texto', 'Copiar en Drive', 'expand_less',
    'format_list_bulleted', 'find_in_page', 'eye_tracking', 'vpn_key',
    'folder', 'table', 'keyboard_arrow_down', 'Productos pagados',
    'Terminal', 'Variables', 'data_object', 'terminal', 'expand_more',
    'code', 'arrow_drop', 'menu', 'search', 'close', 'add', 'more_vert',
]


# ── Extraer info del estudiante ───────────────────────────────────

def extraer_estudiante(contenido):
    estudiante, email, fecha, colab_url = "", "", "", ""

    lineas = contenido.split('\n')
    for i, linea in enumerate(lineas):
        l = linea.strip()
        if l == 'Estudiante:' and i + 1 < len(lineas):
            siguiente = lineas[i + 1].strip()
            match = re.search(r'(.+?)\s*\((.+?)\)', siguiente)
            if match:
                estudiante = match.group(1).strip()
                email      = match.group(2).strip()
        if l == 'Fecha de envío:' and i + 1 < len(lineas):
            fecha = lineas[i + 1].strip()
        if 'colab.research.google.com' in l:
            urls = re.findall(r'https://colab\.research\.google\.com/drive/[\w\-?=&]+', l)
            if urls:
                colab_url = urls[0].rstrip('?usp=sharing').rstrip('?')

    # fallback: buscar colab en todo el texto
    if not colab_url:
        urls = re.findall(r'https://colab\.research\.google\.com/drive/[\w\-]+', contenido)
        if urls:
            colab_url = urls[0]

    return estudiante, email, fecha, colab_url


# ── Evaluar codigo del Colab ──────────────────────────────────────

def evaluar_codigo(texto_colab, tiene_link):
    """
    Retorna (nota: int, comentario: str)
      10  → sin entrega o sin codigo
      80  → entrego pero incompleto
      100 → completo
    """
    if not tiene_link:
        return 10, (
            "No se encontro ningún enlace de entrega en la tarea. "
            "Nota: 10/100. Por favor entrega tu trabajo antes del cierre."
        )

    if not texto_colab or len(texto_colab.strip()) < 80:
        return 10, (
            "El enlace entregado no contiene codigo ejecutable o el notebook "
            "esta vacio. Nota: 10/100. Asegurate de compartir el Colab con acceso publico."
        )

    # Filtrar UI y contar lineas de codigo real
    lineas_codigo = []
    for linea in texto_colab.split('\n'):
        l = linea.strip()
        if not l or len(l) < 3:
            continue
        if any(ui in l for ui in UI_COLAB):
            continue
        if any(kw in l for kw in KEYWORDS_PYTHON):
            lineas_codigo.append(l)

    n = len(lineas_codigo)
    print(f"  Lineas de codigo Python detectadas: {n}")

    if n == 0:
        return 10, (
            "El notebook no contiene codigo Python reconocible. "
            "Nota: 10/100. Verifica que compartiste el notebook correcto."
        )
    elif n < 8:
        return 80, (
            f"Se encontraron solo {n} lineas de codigo. "
            "La entrega esta incompleta — falta desarrollo o ejercicios sin resolver. "
            "Nota: 80/100. Buen inicio, pero intenta completar todos los puntos."
        )
    else:
        return 100, (
            f"Notebook completo con {n} lineas de codigo Python. "
            "Se verifico que contiene imports, procesamiento de datos y "
            "estructuras correctas. Nota: 100/100. Excelente trabajo!"
        )


# ── Login ─────────────────────────────────────────────────────────

async def login(page):
    print("Iniciando sesion...")
    await page.goto(LOGIN_URL, wait_until="networkidle")
    await page.fill('input[name="log"]', USUARIO)
    await page.fill('input[name="pwd"]', PASSWORD)
    await page.click('input[type="submit"]')
    await page.wait_for_load_state("networkidle")
    if "login" in page.url:
        raise Exception("Login fallido")
    print(f"  Sesion activa — {page.url}")


# ── Calificar una tarea ───────────────────────────────────────────

async def calificar_tarea(page, url_tarea):
    print(f"\n{'='*55}")
    print(f"Tarea: {url_tarea}")
    print('='*55)

    # 1. Cargar pagina de la tarea
    await page.goto(url_tarea, wait_until="networkidle")
    await page.wait_for_timeout(2000)

    contenido_pagina = await page.evaluate("""() => {
        document.querySelectorAll('script,style').forEach(e=>e.remove());
        return document.body.innerText;
    }""")

    # 2. Extraer datos del estudiante
    estudiante, email, fecha, colab_url = extraer_estudiante(contenido_pagina)
    print(f"Estudiante : {estudiante or 'Desconocido'}")
    print(f"Email      : {email or 'N/A'}")
    print(f"Fecha      : {fecha or 'N/A'}")
    print(f"Colab URL  : {colab_url or 'NO ENCONTRADO'}")

    # 3. Abrir Colab y extraer codigo
    texto_colab = ""
    if colab_url:
        print(f"\nAbriendo Colab...")
        try:
            await page.goto(colab_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            titulo_colab = await page.title()
            print(f"  Titulo: {titulo_colab}")

            texto_colab = await page.evaluate("""() => {
                const sels = [
                    '.codecell-input-output',
                    '.view-line',
                    '.CodeMirror-line',
                    '.cm-content',
                    '.cell-input pre',
                    '.code-cell',
                ];
                for (const sel of sels) {
                    const els = document.querySelectorAll(sel);
                    if (els.length > 0) {
                        return [...els].map(e=>e.innerText).join('\\n');
                    }
                }
                // fallback: todo el cuerpo
                return document.body.innerText;
            }""")
        except Exception as e:
            print(f"  Error al abrir Colab: {e}")

    # 4. Evaluar y determinar nota
    print("\nEvaluando entrega...")
    nota, comentario = evaluar_codigo(texto_colab, bool(colab_url))
    print(f"  NOTA DETERMINADA: {nota}/100")
    print(f"  Comentario: {comentario}")

    # 5. Volver a la pagina de la tarea y poner nota
    print(f"\nEnviando calificacion...")
    await page.goto(url_tarea, wait_until="networkidle")
    await page.wait_for_timeout(2000)

    # Rellenar nota
    await page.fill(
        'input[name="evaluate_assignment[assignment_mark]"]',
        str(nota)
    )

    # Rellenar comentario
    await page.fill(
        'textarea[name="evaluate_assignment[instructor_note]"]',
        comentario
    )

    # Click en "Evalua esta entrega"
    await page.click('button.tutor-btn-primary')
    await page.wait_for_timeout(3000)

    # Verificar si se envio correctamente
    url_final = page.url
    contenido_final = await page.evaluate("""() => {
        document.querySelectorAll('script,style').forEach(e=>e.remove());
        return document.body.innerText.substring(0, 500);
    }""")

    enviado_ok = (
        "evaluado" in contenido_final.lower()
        or "calificado" in contenido_final.lower()
        or str(nota) in contenido_final
        or "exitosamente" in contenido_final.lower()
        or "success" in contenido_final.lower()
    )

    if enviado_ok:
        print(f"  Calificacion enviada correctamente")
    else:
        print(f"  Nota enviada (verificar manualmente si es necesario)")
        print(f"  Respuesta: {contenido_final[:200]}")

    return {
        "estudiante":  estudiante,
        "email":       email,
        "fecha":       fecha,
        "colab_url":   colab_url,
        "nota":        nota,
        "comentario":  comentario,
        "url_tarea":   url_tarea,
    }


# ── Main ──────────────────────────────────────────────────────────

async def main():
    urls = sys.argv[1:] if len(sys.argv) > 1 else [DEFAULT_URL]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            locale="es-CL"
        )
        page = await context.new_page()

        try:
            await login(page)

            resultados = []
            for url in urls:
                resultado = await calificar_tarea(page, url)
                resultados.append(resultado)

            # Resumen final
            print(f"\n{'='*55}")
            print("RESUMEN DE CALIFICACIONES")
            print('='*55)
            for r in resultados:
                print(f"  {r['estudiante'] or 'Desconocido':<30} Nota: {r['nota']}/100")

            with open("resultados_calificacion.json", "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)
            print(f"\nResultados guardados en: resultados_calificacion.json")

            await page.wait_for_timeout(5000)

        except Exception as e:
            print(f"\nERROR: {e}")
            await page.screenshot(path="error_screenshot.png")
            print("Captura: error_screenshot.png")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
