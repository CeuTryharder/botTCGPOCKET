# 🎴 Pokemon TCG Pocket Bot

> Bot de automatización AFK de código abierto para Pokémon TCG Pocket.  
> Utiliza **ADB** (Android Debug Bridge) y **OpenCV** (Visión por Computadora) para interactuar con un emulador Android.

---

> [!WARNING]
> **Aviso Legal:** Este bot viola los Términos de Servicio de Pokémon TCG Pocket. El uso de macros o herramientas automatizadas puede resultar en el baneo permanente de tu cuenta. **Úsalo bajo tu propia responsabilidad.** Este proyecto es únicamente para fines educativos sobre Visión por Computadora e interacciones ADB.

---

## ✨ Funcionalidades

| Función | Estado |
|---|---|
| 🤖 Automatización AFK completa | ✅ Disponible |
| ⚔️ Farmeo de Batallas en Solitario | ✅ Disponible |
| 🎯 Reclamar Misiones y Recompensas | ✅ Disponible |
| 📸 Herramienta de captura de pantalla para plantillas | ✅ Disponible |

---

## 🏗️ Cómo funciona

El bot opera en 3 capas:

```
Emulador Android (BlueStacks / Nox / AVD)
        ↕  ADB (Android Debug Bridge)
   ADBController  ←→  Vision (OpenCV)
        ↕
     BotTasks  (lógica de las rutinas)
        ↕
     main.py  (menú interactivo)
```

1. **ADBController** (`controller.py`) — Se comunica con el emulador vía ADB: toma capturas de pantalla, realiza taps y swipes.
2. **Vision** (`vision.py`) — Usa OpenCV para buscar imágenes pequeñas ("plantillas") dentro de la captura de pantalla.
3. **BotTasks** (`tasks.py`) — Contiene la lógica de cada rutina automatizada.
4. **main.py** — Punto de entrada con un menú interactivo en consola.

---

## 📋 Requisitos previos

Antes de instalar el bot, asegúrate de tener:

