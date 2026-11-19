# Google AI Pro Trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

Minimalist CLI and interactive launcher for discovering and opening **Google AI Pro (5 TB)** `$0` free-trial offers via Frida + Android Google Play `BillingClient` on **MuMu Player** (with Root enabled) or a rooted Android device.

> **Disclaimer:** Using automation or hooking Google Play Billing may violate Google Terms of Service and risk account restrictions. Use only on secondary accounts, verify the Play checkout dialog shows `$0` / free trial before subscribing, and cancel auto-renewal in Google Play before the trial expires.

---

## Requirements

| Component | Details |
|---|---|
| **OS** | Windows 10 / 11 (or macOS / Linux) |
| **Python** | Python 3.10+ |
| **Frida** | **`frida==16.7.19`** (`pip install -r requirements.txt` — Frida 17+ removed global `Java`, so `16.7.19` is required) |
| **ADB** | Android `platform-tools` (auto-detected from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, MuMu `shell\adb.exe`, or `PATH`) |
| **Device / Emulator** | **MuMu Player** with Root enabled (supports `adb root` / `uid=0` directly without a `su` binary) or a rooted Android phone |
| **Apps on device** | **Google Play Store** (signed in with a payment method added) + **Google One** (`com.google.android.apps.subscriptions.red`) |

---

## Setup

1. Install the exact Frida version:
   ```powershell
   pip install -r requirements.txt
   ```
2. Open **MuMu Player**, go to **Device Settings → Developer Options → Enable Root**, and restart the emulator.
3. Inside MuMu, sign in to **Google Play Store** with your account (with a payment method added) and install **Google One**.

---

## Usage

### Option A: Interactive Menu (Windows)
Double-click `start.bat` and choose your language (`1. English`, `2. Español`, `3. 简体中文`), or run `python pro_trial.py --lang en`. After the environment check, choose from:
1. **Launch Pro 12-month trial** — opens `12months-eft` (`g1.2tb.ai.subs_variant`) on the active Play Store account and pauses at checkout for manual review.
2. **Launch Pro 6-month trial** — opens `6months-eft` (`g1.2tb.ai.subs_variant`) on the active Play Store account and pauses at checkout.
3. **Batch accounts** — paste `email----password----` lines followed by `END`.

### Option B: Direct CLI

1. **Environment self-check** (`adb`, `root`, `frida-server`, billing module):
   ```powershell
   python pro_trial.py --check
   ```

2. **List available Pro offers** on the active Play Store account (read-only):
   ```powershell
   python pro_trial.py --list --serial 127.0.0.1:16384
   ```

3. **Open the checkout dialog and review manually (`--no-confirm`)**:
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --serial 127.0.0.1:16384 --account "your_alt@gmail.com:password"
   ```

4. **Force the 3-month offer (`--plan 3m`)** if Play Store rejects the 12-month variant with *"You already have a subscription"*:
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "your_alt@gmail.com:password"
   ```

### CLI Options

| Flag | Description | Default |
|---|---|---|
| `--check` | Check `adb`, root, `frida-server`, and billing module | — |
| `--list` | Query available offers only without launching checkout | — |
| `--plan` | `pro` / `auto` (longest), `12m`, `6m`, or `3m` | `pro` |
| `--account` | Single account in `email:password[:totp]` format | — |
| `--no-add` | Skip adding the Google account (already signed in on device) | off |
| `--no-switch` | Verify active Play Store account without switching automatically | off |
| `--no-confirm` | Leave the Play checkout dialog open on screen for manual confirmation | off |
| `--serial` | Target specific ADB device serial (e.g. `127.0.0.1:16384`) | first device |

---

## Supported Product IDs

| Plan Flag | Product ID | Storage | Regular Price | Trial Offers |
|---|---|---|---|---|
| `12m` / `pro` | `g1.2tb.ai.subs_variant` | 5 TB | $19.99/mo | 12 months / 6 months (`12months-eft`, `6months-eft*`) |
| `3m` / `pro` | `g1.play.2tb.ai` | 5 TB | $19.99/mo | 3 months (`eft-3mo`) |

---

## Files

- `pro_trial.py` — Minimalist English interactive launcher & CLI entry point
- `bridge.py` — Frida + ADB + UI core engine (supports `adb root` and EN/ES/ZH Play Store UI)
- `start.bat` — Windows double-click launcher for `pro_trial.py`
- `requirements.txt` — Pins `frida==16.7.19`
