# google-pro-trial

[English](README.md) · **Español** · [简体中文](README.zh-CN.md)

Herramienta para Windows y Android que abre las pruebas gratuitas de `$0` de **Google AI Pro (5 TB)** que no aparecen en los botones normales de Google One. Probado en Windows con MuMu Player: se conecta a Google One con Frida, consulta las ofertas reales de Google Play Billing y abre la ventana de pago de Google Play para que verifiques **US$0.00** y confirmes a mano.

## Ofertas disponibles

| Plan | Product ID | Offer ID | Duración | Renovación |
| --- | --- | --- | --- | --- |
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 meses | $19.99/mes |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 meses | $19.99/mes |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 meses | $19.99/mes |

US$0.00 es el cobro del día de activación. Si cancelas la renovación automática justo después en **Play Store → Pagos y suscripciones → Suscripciones**, mantienes el periodo de prueba sin cobros al vencer.

## Requisitos

| Requisito | Detalle |
| --- | --- |
| **Python 3.10+ y Frida 16.7.19** | Ejecuta `pip install -r requirements.txt` (Frida 17+ eliminó `Java` global, por eso se requiere `16.7.19`). |
| **ADB** | Se detecta solo en `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, en `shell\adb.exe` de MuMu o en `PATH`. |
| **MuMu Player (Root) o Android con root** | En MuMu: **Configuración del dispositivo → Opciones de desarrollador → Habilitar root** y reiniciar. Funciona directo con `adb root` (`uid=0`), sin binario `su`. |
| **Google Play + Google One** | Sesión iniciada en una **cuenta secundaria (alt)** con método de pago agregado y sin historial previo de Google One. |

`frida-server` (`x86_64` en MuMu Windows, `arm64` en teléfonos) y el módulo de Play Billing se descargan y suben solos.

## Forma fácil (Windows)

1. Instala Frida `16.7.19`:
   ```powershell
   pip install -r requirements.txt
   ```
2. Inicia tu dispositivo Android dentro de **MuMu Player** (con Root activado), inicia sesión en **Google Play Store**, agrega un método de pago e instala **Google One**.
3. Haz doble clic en **`start.bat`**, elige idioma (`1. English`, `2. Español`, `3. 简体中文`) y selecciona:
   - `1` — **Pro 12 meses** (`12months-eft`), pausa en la ventana de pago para confirmar a mano.
   - `2` — **Pro 6 meses** (`6months-eft`), pausa en la ventana de pago.
   - `3` — **Modo por lotes** (pega líneas `correo----contraseña----` y escribe `END`).

## Línea de comandos (CLI)

```powershell
# Comprobar adb, root, frida-server y módulo de facturación
python pro_trial.py --check

# Ver todas las ofertas de Play Billing en la cuenta activa (solo lectura)
python pro_trial.py --list --serial 127.0.0.1:16384

# Abrir pago en la cuenta activa sin confirmar automáticamente (12m, 6m o 3m)
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
```

Formato para archivo por lotes (una cuenta por línea, campos extra opcionales):
```text
correo----contraseña----recuperación----clave_2fa----tarjeta----MM/AA----CVC----titular----cp
```

## Problemas comunes

- **"Ya tienes una suscripción" en 12m:** Google Play revisa el historial de la cuenta/dispositivo. Prueba con `--plan 3m`, o quita la cuenta que ya activaste antes en MuMu y prueba con otra cuenta nueva.
- **"No se detectó ningún dispositivo":** asegúrate de tener encendida la instancia de Android dentro de MuMu (no solo el panel principal de MuMu).
- **Se queda colgado al consultar ofertas:** revisa `python -c "import frida; print(frida.__version__)"` — si dice `17.x`, instala `frida==16.7.19`.

## Archivos

| Archivo | Función |
| --- | --- |
| `start.bat` | Lanzador de Windows (selector de idioma EN / ES / ZH) |
| `pro_trial.py` | Menú interactivo y punto de entrada CLI |
| `bridge.py` | Núcleo ADB, Frida y Play `BillingClient` (soporta `adb root` y Play Store en EN/ES/ZH) |
| `requirements.txt` | Fija `frida==16.7.19` |

## Licencia y aviso

Úsalo bajo tu propia responsabilidad: solo en cuentas secundarias que no te importe perder, nunca en tu cuenta principal. Licencia MIT — ver `LICENSE`.
