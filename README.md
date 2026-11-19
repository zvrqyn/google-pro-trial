# google-pro-trial

English | [Español](README.es.md) | [简体中文](README.zh-CN.md)

Google One has hidden `$0` free-trial offers for **AI Pro (5 TB)** that don't show up in the app's upgrade page — they only appear in the responses from Google Play Billing. This tool attaches to Google One via Frida, grabs the offer directly from Play Billing, and opens the Play checkout popup on your emulator or rooted phone so you can verify `$0` and confirm manually.

## What you get

- **12 months free** (`g1.2tb.ai.subs_variant` / `12months-eft`) — 5 TB, then `$19.99/mo` if you don't cancel
- **6 months free** (`g1.2tb.ai.subs_variant` / `6months-eft`, plus `6months-eft-2` / `6months-eft-ss-2026`)
- **3 months free** (`g1.play.2tb.ai` / `eft-3mo`) — handy fallback if Google Play rejects the 12-month SKU with *"You already have a subscription"*

Cancel auto-renewal in Google Play right after activating and you keep the trial without getting billed later.

## Before you start

- **Use an alt account.** Don't test on your main Google account.
- **No prior Google One history** on that account (if the account or Play profile had Google One before, Play usually rejects the 12m offer as *"already subscribed"*).
- **Payment method attached** in Google Play (needed to open the checkout sheet; nothing is charged on a `$0` trial).
- **MuMu Player (Root enabled)** or a **rooted Android phone** with **Google Play Store** and **Google One** installed.
  - In MuMu: open **Device Settings -> Developer Options -> Enable Root**, then restart the emulator. Works directly via `adb root` (`uid=0`), no separate `su` binary needed.
- **Python 3.10+** and **`frida==16.7.19`** (Frida 17+ removed the global `Java` runtime, so `16.7.19` is required):

```powershell
pip install -r requirements.txt
```

`adb` is picked up automatically from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`, MuMu's `shell\adb.exe`, or `PATH`. `frida-server` (x86_64 for MuMu on Windows, arm64 for phones) is downloaded and pushed automatically.

## Quick start (Windows)

Double-click `start.bat` and choose your language (`1. English`, `2. Español`, `3. 简体中文`):

1. **12-month Pro trial** — uses the account currently active in Play Store and stops at the checkout dialog so you check `$0` and confirm yourself.
2. **6-month Pro trial** — same flow with `6months-eft`.
3. **Batch mode** — paste `email----password----` lines followed by `END`.

## CLI usage

```powershell
# Check adb, root, frida-server, and billing module
python pro_trial.py --check

# Print all offers returned by Play Billing for the active account (doesn't open checkout)
python pro_trial.py --list --serial 127.0.0.1:16384

# Open checkout on an account already signed in on MuMu (manual confirm)
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"

# Switch offer: --plan 6m or --plan 3m
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
```

| Flag | Meaning |
|---|---|
| `--check` | Check environment (`adb`, root, `frida-server`, billing module) |
| `--list` | List offers only, without opening checkout |
| `--plan` | `pro` / `auto` (longest), `12m`, `6m`, or `3m` |
| `--account` | Single account (`email:password[:totp]`) |
| `--no-add` | Skip adding account (already signed in) |
| `--no-switch` | Don't switch Play accounts, only verify the active one |
| `--no-confirm` | Stop at the Play checkout popup so you confirm manually |
| `--serial` | Target specific ADB device (e.g. `127.0.0.1:16384`) |

## Offers reference

| `--plan` | Product ID | Offer ID | Trial | Price after |
|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 months | $19.99/mo |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft` (`6months-eft-2`, `6months-eft-ss-2026`) | 6 months | $19.99/mo |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 months | $19.99/mo |

## Repo layout

- `start.bat` — Windows double-click entry (EN / ES / ZH language menu)
- `pro_trial.py` — Interactive menu and CLI entry point
- `bridge.py` — ADB, Frida, and Play `BillingClient` core (handles `adb root` + EN/ES/ZH Play Store UI)
- `requirements.txt` — pins `frida==16.7.19`

## Note

For research and personal testing only. Always check that Google Play shows `$0` / Free trial before tapping Subscribe, and cancel auto-renewal in **Play Store -> Payments & subscriptions -> Subscriptions**.