- **Python 3.8 o superior** — [Descargar Python](https://www.python.org/downloads/)
- **ADB (Android Debug Bridge)** — Incluido en [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)
- **Un emulador Android** — Se recomienda una de estas opciones:
  - [BlueStacks 5](https://www.bluestacks.com/)
  - [Nox Player](https://www.bignox.com/)
  - Android Studio AVD (Android Virtual Device)
- **Pokémon TCG Pocket** instalado y con sesión iniciada en el emulador.

### Verificar que ADB está instalado

Abre una terminal y ejecuta:
```bash
adb version
```
Deberías ver algo como `Android Debug Bridge version 1.0.41`. Si no lo reconoce, añade la carpeta `platform-tools` a tu variable de entorno `PATH`.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/botTCGPOCKET.git
cd botTCGPOCKET
```

### 2. Crear y activar el entorno virtual

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias instaladas son:

| Librería | Versión | Uso |
|---|---|---|
| `opencv-python` | 4.9.0.80 | Reconocimiento de imágenes (template matching) |
| `numpy` | 1.26.4 | Procesamiento de arrays de imagen |
| `pure-python-adb` | 0.3.0.dev0 | Comunicación con ADB |
| `Pillow` | 10.3.0 | Manejo de imágenes |

---

## 🖼️ Configuración de Plantillas (Paso Obligatorio)

El bot funciona mediante **reconocimiento de imágenes**: busca pequeñas imágenes de referencia (llamadas "plantillas" o "templates") dentro de la captura de pantalla del emulador.

Debes crear estas plantillas tú mismo, ya que los botones varían según el idioma, resolución y versión del emulador.

### Plantillas necesarias

Guarda los recortes en la carpeta `bot/templates/` con **exactamente** estos nombres:

#### Para "Farmear Batallas en Solitario":

| Archivo | Descripción |
|---|---|
| `battle_btn.png` | Botón para iniciar una batalla |
| `auto_battle_btn.png` | Botón para activar la auto-batalla dentro de la partida |
| `ok_btn.png` | Botón "OK" al finalizar una batalla o reclamar recompensa |
| `next_btn.png` | Botón "Siguiente" o "Continuar" tras ganar/perder |

#### Para "Reclamar Misiones":

| Archivo | Descripción |
|---|---|
| `missions_tab.png` | Icono/pestaña de Misiones en el menú principal |
| `claim_all_btn.png` | Botón "Reclamar Todo" en la pantalla de misiones |
| `ok_btn.png` | Botón "OK" de confirmación (compartido con el anterior) |

### Cómo crear las plantillas

1. Abre el emulador y lanza Pokémon TCG Pocket.
2. Navega a la pantalla donde aparece el botón que quieres capturar.
3. Con el entorno virtual activado, ejecuta desde la raíz del proyecto:
   ```bash
   python bot/screenshot.py
   ```
4. Se generará un archivo `screenshot_XXXXXX.png` en la carpeta actual.
5. Abre esa imagen con cualquier editor (Preview en Mac, Paint en Windows, etc.).
6. **Recorta únicamente el botón**, intentando no incluir demasiado fondo.
7. Guarda el recorte en `bot/templates/` con el nombre exacto correspondiente.

Repite el proceso para cada plantilla necesaria.

> [!TIP]
> Los recortes deben ser precisos. Un recorte muy grande con mucho fondo puede causar que el bot no encuentre el botón correctamente. Intenta recortar solo el texto y/o icono del botón.

---

## 🚀 Uso

### 1. Conectar ADB al emulador

**BlueStacks:** ADB suele conectarse automáticamente al puerto `5555`:
```bash
adb connect 127.0.0.1:5555
```

**Nox Player:** Suele usar el puerto `62001`:
```bash
adb connect 127.0.0.1:62001
```

**Android Studio AVD:** Suele conectarse automáticamente como `emulator-5554`.

Verifica los dispositivos conectados con:
```bash
adb devices
```
Deberías ver tu emulador en la lista.

### 2. Ejecutar el bot

Con el entorno virtual activado, ejecuta desde la raíz del proyecto:

```bash
python bot/main.py
```

Verás un menú interactivo:

```
Initializing Pokemon TCG Pocket Bot...
Checking ADB connection...

Select a task:
1. Farm Solo Battles
2. Claim Missions
3. Exit
Choice:
```

### 3. Seleccionar una tarea

| Opción | Descripción |
|---|---|
| `1` | **Farm Solo Battles** — Bucle infinito de batallas en solitario usando auto-batalla. Inicia desde la pantalla de selección de batalla. |
| `2` | **Claim Missions** — Navega a la pestaña de misiones y reclama todas las recompensas disponibles. Inicia desde el menú principal. |
| `3` | **Exit** — Cierra el bot. |

> [!IMPORTANT]
> Asegúrate de que el juego esté en la pantalla correcta **antes** de lanzar la tarea:
> - Tarea 1 → Pantalla de selección de batalla en solitario.
> - Tarea 2 → Menú principal del juego.

### 4. Detener el bot

Para detener el bot en cualquier momento, pulsa `Ctrl + C` en la terminal.

---

## 🗂️ Estructura del Proyecto

```
botTCGPOCKET/
├── bot/
│   ├── main.py          # Punto de entrada: menú interactivo
│   ├── controller.py    # Comunicación ADB (tap, swipe, screenshot)
│   ├── vision.py        # Reconocimiento de imágenes con OpenCV
│   ├── tasks.py         # Rutinas automatizadas (farmeo, misiones)
│   ├── screenshot.py    # Herramienta para capturar pantalla del emulador
│   └── templates/       # Carpeta donde guardar las imágenes de referencia
│       ├── battle_btn.png        (a crear por el usuario)
│       ├── auto_battle_btn.png   (a crear por el usuario)
│       ├── ok_btn.png            (a crear por el usuario)
│       ├── next_btn.png          (a crear por el usuario)
│       ├── missions_tab.png      (a crear por el usuario)
│       └── claim_all_btn.png     (a crear por el usuario)
├── requirements.txt     # Dependencias de Python
├── README.md            # Esta documentación
├── GUIA_USO.md          # Guía de uso rápido en español
└── LICENSE              # Licencia MIT
```

---

## 🔧 Solución de Problemas

### El bot no encuentra los botones

- Asegúrate de que los archivos `.png` están en `bot/templates/` con los nombres correctos.
- Vuelve a crear la plantilla con un recorte más preciso (menos fondo alrededor del botón).
- Comprueba que la resolución del emulador no haya cambiado desde que creaste las plantillas.

### Error: `adb: command not found`

- Instala [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) y añade la carpeta a tu `PATH`.

### Error de conexión ADB

- Verifica que el emulador esté en ejecución.
- Ejecuta `adb devices` para comprobar si el dispositivo aparece.
- Intenta `adb kill-server` seguido de `adb start-server` para reiniciar el servidor ADB.
- Conecta manualmente con `adb connect 127.0.0.1:PUERTO` (consulta el puerto en la configuración de tu emulador).

### `ModuleNotFoundError` al ejecutar el bot

- Asegúrate de tener el entorno virtual activado (`source venv/bin/activate` en Mac/Linux).
- Reinstala las dependencias: `pip install -r requirements.txt`.

---

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo [`LICENSE`](LICENSE) para más información.
