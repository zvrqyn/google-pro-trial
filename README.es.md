# Google AI Pro Trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

Lanzador interactivo minimalista y CLI para consultar y abrir pruebas gratuitas (`$0`) de **Google AI Pro (5 TB)** mediante Frida + `BillingClient` de Google Play en **MuMu Player** (con Root activado) o un Android con root.

> **Aviso:** Automatizar o inyectar en Google Play Billing puede infringir los Términos de Servicio de Google y provocar restricciones en la cuenta. Úsalo solo en cuentas secundarias, verifica en pantalla que muestre prueba gratuita (`$0` hoy) antes de pulsar suscribir y cancela la renovación automática en Google Play antes de que termine el periodo de prueba.

---

## Requisitos

| Componente | Detalle |
|---|---|
| **Sistema** | Windows 10 / 11 (o macOS / Linux) |
| **Python** | Python 3.10+ |
| **Frida** | **`frida==16.7.19`** (`pip install -r requirements.txt` — Frida 17+ quitó `Java` global, por lo que `16.7.19` es obligatorio) |
| **ADB** | Android `platform-tools` (se detecta solo en `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, en `shell\adb.exe` de MuMu o en `PATH`) |
| **Dispositivo / Emulador** | **MuMu Player** con Root activado (soporta `adb root` / `uid=0` directo sin binario `su`) o teléfono Android con root |
| **Apps en el dispositivo** | **Google Play Store** (con sesión iniciada y método de pago agregado) + **Google One** (`com.google.android.apps.subscriptions.red`) |

---

## Preparación

1. Instala la versión exacta de Frida:
   ```powershell
   pip install -r requirements.txt
   ```
2. Abre **MuMu Player**, entra a **Configuración del dispositivo → Opciones de desarrollador → Habilitar root**, activa el interruptor y reinicia el emulador.
3. Dentro de MuMu, inicia sesión en **Google Play Store** con tu cuenta secundaria (con tarjeta vinculada) e instala **Google One**.

---

## Uso

### Opción A: Menú interactivo con selector de idioma (Windows)
Haz doble clic en `start.bat` y elige tu idioma (`1. English`, `2. Español`, `3. 简体中文`), o ejecuta `python pro_trial.py --lang es`. Tras comprobar el entorno podrás elegir:
1. **Abrir prueba Pro 12 meses** — abre `12months-eft` (`g1.2tb.ai.subs_variant`) en la cuenta activa de Play Store y pausa en el pago para confirmar a mano.
2. **Abrir prueba Pro 6 meses** — abre `6months-eft` (`g1.2tb.ai.subs_variant`) en la cuenta activa de Play Store y pausa en el pago.
3. **Modo por lotes** — pega líneas `correo----contraseña----` y termina con `END`.

### Opción B: Línea de comandos directa

1. **Comprobar entorno** (`adb`, `root`, `frida-server`, módulo de facturación):
   ```powershell
   python pro_trial.py --check
   ```

2. **Listar ofertas disponibles** en la cuenta activa de Play Store (solo lectura):
   ```powershell
   python pro_trial.py --list --serial 127.0.0.1:16384
   ```

3. **Abrir la pantalla de pago y dejarla lista para confirmar manualmente (`--no-confirm`)**:
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --serial 127.0.0.1:16384 --account "tucorreo@gmail.com:tuclave"
   ```

4. **Ir directo a la oferta de 3 meses (`--plan 3m`)** si Google Play responde *"Ya tienes una suscripción"* con la variante de 12 meses:
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "tucorreo@gmail.com:tuclave"
   ```

### Opciones de línea de comandos

| Opción | Descripción | Por defecto |
|---|---|---|
| `--check` | Verifica `adb`, root, `frida-server` y módulo de facturación | — |
| `--list` | Solo consulta las ofertas disponibles sin abrir el cobro | — |
| `--plan` | `pro` / `auto` (más larga), `12m`, `6m` o `3m` | `pro` |
| `--account` | Cuenta única en formato `correo:contraseña[:totp]` | — |
| `--no-add` | Salta el inicio de sesión (cuando la cuenta ya está en el dispositivo) | desactivado |
| `--no-switch` | Verifica la cuenta activa en Play Store sin cambiarla automáticamente | desactivado |
| `--no-confirm` | Deja la ventana de pago de Google Play abierta para confirmar a mano | desactivado |
| `--serial` | Apunta a un dispositivo ADB concreto (ej. `127.0.0.1:16384`) | primer dispositivo |

---

## IDs de producto soportados

| Plan (`--plan`) | Product ID | Almacenamiento | Precio regular | Ofertas de prueba |
|---|---|---|---|---|
| `12m` / `pro` | `g1.2tb.ai.subs_variant` | 5 TB | $19.99/mes | 12 meses / 6 meses (`12months-eft`, `6months-eft*`) |
| `3m` / `pro` | `g1.play.2tb.ai` | 5 TB | $19.99/mes | 3 meses (`eft-3mo`) |

---

## Archivos

- `pro_trial.py` — Menú interactivo minimalista en inglés y punto de entrada CLI
- `bridge.py` — Motor Frida + ADB + UI (compatible con `adb root` e interfaz en español, inglés y chino)
- `start.bat` — Lanzador de Windows para `pro_trial.py`
- `requirements.txt` — Fija `frida==16.7.19`
