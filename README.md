# google-pro-trial

**English** · [Español](README.es.md) · [简体中文](README.zh-CN.md)

A Windows & Android tool for opening **Google AI Pro (5 TB)** `$0` free-trial offers that don't appear in the regular Google One upgrade UI. Tested on Windows with MuMu Player: it hooks Google One via Frida, pulls the live Play Billing offers, and opens the Google Play checkout dialog so you can verify **US$0.00** and confirm manually.

## Available offers

| Plan | Product ID | Offer ID | Trial | Renewal price |
| --- | --- | --- | --- | --- |
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 months | $19.99/mo |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 months | $19.99/mo |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 months | $19.99/mo |

US$0.00 is the charge at sign-up. Cancel auto-renewal right afterward under **Play Store → Payments & subscriptions → Subscriptions** and you keep the trial period without getting charged later.

## Requirements

| Requirement | Notes |
| --- | --- |
| **Python 3.10+ & Frida 16.7.19** | Run `pip install -r requirements.txt` (Frida 17+ removed global `Java`, so `16.7.19` is required). |
| **ADB** | Auto-detected from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, MuMu's `shell\adb.exe`, or `PATH`. |
| **MuMu Player (Root) or rooted Android** | In MuMu: **Device Settings → Developer Options → Enable Root**, then restart. Works directly over `adb root` (`uid=0`), no `su` binary required. |
| **Google Play + Google One** | Signed in on a **secondary (alt) account** with a payment method added and no prior Google One subscription history. |

`frida-server` (`x86_64` on Windows MuMu, `arm64` on phones) and the Play Billing helper module are downloaded and pushed automatically.

## Easiest way (Windows)

1. Install Frida `16.7.19`:
   ```powershell
   pip install -r requirements.txt
   ```
2. Start your Android instance inside **MuMu Player** (with Root enabled), sign in to **Google Play Store**, add a payment method, and install **Google One**.
3. Double-click **`start.bat`**, pick your language (`1. English`, `2. Español`, `3. 简体中文`), then choose:
   - `1` — **Pro 12 months** (`12months-eft`), stops at the Play checkout sheet for manual confirmation.
   - `2` — **Pro 6 months** (`6months-eft`), stops at checkout.
   - `3` — **Batch mode** (paste `email----password----` lines, then type `END`).

## Command line (CLI)

```powershell
# Check adb, root, frida-server, and billing module
python pro_trial.py --check

# List all offers returned by Play Billing for the active account (read-only)
python pro_trial.py --list --serial 127.0.0.1:16384

# Open checkout on the active account without auto-confirming (12m, 6m, or 3m)
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
```

Batch file format (one per line, trailing fields optional):
```text
email----password----recovery----2fa_secret----card----MM/YY----CVC----holder----zip
```

## Common issues

- **"You already have a subscription" on 12m:** Google Play checks account/device history. Try `--plan 3m`, or remove the previously subscribed account from MuMu and test with a fresh alt.
- **"No device found":** Make sure the actual Android emulator window is running (not just the MuMu manager/launcher).
- **Script hangs at billing query:** Check `python -c "import frida; print(frida.__version__)"` — if it's `17.x`, reinstall `frida==16.7.19`.

## Files

| File | Role |
| --- | --- |
| `start.bat` | Windows launcher (EN / ES / ZH language picker) |
| `pro_trial.py` | Interactive menu and CLI entry point |
| `bridge.py` | ADB, Frida, and Play `BillingClient` core (supports `adb root` + EN/ES/ZH Play UI) |
| `requirements.txt` | Pins `frida==16.7.19` |

## License & notice

Use at your own risk — only use secondary accounts you don't mind losing, never your main Google account. Licensed under the MIT License — see `LICENSE`.
