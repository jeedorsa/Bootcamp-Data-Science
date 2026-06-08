# Presentación de proyectos — Formato VC Pitch

**Bootcamp Data Science · Módulo 2 · Semana 8**
**Instructor:** Jesús Ortiz · SkillNest
**Fechas:** Jueves 11 y Viernes 12 de junio de 2026

---

## El formato

Cada estudiante presenta su proyecto en **formato pitch tipo Venture Capital**.

- **3 minutos** de presentación. Se corta a los 3 minutos exactos.
- **5 minutos** de preguntas y discusión con el panel.
- Total por estudiante: **8 minutos** (más 2 de transición = 10 min por slot).

## Qué NO se evalúa

- **No mostrar resultados de modelos.** Esto NO es una entrega final de proyecto.
- No es un demo de código ni de notebooks.
- No se penaliza si no tienen el modelo entrenado.

## Qué SÍ se evalúa

Esto es una **defensa de propuesta**. Los criterios son los mismos que usaría un fondo de inversión cuando le presentan una idea:

1. **¿Es un problema real que vale la pena resolver?**
2. **¿Entienden el dataset y sus limitaciones?**
3. **¿Tienen un plan técnico realista?**
4. **¿Saben defender su idea bajo presión?**

---

## Rúbrica detallada (escala 1-5 por criterio)

### 1. Problema y motivación (20 pts)

| Pts | Descripción |
|---|---|
| 5 | Problema claramente definido, relevante para una industria identificada, con stakeholders claros y un \"así qué\" potente |
| 4 | Problema bien definido pero relevancia o stakeholders no del todo claros |
| 3 | Problema definido pero suena académico o sin urgencia real |
| 2 | Problema vago, cuesta entender qué se quiere resolver |
| 1 | No queda claro qué problema están atacando |

### 2. Dataset y exploración inicial (20 pts)

| Pts | Descripción |
|---|---|
| 5 | Dataset bien identificado con fuente, tamaño y estructura. Muestran ejemplos de filas. Mencionan limitaciones obvias (sesgo, calidad, completitud) |
| 4 | Dataset identificado pero falta algún detalle relevante (tamaño, fuente o limitaciones) |
| 3 | Dataset mencionado pero sin profundidad ni reconocimiento de limitaciones |
| 2 | Dataset vago, no queda claro qué van a usar |
| 1 | No hay claridad sobre los datos disponibles |

### 3. Plan técnico (20 pts)

| Pts | Descripción |
|---|---|
| 5 | Plan paso a paso realista: limpieza, EDA, modelos a probar, métricas correctas para el problema, criterios de éxito numéricos. Justifican las decisiones técnicas |
| 4 | Plan claro pero falta justificar algunas decisiones técnicas |
| 3 | Plan general pero sin detalles concretos. Métricas mencionadas sin justificación |
| 2 | Plan superficial, parece improvisado |
| 1 | Sin plan claro o plan poco realista |

### 4. Identificación de desafíos (15 pts)

| Pts | Descripción |
|---|---|
| 5 | Identifican 3+ desafíos concretos (técnicos, de datos o de negocio) y proponen mitigaciones realistas para cada uno |
| 4 | Identifican 2 desafíos con mitigaciones |
| 3 | Mencionan algún desafío pero sin proponer mitigación |
| 2 | Reconocen vagamente que habrá problemas |
| 1 | No reconocen ningún desafío (señal de inexperiencia) |

### 5. Comunicación y manejo del tiempo (15 pts)

| Pts | Descripción |
|---|---|
| 5 | Presentación clara, fluida, dentro del tiempo. Apoyos visuales útiles. Lenguaje accesible sin perder rigor técnico |
| 4 | Presentación clara y dentro del tiempo, alguna sección menos lograda |
| 3 | Se entiende la idea pero le falta pulido. Se pasa o queda corto del tiempo por más de 30 segundos |
| 2 | Presentación confusa o muy desordenada |
| 1 | Improvisada, no se entiende qué proponen |

### 6. Defensa en preguntas y respuestas (10 pts)

| Pts | Descripción |
|---|---|
| 5 | Responde con seguridad, reconoce lo que no sabe, propone caminos para resolver dudas |
| 4 | Responde bien la mayoría, una respuesta dudosa |
| 3 | Responde con dudas, algunas respuestas evasivas |
| 2 | Le cuesta defender la idea, varias respuestas vagas |
| 1 | No logra responder o las respuestas son contradictorias |

### Total: 100 puntos

---

## Estructura sugerida para los 3 minutos de pitch

Si presentan en este orden les va a salir mejor:

