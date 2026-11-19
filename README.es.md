# google-pro-trial

[English](README.md) | Español | [简体中文](README.zh-CN.md)

Google One tiene pruebas gratuitas de `$0` para **AI Pro (5 TB)** que no salen en los botones normales de la app: solo aparecen en las respuestas internas de Google Play Billing. Esta herramienta se conecta a Google One con Frida, saca la oferta directo desde Play Billing y te deja abierta la ventana de pago de Google Play en tu emulador o teléfono con root para que revises que marque `$0` y confirmes a mano.

## Qué ofrece

- **12 meses gratis** (`g1.2tb.ai.subs_variant` / `12months-eft`) — 5 TB, luego `$19.99/mes` si no cancelas
- **6 meses gratis** (`g1.2tb.ai.subs_variant` / `6months-eft`, más `6months-eft-2` / `6months-eft-ss-2026`)
- **3 meses gratis** (`g1.play.2tb.ai` / `eft-3mo`) — buena alternativa si Play Store te rechaza el de 12 meses con *"Ya tienes una suscripción"*

Si cancelas la renovación automática en Google Play justo después de activarlo, conservas el periodo de prueba sin cobros futuros.

## Antes de empezar

- **Usa una cuenta secundaria.** No lo pruebes en tu cuenta principal de Google.
- **Sin historial previo de Google One** en esa cuenta (si ya tuvo suscripción antes, Google Play suele bloquear el de 12 meses diciendo *"Ya tienes una suscripción"*).
- **Método de pago agregado** en Google Play (necesario para que abra la ventana de cobro; no cobra nada en una prueba `$0`).
- **MuMu Player (con Root activado)** o un **Android con root**, con **Google Play Store** y **Google One** instalados.
  - En MuMu: entra a **Configuración del dispositivo -> Opciones de desarrollador -> Habilitar root** y reinicia el emulador. Funciona directo con `adb root` (`uid=0`), no necesita binario `su`.
- **Python 3.10+** y **`frida==16.7.19`** (Frida 17+ quitó `Java` global, por eso hay que usar `16.7.19`):

```powershell
pip install -r requirements.txt
```

`adb` se detecta solo en `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, en `shell\adb.exe` de MuMu o en `PATH`. `frida-server` (`x86_64` para MuMu en Windows, `arm64` para teléfonos) se descarga y sube automáticamente.

## Inicio rápido (Windows)

Haz doble clic en `start.bat` y elige tu idioma (`1. English`, `2. Español`, `3. 简体中文`):

1. **Prueba Pro 12 meses** — usa la cuenta que tengas abierta en Play Store y se detiene en el cobro para que revises `$0` y confirmes tú mismo.
2. **Prueba Pro 6 meses** — mismo flujo con `6months-eft`.
3. **Modo por lotes** — pega líneas `correo----contraseña----` y escribe `END` al final.

## Uso por consola (CLI)

```powershell
# Comprobar adb, root, frida-server y módulo de facturación
python pro_trial.py --check

# Ver todas las ofertas que devuelve Play Billing en la cuenta activa (no abre pago)
python pro_trial.py --list --serial 127.0.0.1:16384

# Abrir pago en una cuenta ya iniciada en MuMu (confirmación manual)
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"

# Cambiar de oferta: --plan 6m o --plan 3m
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
```

| Opción | Qué hace |
|---|---|
| `--check` | Revisa el entorno (`adb`, root, `frida-server`, módulo de facturación) |
| `--list` | Lista las ofertas sin abrir el cobro |
| `--plan` | `pro` / `auto` (la más larga), `12m`, `6m` o `3m` |
| `--account` | Cuenta única (`correo:contraseña[:totp]`) |
| `--no-add` | Salta el inicio de sesión (cuando la cuenta ya está en el emulador) |
| `--no-switch` | No cambia de cuenta en Play Store, solo verifica la actual |
| `--no-confirm` | Deja la ventana de pago abierta para confirmar a mano |
| `--serial` | Apunta a un dispositivo ADB concreto (ej. `127.0.0.1:16384`) |

## Ofertas soportadas

| `--plan` | Product ID | Offer ID | Duración | Precio después |
|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 meses | $19.99/mes |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 meses | $19.99/mes |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 meses | $19.99/mes |

## Archivos

- `start.bat` — Lanzador de Windows (selector de idioma EN / ES / ZH)
- `pro_trial.py` — Menú interactivo y punto de entrada CLI
- `bridge.py` — Núcleo de ADB, Frida y Play `BillingClient` (compatible con `adb root` y Play Store en EN/ES/ZH)
- `requirements.txt` — fija `frida==16.7.19`

## Aviso

Solo para pruebas personales e investigación. Comprueba siempre que Google Play muestre `$0` / Prueba gratuita antes de pulsar Suscribirse, y cancela la renovación automática en **Play Store -> Pagos y suscripciones -> Suscripciones**.
