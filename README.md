# google-pro-trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

Queries Google Play `BillingClient` inside Google One via Frida to open `$0` free-trial checkout flows for **Google AI Pro (5 TB)** on **MuMu Player** (with Root enabled) or a rooted Android device.

> Use on secondary accounts only. Always verify the Play Store checkout dialog shows a `$0` free trial before confirming, and cancel auto-renewal in Google Play before the trial ends.

## Requirements

- Windows 10/11 (or macOS / Linux)
- Python 3.10+
- **`frida==16.7.19`** (`pip install -r requirements.txt` — Frida 17+ removed global `Java`, so `16.7.19` is required)
- `adb` (`platform-tools` — auto-detected from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, MuMu `shell\adb.exe`, or `PATH`)
- **MuMu Player** with Root enabled (`Device Settings -> Developer Options -> Enable Root -> Restart`) or a rooted Android phone
- **Google Play Store** (signed in with a payment method added) + **Google One** (`com.google.android.apps.subscriptions.red`) installed on the device

## Setup

```powershell
pip install -r requirements.txt
```

Start MuMu Player with Root enabled, sign in to Google Play Store, add a payment method, and install Google One.

## Usage

### Windows launcher (`start.bat`)
Double-click `start.bat`, pick a language (`1. English`, `2. Español`, `3. 简体中文`), then select an action:
1. **12-month Pro trial** (`12months-eft`) on the active Play Store account — stops at the checkout dialog so you confirm manually.
2. **6-month Pro trial** (`6months-eft`) on the active Play Store account — stops at the checkout dialog.
3. **Batch mode** — paste `email----password----` lines followed by `END`.

### CLI

Check `adb`, root, `frida-server`, and the billing module:
```powershell
python pro_trial.py --check
```

List all offers returned by Play Billing for the active account (read-only):
```powershell
python pro_trial.py --list --serial 127.0.0.1:16384
```

Open checkout on an already signed-in account without auto-confirming:
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
```

Use `--plan 6m` or `--plan 3m` if you want the 6-month or 3-month offer instead:
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
```

### Flags

| Flag | What it does | Default |
|---|---|---|
| `--check` | Verify `adb`, root, `frida-server`, and billing module | — |
| `--list` | Print available offers without launching checkout | — |
| `--plan` | `pro` / `auto` (longest), `12m`, `6m`, or `3m` | `pro` |
| `--account` | Single account (`email:password[:totp]`) | — |
| `--no-add` | Skip Google login (account already on device) | off |
| `--no-switch` | Verify active Play account without switching | off |
| `--no-confirm` | Leave checkout open on screen for manual confirmation | off |
| `--serial` | Specific ADB target (e.g. `127.0.0.1:16384`) | first device |

## Product IDs & Offers

| `--plan` | Product ID | Offer ID(s) | Trial | Storage | Regular Price |
|---|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 months | 5 TB | $19.99/mo |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 months | 5 TB | $19.99/mo |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 months | 5 TB | $19.99/mo |

## Files

- `start.bat` — Windows launcher with language prompt
- `pro_trial.py` — Menu and CLI entry point
- `bridge.py` — ADB, Frida, and Play `BillingClient` logic (supports `adb root` and EN/ES/ZH Play UI)
- `requirements.txt` — `frida==16.7.19`