1. **30 segundos — El problema**
   - ¿Qué problema están resolviendo?
   - ¿Quién lo sufre? ¿Por qué importa?
   - Una frase tipo "tal industria pierde X millones por Y razón"

2. **30 segundos — La data**
   - ¿Qué dataset van a usar?
   - ¿Cuántas filas, cuántas features, de qué fuente?
   - ¿Qué limitaciones tiene?

3. **60 segundos — El plan**
   - ¿Qué tipo de problema es? (regresión, clasificación, etc.)
   - ¿Qué modelos van a probar? ¿Por qué esos?
   - ¿Qué métrica van a optimizar y por qué esa?
   - ¿Cómo van a validar (train/test, CV, etc.)?

4. **30 segundos — Los desafíos**
   - 3 cosas que les preocupan y cómo las van a manejar
   - Por ejemplo: clases desbalanceadas, nulos, features categóricas con alta cardinalidad

5. **30 segundos — El cierre**
   - ¿Qué entregarán?
   - ¿Qué éxito se vería como?

---

## Preguntas tipo que voy a hacer en el Q&A

Para que se preparen, estas son las preguntas más probables:

- ¿Por qué eligieron ESE dataset y no otro similar?
- ¿Qué pasa si el dataset está sucio o le faltan muchas filas?
- ¿Por qué van a optimizar esa métrica y no otra? Por ejemplo accuracy vs F1.
- Si el resultado del modelo es malo, ¿qué harán?
- ¿Cómo saben que el problema vale la pena resolverlo automáticamente vs hacerlo manual?
- ¿Quién va a usar esto en la vida real?
- ¿Cómo van a manejar las clases desbalanceadas si las hay?
- ¿Por qué empezarían por X modelo y no por Y?
- ¿Cuánto se demorarían en entrenar el modelo final con el dataset completo?
- ¿Qué harían si el modelo termina sobre-prediciendo una clase?
- ¿Cómo van a validar que el modelo funciona bien sin overfitear?
- ¿Han pensado en cómo se desplegaría esto en producción?

---

## Lo que SÍ recomiendo llevar

- 3-5 slides como máximo (ojalá menos).
- Una imagen del dataset (un `df.head()` cuenta).
- Una idea visual del flujo del proyecto (no necesita ser bonito, claro basta).
- Un slide con los desafíos identificados.

## Lo que NO recomiendo llevar

- Demos de código en vivo (no hay tiempo).
- Resultados del modelo (no es lo que se evalúa).
- Slides con mucho texto (los van a leer y se distraen).
- Animaciones.

---

## Calendario de presentaciones

Para reservar su slot vamos a usar **Calendly** (la herramienta de agendamiento que mejor se adapta a este caso).

### Horarios disponibles

**Jueves 11 de junio:**
- Bloque 1: 18:15 — 19:15 (6 slots de 10 min)
- Pausa: 19:15 — 19:30
- Bloque 2: 19:30 — 21:00 (9 slots de 10 min)
- Pausa: 21:00 — 21:15
- Bloque 3: 21:15 — 22:00 (4-5 slots de 10 min según necesidad)

**Viernes 12 de junio:**
- Mismo formato, si quedan estudiantes por presentar

Total disponible por día: ~19 slots. Suficiente para los 22 estudiantes.

### Link de Calendly (a configurar por el instructor)

`https://calendly.com/jesus-ortiz-skillnest/presentacion-proyecto-final`

Cuando vayan a reservar:
- Eligen un slot disponible.
- Confirman su nombre y correo.
- Reciben confirmación por mail y un Google Calendar invite.
- Si necesitan cambiar, lo hacen desde el mismo link sin pedir permiso (siempre que haya slots libres).

---

## Reglas del juego

1. **Llegar 5 minutos antes** del slot reservado.
2. **No exceder los 3 minutos de pitch.** Se les avisa a los 2:30 y se les corta a los 3:00.
3. Si se enferman o tienen emergencia, **avisar por mail con 12 horas de anticipación** mínimo para reagendar.
4. La nota se entrega el mismo día por correo.
5. Esta presentación pesa **30% de la nota final del módulo**.

---

## Una recomendación final

No pierdan tiempo intentando que el pitch sea perfecto. **Lo que más valoran los inversores es la claridad y la honestidad sobre los desafíos**, no la perfección. Si saben qué problema están resolviendo, por qué importa y cómo lo van a abordar de forma realista, ya tienen la mitad de la nota asegurada.

El otro 50% es saber defenderlo bajo preguntas. Para eso practiquen el pitch en voz alta con un compañero antes y pídanle que les haga preguntas difíciles.

Buena suerte.

Jesús Ortiz
SkillNest
