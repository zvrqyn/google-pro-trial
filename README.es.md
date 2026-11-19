# google-pro-trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

Consulta `BillingClient` de Google Play dentro de Google One mediante Frida para abrir el cobro en `$0` de las pruebas gratuitas de **Google AI Pro (5 TB)** en **MuMu Player** (con Root activado) o un Android con root.

> Úsalo solo en cuentas secundarias. Revisa siempre en pantalla que marque prueba gratuita (`$0` hoy) antes de confirmar y cancela la renovación automática en Google Play antes de que termine el periodo de prueba.

## Requisitos

- Windows 10/11 (o macOS / Linux)
- Python 3.10+
- **`frida==16.7.19`** (`pip install -r requirements.txt` — Frida 17+ eliminó `Java` global, así que `16.7.19` es obligatorio)
- `adb` (`platform-tools` — se detecta solo en `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, en `shell\adb.exe` de MuMu o en `PATH`)
- **MuMu Player** con Root activado (`Configuración del dispositivo -> Opciones de desarrollador -> Habilitar root -> Reiniciar`) o teléfono Android con root
- **Google Play Store** (con sesión iniciada y método de pago agregado) + **Google One** (`com.google.android.apps.subscriptions.red`) instalado en el dispositivo

## Instalación

```powershell
pip install -r requirements.txt
```

Abre MuMu Player con Root activado, inicia sesión en Google Play Store, agrega un método de pago e instala Google One.

## Uso

### Lanzador de Windows (`start.bat`)
Haz doble clic en `start.bat`, elige idioma (`1. English`, `2. Español`, `3. 简体中文`) y selecciona una opción:
1. **Prueba Pro 12 meses** (`12months-eft`) sobre la cuenta activa en Play Store — se detiene en la ventana de pago para confirmar a mano.
2. **Prueba Pro 6 meses** (`6months-eft`) sobre la cuenta activa en Play Store — se detiene en la ventana de pago.
3. **Modo por lotes** — pega líneas `correo----contraseña----` y termina con `END`.

### Línea de comandos (CLI)

Comprobar `adb`, root, `frida-server` y módulo de facturación:
```powershell
python pro_trial.py --check
```

Ver todas las ofertas que devuelve Play Billing en la cuenta activa (solo lectura):
```powershell
python pro_trial.py --list --serial 127.0.0.1:16384
```

Abrir el pago sobre una cuenta ya iniciada sin confirmar automáticamente:
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "correo@gmail.com:clave"
```

Cambiar a `--plan 6m` o `--plan 3m` si quieres la oferta de 6 o 3 meses:
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "correo@gmail.com:clave"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "correo@gmail.com:clave"
```

### Parámetros

| Opción | Qué hace | Por defecto |
|---|---|---|
| `--check` | Comprueba `adb`, root, `frida-server` y módulo de facturación | — |
| `--list` | Muestra las ofertas disponibles sin abrir el pago | — |
| `--plan` | `pro` / `auto` (la más larga), `12m`, `6m` o `3m` | `pro` |
| `--account` | Cuenta única (`correo:contraseña[:totp]`) | — |
| `--no-add` | Salta el inicio de sesión (cuenta ya en el dispositivo) | off |
| `--no-switch` | Verifica la cuenta activa en Play sin cambiarla | off |
| `--no-confirm` | Deja el pago abierto en pantalla para confirmar manualmente | off |
| `--serial` | Dispositivo ADB concreto (ej. `127.0.0.1:16384`) | primero disponible |

## IDs de producto y ofertas

| `--plan` | Product ID | Offer ID(s) | Prueba | Espacio | Precio regular |
|---|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 meses | 5 TB | $19.99/mes |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 meses | 5 TB | $19.99/mes |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 meses | 5 TB | $19.99/mes |

## Archivos

- `start.bat` — Lanzador de Windows con selector de idioma
- `pro_trial.py` — Menú interactivo y entrada CLI
- `bridge.py` — Lógica de ADB, Frida y Play `BillingClient` (soporta `adb root` y UI en EN/ES/ZH)
- `requirements.txt` — `frida==16.7.19`
