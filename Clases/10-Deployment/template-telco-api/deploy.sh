#!/bin/bash
# ============================================================
# Deploy a Azure Container Apps en 6 comandos
# ============================================================
#
# Antes de correr este script:
#   1. Tener Azure CLI instalado: brew install azure-cli
#   2. Login en Azure: az login
#   3. Tener Docker corriendo (si vas a buildear local)
#
# Para correr: bash deploy.sh
# ============================================================

set -e  # falla si algun comando falla

# ── CONFIGURACION (cambien estos valores) ──────────────
TU_NOMBRE="bootcamp"                      # cambien por su nombre, sin espacios ni mayusculas
RESOURCE_GROUP="rg-telco-${TU_NOMBRE}"
LOCATION="eastus"                         # otra opcion: westus2, brazilsouth
ACR_NAME="acr${TU_NOMBRE}$(date +%s)"     # nombre del Container Registry (debe ser unico global)
ENV_NAME="env-telco-${TU_NOMBRE}"         # nombre del Container Apps Environment
APP_NAME="telco-api-${TU_NOMBRE}"         # nombre de la app
IMAGE_TAG="v1"

echo "==============================================="
echo "Deploy Telco Churn API a Azure Container Apps"
echo "==============================================="
echo "Resource Group: $RESOURCE_GROUP"
echo "ACR:            $ACR_NAME"
echo "App:            $APP_NAME"
echo "Location:       $LOCATION"
echo ""

# ── PASO 1: Crear Resource Group ────────────────────────
echo "[1/6] Creando Resource Group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none
echo "  OK"

# ── PASO 2: Crear Container Registry (donde vive la imagen Docker) ──
echo "[2/6] Creando Container Registry..."
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled true \
    --output none
echo "  OK ($ACR_NAME.azurecr.io)"

# ── PASO 3: Buildear la imagen Docker y subirla al ACR ──
# Usamos 'az acr build' que buildea en el cloud (no necesita Docker local)
echo "[3/6] Buildeando imagen en Azure (tarda 2-3 minutos)..."
az acr build \
    --registry "$ACR_NAME" \
    --image "telco-api:$IMAGE_TAG" \
    --file Dockerfile \
    . \
    --output none
echo "  OK"

# ── PASO 4: Crear Container Apps Environment ────────────
echo "[4/6] Creando Container Apps Environment..."
az containerapp env create \
    --name "$ENV_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none
echo "  OK"

# ── PASO 5: Deployar la Container App ───────────────────
echo "[5/6] Deployando Container App..."
ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

az containerapp create \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --environment "$ENV_NAME" \
    --image "${ACR_LOGIN_SERVER}/telco-api:${IMAGE_TAG}" \
    --target-port 8000 \
    --ingress external \
    --registry-server "$ACR_LOGIN_SERVER" \
    --registry-username "$ACR_NAME" \
    --registry-password "$ACR_PASSWORD" \
    --cpu 0.5 \
    --memory 1.0Gi \
    --min-replicas 0 \
    --max-replicas 2 \
    --output none
echo "  OK"

# ── PASO 6: Obtener URL publica ─────────────────────────
echo "[6/6] Obteniendo URL publica..."
URL=$(az containerapp show \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.configuration.ingress.fqdn" \
    -o tsv)

echo ""
echo "==============================================="
echo "DEPLOY COMPLETADO"
echo "==============================================="
echo ""
echo "Tu API esta corriendo en:"
echo "  https://${URL}"
echo ""
echo "Endpoints:"
echo "  https://${URL}/         (health check)"
echo "  https://${URL}/docs     (Swagger UI - probar desde el navegador)"
echo "  https://${URL}/predict  (POST con datos del cliente)"
echo ""
echo "Para probar desde Python: python test_api.py https://${URL}"
echo ""
echo "Para limpiar todo cuando termine la clase:"
echo "  az group delete --name $RESOURCE_GROUP --yes --no-wait"
echo ""
