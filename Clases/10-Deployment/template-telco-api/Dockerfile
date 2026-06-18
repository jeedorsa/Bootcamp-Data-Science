# Imagen base liviana con Python 3.10
FROM python:3.10-slim

# Variables de entorno comunes
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /code

# Instalar dependencias primero (mejora cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar la app y el modelo
COPY app/ ./app/

# Exponer el puerto donde corre uvicorn
EXPOSE 8000

# Comando que se ejecuta al levantar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
