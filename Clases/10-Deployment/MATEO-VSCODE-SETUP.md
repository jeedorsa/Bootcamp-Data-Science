# MATEO en VS Code — Setup en 5 minutos

Guía para conectar tu MATEO (Ollama corriendo local) a VS Code y tener tu propio Copilot privado y gratuito.

---

## Paso 0 — Instalar y ENCENDER Ollama (3 min)

**¿Qué es Ollama?** El servidor que corre el modelo LLM (MATEO) en tu máquina. Sin Ollama corriendo, nada funciona.

### Instalación (solo la primera vez)

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** descargar instalador desde https://ollama.com/download

### ENCENDER Ollama

Ollama necesita estar corriendo como servicio para responder. Hay 2 formas:

**Opción A — Servicio (recomendado, queda encendido siempre):**

```bash
# Mac
brew services start ollama

# Linux (systemd)
sudo systemctl start ollama
sudo systemctl enable ollama   # para que arranque solo al reiniciar

# Windows: Ollama arranca solo al instalarse, mirá la bandeja del sistema
```

**Opción B — Manualmente en una terminal (queda apagado al cerrar):**

```bash
ollama serve
```

Esta terminal queda ocupada mientras Ollama corre. Abrí otra terminal para los demás comandos.

### Verificar que ENCENDIÓ correctamente

```bash
curl http://localhost:11434
```

Tiene que responder `Ollama is running`. Si te tira `Connection refused`, Ollama NO está encendido — volvé al paso anterior.

### APAGAR Ollama (cuando quieras liberar RAM)

```bash
# Mac
brew services stop ollama

# Linux
sudo systemctl stop ollama

# Si lo encendiste con "ollama serve": Ctrl+C en esa terminal
```

### Descargar tu primer modelo

```bash
ollama pull llama3.1:8b      # 4.7 GB - funciona en 8 GB RAM
ollama pull qwen2.5:7b       # 4.4 GB - mejor para código (necesitas 16+ GB RAM ideal)
```

Verificá que quedó:
```bash
ollama list
```

---

## Paso 1 — Probar que MATEO responde (10 seg)

```bash
ollama run llama3.1:8b "Hola, presentate"
```

Si te responde algo, MATEO está vivo y conversa. Escribí `/bye` para salir. Ahora a conectarlo a VS Code.

---

## Paso 2 — Instalar la extensión Continue (1 min)

1. Abrí **VS Code**
2. `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows/Linux) → buscá **Continue**
3. Click **Install** en la extensión de `continue.dev`
4. Reiniciá VS Code

---

## Paso 3 — Configurar Continue para que use tu MATEO (2 min)

Abrí (o creá) el archivo `~/.continue/config.json` y pegá esto:

```json
{
  "models": [
    {
      "title": "MATEO Local",
      "provider": "ollama",
      "model": "llama3.1:8b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Autocomplete",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b"
  }
}
```

> **Importante**: cambiá `"llama3.1:8b"` por el modelo que descargaste (`qwen2.5:7b`, `qwen3:14b`, etc).

> Para el **autocompletado** descargá un modelo chiquito (rápido):
> ```bash
> ollama pull qwen2.5-coder:1.5b
> ```

---

## Paso 4 — Probar (1 min)

1. En VS Code: abrí el panel de Continue (icono en la barra lateral izquierda, o `Cmd+L`)
2. Escribí: `Explica que es FastAPI en 3 lineas`
3. Si te responde → tu MATEO está conectado ✅

### Trucos rápidos

| Atajo | Qué hace |
|---|---|
| `Cmd+L` | Abrir panel de chat con MATEO |
| `Cmd+I` | Editar código seleccionado con instrucción en lenguaje natural |
| `Cmd+Shift+L` | Generar código nuevo en el cursor |
| Escribir `@file` | Pasarle un archivo completo como contexto |
| Escribir `@codebase` | Pasarle el contexto del proyecto entero |

---

## ¿Y si quiero el modelo de Azure (más potente)?

Si tenés MATEO también deployado en una Azure VM (ver [docs/02-setup-azure.md](https://github.com/jeedorsa/MATEO/blob/main/docs/02-setup-azure.md)), agregalo como modelo extra:

```json
{
  "models": [
    {
      "title": "MATEO Local (rapido)",
      "provider": "ollama",
      "model": "llama3.1:8b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "MATEO Azure (potente)",
      "provider": "openai",
      "model": "THUDM/glm-4-9b-chat",
      "apiBase": "http://<TU-IP-AZURE>:8000/v1",
      "apiKey": "tu-token-secreto"
    }
  ]
}
```

Después en el panel de Continue, usás el selector arriba para cambiar entre los modelos según necesites velocidad o calidad.

---

## Troubleshooting

### "Connection refused" / Continue no responde
Ollama está APAGADO. Hacé este check rápido:

```bash
curl http://localhost:11434
```

Si te tira `Connection refused`, encendelo:
- **Mac:** `brew services start ollama`
- **Linux:** `sudo systemctl start ollama`
- **Windows:** abrir Ollama desde el menú de inicio
- **Manualmente (cualquier OS):** `ollama serve` en una terminal

Verificá que arrancó con `curl http://localhost:11434` — debe decir `Ollama is running`.

### El autocompletado es lento
El modelo de autocompletado es muy grande. Cambialo a uno chico:
```bash
ollama pull qwen2.5-coder:1.5b
```
Y en el config.json poné `"model": "qwen2.5-coder:1.5b"` en `tabAutocompleteModel`.

### Continue no aparece en la barra lateral
Reiniciá VS Code completamente (no solo recargar ventana).

### Quiero deshabilitar el autocompletado temporalmente
En `~/.continue/config.json` borrá la sección `tabAutocompleteModel` o ponela en `null`.

---

## Para los más curiosos

Continue es **open source** y tiene mucho más:
- **Slash commands** custom: `/explain`, `/test`, `/comment` con prompts tuyos
- **Context providers** custom: conectar a Notion, Linear, etc
- **Diff editing**: ver lo que el modelo cambió antes de aceptar

Ver: https://docs.continue.dev

---

## Otras alternativas (si Continue no te gusta)

- **Cline**: agente autónomo (lee/escribe archivos, ejecuta comandos). Lo más cercano a Claude Code corriendo gratis.
- **Cursor**: editor entero basado en IA. Soporta APIs custom.
- **Zed**: editor liviano con soporte nativo de Ollama.

Para coding agéntico avanzado, **Cline + Qwen3-Coder** en tu MATEO es lo más potente que vas a tener corriendo gratis.
