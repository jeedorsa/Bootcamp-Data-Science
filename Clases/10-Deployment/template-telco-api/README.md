# Telco Churn API — Template de Deployment

Este template tiene todo lo necesario para que ustedes deployen su propia API de predicción de churn a Azure Container Apps en menos de 10 minutos.

El modelo es el XGBoost de Telco Customer Churn que vimos en la semana 8 (ejercicio 8.3).

---

## Estructura

```
template-telco-api/
├── app/
│   ├── main.py          # FastAPI con endpoints /predict y /batch
│   ├── model.joblib     # Modelo XGBoost pre-entrenado (462 KB)
│   └── schema.json      # Schema de las features esperadas
├── Dockerfile           # Imagen Docker lista
├── requirements.txt     # Dependencias Python
├── deploy.sh            # Script con los 6 comandos de Azure
├── test_api.py          # Cliente para probar el endpoint
└── README.md            # Este archivo
```

---

## Paso 1: Prerequisitos (instalar UNA vez)

### En su computadora:
- **Azure CLI**: `brew install azure-cli` (Mac) o `winget install Microsoft.AzureCLI` (Windows)
- **Python 3.10+**: para correr `test_api.py` desde su máquina
- **Docker** (opcional): solo si quieren buildear local en vez de en Azure

### Cuenta de Azure:
- Una cuenta activa (Azure for Students gratis con $100 USD funciona perfecto)
- Una suscripción habilitada

```bash
# Login a Azure desde la terminal
az login

# Confirmar que están en la suscripción correcta
az account show
```

---

## Paso 2: Correr la app LOCALMENTE (recomendado antes del deploy)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Levantar la app con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. En otro terminal, probar
python test_api.py
# o abrir http://localhost:8000/docs en el navegador (Swagger UI automática)
```

Si funciona local, va a funcionar en Azure.

---

## Paso 3: Deploy a Azure Container Apps

### Editar `deploy.sh`:

Abran `deploy.sh` y cambien la variable `TU_NOMBRE` por su nombre sin espacios ni mayúsculas:

```bash
TU_NOMBRE="ivan"   # ejemplo
```

### Ejecutar el deploy:

```bash
bash deploy.sh
```

El script hace estos 6 pasos automáticamente:

1. Crea un Resource Group
2. Crea un Container Registry (donde vive su imagen Docker)
3. Buildea la imagen Docker EN EL CLOUD (no necesitan Docker local)
4. Crea un Container Apps Environment
5. Deploya la Container App con la imagen
6. Devuelve la URL pública

**Tarda entre 5 y 8 minutos**. Al final les imprime algo como:

```
Tu API esta corriendo en:
  https://telco-api-ivan.eastus.azurecontainerapps.io

Endpoints:
  https://telco-api-ivan.eastus.azurecontainerapps.io/         (health)
  https://telco-api-ivan.eastus.azurecontainerapps.io/docs     (Swagger UI)
  https://telco-api-ivan.eastus.azurecontainerapps.io/predict  (POST)
```

---

## Paso 4: Probar el endpoint deployado

```bash
# Probar desde la terminal
python test_api.py https://telco-api-ivan.eastus.azurecontainerapps.io

# O abrir en el navegador
open https://telco-api-ivan.eastus.azurecontainerapps.io/docs
```

Pueden usar Swagger UI directamente desde el navegador para mandar requests sin escribir código.

### Pega un ejemplo en /docs:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure": 2,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "Yes",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 95.5,
  "TotalCharges": 195.0
}
```

Respuesta esperada:

```json
{
  "probabilidad_churn": 0.8095,
  "decision": "RIESGO ALTO",
  "recomendacion": "Cliente con muy alta probabilidad de churn. Priorizar campaña de retención con descuento.",
  "timestamp": "2026-06-15T17:23:45.123Z"
}
```

---

## Paso 5: Compartir su API

Su API es **pública**. Pueden:
- Compartirla en LinkedIn como demo de su portfolio
- Llamarla desde una app web
- Conectarla con Zapier, n8n, Make, etc.
- Integrarla con Power BI o Tableau como fuente

---

## Limpieza al terminar la clase (IMPORTANTE)

Para no acumular costos en Azure, **borren todo después** de la clase:

```bash
# Reemplazar TU_NOMBRE por el suyo
az group delete --name rg-telco-TU_NOMBRE --yes --no-wait
```

Esto borra absolutamente todo (Resource Group + Container Registry + Container App + logs) en ~2 minutos.

---

## Personalizar (después de clase)

¿Quieren deployar SU PROPIO modelo en vez del de Telco?

1. **Entrenar y serializar su modelo** como Pipeline de sklearn:
   ```python
   import joblib
   joblib.dump(mi_pipeline, "app/model.joblib")
   ```

2. **Editar `app/main.py`**:
   - Cambiar el schema de Pydantic en `class Cliente`
   - Ajustar `transformar_input` si tienen mapeos manuales
   - Ajustar `interpretar` con sus reglas de decisión

3. **Re-deploy**:
   ```bash
   bash deploy.sh
   ```

El template les ahorra el setup inicial. El código de la API en sí son ~150 líneas, fáciles de adaptar.

---

## Troubleshooting

### "az: command not found"
No tienen Azure CLI instalado. Instalen con `brew install azure-cli` (Mac) o equivalente.

### "Authentication failed"
No están logueados. Corran `az login` primero.

### El deploy falla en el paso 3 (build)
Verifiquen que están en la carpeta `template-telco-api/` cuando ejecutan `bash deploy.sh`. Tiene que ver el `Dockerfile` en el directorio actual.

### El deploy completa pero la URL devuelve 404
Esperen 1-2 minutos. La app tarda en arrancar la primera vez (descarga la imagen + carga el modelo en memoria).

### "Quota exceeded" en Container Apps
Su región no tiene cuota suficiente. Cambien `LOCATION="eastus"` en `deploy.sh` a otra región como `westus2`, `brazilsouth`, o `northeurope`.

---

## Costos estimados

Con la configuración del template (0.5 vCPU, 1 GB RAM, scale to zero):
- **Tráfico bajo (clase + portfolio)**: ~$0 a $1 USD/mes
- **Tráfico moderado (cientos de requests/día)**: ~$5 USD/mes
- **Tráfico alto**: depende, pero hay alertas configurables

Con `min-replicas 0` (el default del template), la app se apaga cuando no hay tráfico y vuelve a arrancar en 5-10 segundos cuando llega un request. Esto reduce el costo a centavos.

---

## Siguiente paso: Ollama local

Después de esta clase vamos a ver cómo correr un LLM (Llama 3 8B) **localmente sin gastar tokens**. Ver carpeta `../ollama-demo/`.
