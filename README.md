# google-pro-trial

**English** · [Español](README.es.md) · [简体中文](README.zh-CN.md)

A terminal menu for Google AI Pro (5 TB) trials on Android. I tested it on Windows with MuMu Player. Google Play showed three trial lengths for my account. I chose the 12-month offer and the receipt showed **US$0.00**.

## What showed up on my account

| Trial | What I saw |
| --- | --- |
| 12 months | Confirmed in Google Play. The receipt was for US$0.00. |
| 6 months | Appeared among the offers for the same account. |
| 3 months | Also appeared for that account. |

The Windows menu shows the 12- and 6-month options. The table includes the 3-month offer because it also appeared in the account results.

## What the receipt tells you

US$0.00 was the charge at sign-up. Google Play lists the renewal date and price separately under **Payments & subscriptions → Subscriptions**. Those are the terms to check for your own account.

## Project files

The menu is available in English, Spanish and Simplified Chinese. It is designed for MuMu Player and rooted Android phones.

| File | Role |
| --- | --- |
| `start.bat` | Windows launcher. |
| `pro_trial.py` | Language selection, terminal menu and command-line options. |
| `bridge.py` | Communication between the computer and the Android device. |
| `requirements.txt` | Python dependency used by the project. |

Based on work by **gylive**. The MIT license and copyright notices are in `LICENSE`.
