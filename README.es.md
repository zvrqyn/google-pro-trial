# google-pro-trial

[English](README.md) · **Español** · [简体中文](README.zh-CN.md)

Un menú de terminal para las pruebas de Google AI Pro (5 TB) en Android. Lo probé en Windows con MuMu Player. En mi cuenta aparecieron tres duraciones. Elegí la de 12 meses y el recibo de Google Play marcó **US$0.00**.

## Qué apareció en mi cuenta

| Duración | Qué vi |
| --- | --- |
| 12 meses | Confirmé la suscripción en Google Play. El recibo fue de US$0.00. |
| 6 meses | Figuraba entre las ofertas de la misma cuenta. |
| 3 meses | También aparecía en esa cuenta. |

En el menú de Windows verás las opciones de 12 y 6 meses. La de 3 meses figura en la tabla porque también apareció al consultar las ofertas de la cuenta.

## Cómo leer el recibo

Los US$0.00 corresponden al día en que activé la prueba. Google Play muestra por separado la fecha y el precio de renovación en **Pagos y suscripciones → Suscripciones**. Ahí puedes consultar las condiciones de tu cuenta.

## Archivos del proyecto

El menú está en español, inglés y chino simplificado. Está pensado para MuMu Player y teléfonos Android con root.

| Archivo | Para qué sirve |
| --- | --- |
| `start.bat` | Abre el programa en Windows. |
| `pro_trial.py` | Contiene el selector de idioma, el menú y las opciones de consola. |
| `bridge.py` | Se encarga de la comunicación entre el equipo y el dispositivo Android. |
| `requirements.txt` | Indica la dependencia de Python que usa el proyecto. |

Basado en el trabajo de **gylive**. La licencia MIT y los avisos de autoría están en `LICENSE`.
