"""
Telco Customer Churn — API de prediccion en FastAPI
====================================================

Endpoints:
- GET  /          health check
- GET  /docs      Swagger UI automatica (generada por FastAPI)
- POST /predict   predice probabilidad de churn para un cliente
- POST /batch     predice para una lista de clientes

Para correr localmente:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Despues abrir http://localhost:8000/docs en el navegador.
"""

from datetime import datetime
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Carga el modelo al iniciar (no en cada request)
MODEL_PATH = Path(__file__).parent / "model.joblib"
modelo = joblib.load(MODEL_PATH)


# ── Schema del input ──────────────────────────────────────────────
# Pydantic valida el tipo y formato de cada campo automaticamente.
class Cliente(BaseModel):
    # Demograficos
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0, 1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]

    # Contrato y servicios
    tenure: int = Field(..., ge=0, le=100, description="Meses con el servicio")
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal[
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ]

    # Cargos
    MonthlyCharges: float = Field(..., ge=0, le=500)
    TotalCharges: float = Field(..., ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "gender": "Female", "SeniorCitizen": 0,
                "Partner": "Yes", "Dependents": "No",
                "tenure": 12, "PhoneService": "Yes",
                "MultipleLines": "No", "InternetService": "Fiber optic",
                "OnlineSecurity": "No", "OnlineBackup": "No",
                "DeviceProtection": "No", "TechSupport": "No",
                "StreamingTV": "No", "StreamingMovies": "No",
                "Contract": "Month-to-month", "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 70.7, "TotalCharges": 850.5
            }
        }
    }


class PrediccionChurn(BaseModel):
    probabilidad_churn: float
    decision: Literal["RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO"]
    recomendacion: str
    timestamp: str


# ── App ───────────────────────────────────────────────────────────
app = FastAPI(
    title="Telco Churn Prediction API",
    description="Predice si un cliente va a cancelar su contrato. Modelo entrenado con XGBoost.",
    version="1.0.0",
)


# Transformaciones que aplico para que el cliente pueda mandar strings
# y yo internamente convertirlo al formato que espera el pipeline
def transformar_input(cliente: Cliente) -> pd.DataFrame:
    data = cliente.model_dump()
    # Mapeos manuales que el pipeline original aplicaba antes del prep
    data["gender"] = 1 if data["gender"] == "Male" else 0
    for c in ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]:
        data[c] = 1 if data[c] == "Yes" else 0
    data["Contract"] = {"Month-to-month": 0, "One year": 1, "Two year": 2}[data["Contract"]]
    return pd.DataFrame([data])


def interpretar(proba: float) -> tuple[str, str]:
    if proba >= 0.7:
        return "RIESGO ALTO", "Cliente con muy alta probabilidad de churn. Priorizar campaña de retención con descuento."
    if proba >= 0.4:
        return "RIESGO MEDIO", "Cliente con riesgo moderado. Incluir en campaña masiva de retención."
    return "RIESGO BAJO", "Cliente con bajo riesgo. No requiere acción especial."


# ── Endpoints ─────────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "ok", "modelo": "telco-churn-xgboost", "version": "1.0.0"}


@app.post("/predict", response_model=PrediccionChurn)
def predict(cliente: Cliente):
    try:
        df = transformar_input(cliente)
        proba = float(modelo.predict_proba(df)[0, 1])
        decision, recomendacion = interpretar(proba)
        return PrediccionChurn(
            probabilidad_churn=round(proba, 4),
            decision=decision,
            recomendacion=recomendacion,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en prediccion: {e}")


@app.post("/batch")
def batch(clientes: list[Cliente]):
    if len(clientes) > 1000:
        raise HTTPException(status_code=400, detail="Maximo 1000 clientes por batch")
    df = pd.concat([transformar_input(c) for c in clientes], ignore_index=True)
    probas = modelo.predict_proba(df)[:, 1]
    resultados = []
    for proba in probas:
        decision, recomendacion = interpretar(float(proba))
        resultados.append({
            "probabilidad_churn": round(float(proba), 4),
            "decision": decision,
            "recomendacion": recomendacion,
        })
    return {"n_predicciones": len(resultados), "predicciones": resultados}
