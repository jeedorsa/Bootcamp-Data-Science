# Ollama local + Gateway FastAPI

Su propio "ChatGPT" corriendo en su máquina, **sin gastar tokens**.

---

## Por qué hacer esto

| | Ollama local | API OpenAI/Anthropic |
|---|---|---|
| Costo | Gratis (después del setup) | $0.50 a $15 USD por 1M tokens |
| Latencia | 50-200ms (sin red) | 200-1000ms |
| Privacidad | 100% local | Datos pasan por sus servidores |
| Tamaño modelo | 8B-70B parámetros | 100B+ |
| Calidad | Buena para tareas simples | Excelente |
| Setup | 30 min primera vez | Solo API key |

**Cuándo elegir Ollama local:**
- Pruebas de prompt engineering antes de gastar plata
- Datos sensibles que no pueden salir de la red de la empresa
- Apps con alto volumen donde el costo de API se dispara
- Edge computing (correr LLM en una VM sin internet)

**Cuándo elegir API externa:**
- Necesitan la mejor calidad disponible
- Casos puntuales de baja frecuencia
- No tienen hardware con GPU/RAM suficiente

---

## Requisitos del hardware

- **RAM**: mínimo 16 GB (Ollama necesita ~8 GB libres para Llama 3 8B)
- **Disco**: ~5 GB libres por modelo descargado
- **CPU**: cualquiera moderna (Apple Silicon es muy rápido)
- **GPU**: opcional, acelera mucho si tienen una NVIDIA con 8+ GB VRAM

---

## Opción A: Correr Ollama directo en su máquina (más simple)

### Paso 1: Instalar Ollama

```bash
# Mac
brew install ollama

# Windows
# Bajar de https://ollama.com/download/windows

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### Paso 2: Arrancar Ollama y descargar un modelo

```bash
# Arrancar el servidor en background
ollama serve &

# Descargar Llama 3 8B (~5 GB, tarda 5-10 min)
ollama pull llama3

# Probar
ollama run llama3 "Hola, quien eres?"
```

### Paso 3: Llamar desde Python

```python
import requests

r = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3",
    "prompt": "Explica que es un endpoint REST en 3 lineas",
    "stream": False
})
print(r.json()["response"])
```

---

## Opción B: Correr Ollama + Gateway con Docker Compose

Si quieren tenerlo bien organizado y reproducible:

### Paso 1: Instalar Docker Desktop

- Mac: https://docs.docker.com/desktop/install/mac-install/
- Windows: https://docs.docker.com/desktop/install/windows-install/

### Paso 2: Levantar todo

```bash
# Desde la carpeta ollama-demo/
docker-compose up -d

# Ver los logs
docker-compose logs -f ollama
```

### Paso 3: Descargar el modelo dentro del container

```bash
docker exec -it ollama ollama pull llama3
```

### Paso 4: Probar el gateway

```bash
# Health check
curl http://localhost:8001/

# Chat simple
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explica que es FastAPI en 3 lineas", "max_tokens": 200}'

# Endpoint integrado con Telco Churn (envia datos del cliente, devuelve resumen ejecutivo)
curl -X POST http://localhost:8001/resumir-cliente \
  -H "Content-Type: application/json" \
  -d '{"tenure": 2, "contrato": "Month-to-month", "pago": "Electronic check", "monto": 95.5, "probabilidad_churn": 0.81}'
```

### Paso 5: Apagar todo cuando terminen

```bash
docker-compose down
```

---

## Modelos recomendados para tareas comunes

```bash
# Chat general (8 GB RAM)
ollama pull llama3

# Más liviano, más rapido (4 GB RAM)
ollama pull llama3.2:3b

# Mejor en español
ollama pull qwen2.5:7b

# Programación (8 GB RAM)
ollama pull codellama

# Modelo multimodal (acepta imágenes)
ollama pull llava
```

---

## Integración con la API de Telco Churn

Pueden combinar AMBAS APIs:

1. **Cliente llama a Telco API** → recibe probabilidad de churn
2. **Cliente llama a Ollama Gateway con esa data** → recibe resumen ejecutivo en lenguaje natural

```python
import requests

# 1. Llamada al modelo de churn
cliente = {"gender": "Female", "tenure": 2, ...}
churn_resp = requests.post("https://telco-api-bootcamp.eastus.azurecontainerapps.io/predict", json=cliente).json()

# 2. Pedirle al LLM que genere un resumen ejecutivo
prompt = f"""Cliente con probabilidad de churn = {churn_resp['probabilidad_churn']*100:.1f}%.
Datos: tenure {cliente['tenure']} meses, contrato {cliente['Contract']}.
Generar resumen ejecutivo de 3 lineas con accion comercial recomendada."""

llm_resp = requests.post("http://localhost:8001/chat", json={"prompt": prompt}).json()
print(llm_resp["response"])
```

Esa es la combinación moderna: **modelo de ML clásico para la predicción + LLM para la explicación en lenguaje natural**. Lo que están haciendo bancos, telcos y retailers en producción.

---

## Costo comparado (números reales)

Para el caso de generar 10,000 resúmenes ejecutivos al mes:

| Solución | Costo mensual |
|---|---|
| GPT-4o API | ~$30 USD |
| Claude Sonnet API | ~$15 USD |
| Llama 3 8B en VM Azure D4s_v3 | ~$140 USD (VM 24/7) |
| **Llama 3 8B en su laptop** | **$0 USD** |

El break-even es alrededor de los 5,000-10,000 requests/mes. Por debajo de eso, conviene API. Por encima, conviene self-hosted.
