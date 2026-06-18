"""
Gateway FastAPI que llama a Ollama corriendo localmente.

Esto les permite tener su propio "ChatGPT" sin pagar tokens.
Solo necesitan una maquina con minimo 16 GB de RAM (8 GB libres para Ollama).
"""

import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3")


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    model: Optional[str] = None
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(500, ge=10, le=4000)


class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_estimados: int


app = FastAPI(
    title="Ollama Gateway",
    description="API que llama a Ollama local sin gastar tokens de OpenAI/Anthropic",
    version="1.0.0",
)


@app.get("/")
def health():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        modelos = [m["name"] for m in r.json().get("models", [])]
        return {"status": "ok", "modelos_disponibles": modelos}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    model = req.model or DEFAULT_MODEL
    payload = {
        "model": model,
        "prompt": req.prompt,
        "stream": False,
        "options": {
            "temperature": req.temperature,
            "num_predict": req.max_tokens,
        },
    }
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return ChatResponse(
            response=data["response"],
            model=model,
            tokens_estimados=len(data["response"].split()),
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ollama no responde: {e}")


@app.post("/resumir-cliente")
def resumir_cliente(datos_cliente: dict):
    """
    Ejemplo de uso real: integrar el LLM con la API de Telco Churn.

    El cliente envia datos demograficos + comportamiento y el LLM genera
    un resumen ejecutivo con recomendacion accionable de retencion.
    """
    prompt = f"""Eres un analista comercial de retencion de clientes en una telco.
Analiza este cliente y genera un resumen ejecutivo en 3 lineas con:
1. Perfil del cliente
2. Riesgo principal de churn
3. Accion comercial recomendada

Datos del cliente: {datos_cliente}

Resumen ejecutivo:"""

    return chat(ChatRequest(prompt=prompt, max_tokens=200, temperature=0.3))
