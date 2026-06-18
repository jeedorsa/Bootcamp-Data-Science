"""
Cliente Python para probar la API de Telco Churn.

Uso local (si la app corre con uvicorn):
    python test_api.py

Uso contra Azure (despues del deploy):
    python test_api.py https://telco-api-bootcamp.eastus.azurecontainerapps.io
"""

import sys
import requests
import json


# Cliente con perfil de ALTO RIESGO (mes a mes + fibra + electronic check + tenure bajo)
CLIENTE_ALTO_RIESGO = {
    "gender": "Female", "SeniorCitizen": 0,
    "Partner": "No", "Dependents": "No",
    "tenure": 2, "PhoneService": "Yes",
    "MultipleLines": "No", "InternetService": "Fiber optic",
    "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No",
    "StreamingTV": "Yes", "StreamingMovies": "Yes",
    "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.50, "TotalCharges": 195.0
}

# Cliente con perfil de BAJO RIESGO (2 años + sin servicios premium + bank transfer + tenure alto)
CLIENTE_BAJO_RIESGO = {
    "gender": "Male", "SeniorCitizen": 0,
    "Partner": "Yes", "Dependents": "Yes",
    "tenure": 60, "PhoneService": "Yes",
    "MultipleLines": "Yes", "InternetService": "DSL",
    "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
    "DeviceProtection": "Yes", "TechSupport": "Yes",
    "StreamingTV": "No", "StreamingMovies": "No",
    "Contract": "Two year", "PaperlessBilling": "No",
    "PaymentMethod": "Bank transfer (automatic)",
    "MonthlyCharges": 65.30, "TotalCharges": 3850.0
}


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    base_url = base_url.rstrip("/")

    print(f"Probando API en: {base_url}\n")

    # 1. Health check
    print("[1] Health check:")
    r = requests.get(f"{base_url}/")
    print(f"    Status: {r.status_code}")
    print(f"    Body:   {r.json()}\n")

    # 2. Prediccion cliente alto riesgo
    print("[2] Prediccion cliente ALTO RIESGO (tenure=2, fibra, electronic check):")
    r = requests.post(f"{base_url}/predict", json=CLIENTE_ALTO_RIESGO)
    print(f"    Status: {r.status_code}")
    print(f"    Body:   {json.dumps(r.json(), indent=2)}\n")

    # 3. Prediccion cliente bajo riesgo
    print("[3] Prediccion cliente BAJO RIESGO (tenure=60, contrato 2 anos):")
    r = requests.post(f"{base_url}/predict", json=CLIENTE_BAJO_RIESGO)
    print(f"    Status: {r.status_code}")
    print(f"    Body:   {json.dumps(r.json(), indent=2)}\n")

    # 4. Batch
    print("[4] Prediccion en BATCH (2 clientes):")
    r = requests.post(f"{base_url}/batch", json=[CLIENTE_ALTO_RIESGO, CLIENTE_BAJO_RIESGO])
    print(f"    Status: {r.status_code}")
    print(f"    Body:   {json.dumps(r.json(), indent=2)}")


if __name__ == "__main__":
    main()
