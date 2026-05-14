# 📖 Guía de Uso Rápido — Bot Pokémon TCG Pocket

Esta guía resume los pasos esenciales para poner en marcha el bot desde cero.  
Para documentación completa consulta el [README.md](README.md).

---

## Paso 1 — Instalar dependencias

```bash
# Activa el entorno virtual
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# Instala las librerías necesarias
pip install -r requirements.txt
```

---

## Paso 2 — Conectar el emulador por ADB

Abre tu emulador (BlueStacks, Nox, etc.) y conecta ADB:

```bash
# BlueStacks
adb connect 127.0.0.1:5555

# Nox Player
adb connect 127.0.0.1:62001

# Verificar conexión
adb devices
```

Deberías ver tu emulador listado como `device`.

---

## Paso 3 — Crear las plantillas de imágenes

El bot usa **reconocimiento de imágenes**: necesita pequeños recortes de los botones del juego para saber dónde hacer clic.

### 3.1 — Capturar la pantalla del emulador

Navega en el juego a la pantalla donde aparece el botón que quieres capturar y ejecuta:

```bash
python bot/screenshot.py
```

Se creará un archivo `screenshot_XXXXXX.png` en la carpeta raíz del proyecto.

### 3.2 — Recortar el botón

Abre la captura con cualquier editor de imágenes y recorta **únicamente** el botón (sin demasiado fondo).

### 3.3 — Guardar en la carpeta de plantillas

Guarda el recorte en `bot/templates/` con el nombre exacto correspondiente:

| Nombre del archivo | Qué recortar |
|---|---|
| `battle_btn.png` | Botón de iniciar batalla en solitario |
| `auto_battle_btn.png` | Botón de auto-batalla dentro de la partida |
| `ok_btn.png` | Botón "OK" de confirmación / fin de batalla |
| `next_btn.png` | Botón "Siguiente" o "Continuar" |
| `missions_tab.png` | Pestaña/icono de Misiones en el menú principal |
| `claim_all_btn.png` | Botón "Reclamar Todo" en la sección de misiones |

Repite los pasos 3.1–3.3 para cada plantilla.

---

## Paso 4 — Ejecutar el bot

Coloca el juego en la pantalla correcta y lanza el bot:

```bash
python bot/main.py
```

Selecciona una opción del menú:

```
1. Farm Solo Battles   → Inicia desde la pantalla de selección de batalla
2. Claim Missions      → Inicia desde el menú principal del juego
3. Exit                → Salir
```

Para detener el bot en cualquier momento: **`Ctrl + C`**

---

## ⚡ Solución rápida de problemas

| Problema | Solución |
|---|---|
| `adb: command not found` | Instala [Platform Tools](https://developer.android.com/tools/releases/platform-tools) y añádelo al `PATH` |
| El bot no encuentra los botones | Recrea la plantilla con un recorte más preciso; asegúrate del nombre exacto del archivo |
| Error de conexión ADB | Ejecuta `adb kill-server && adb start-server`, luego reconecta |
| `ModuleNotFoundError` | Activa el entorno virtual y ejecuta `pip install -r requirements.txt` |
| La pantalla no coincide | Asegúrate de estar en la pantalla correcta antes de iniciar la tarea |
