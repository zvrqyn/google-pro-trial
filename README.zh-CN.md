# google-pro-trial

[English](README.md) | [Español](README.es.md) | 简体中文

Google One 里隐藏着 **AI Pro (5 TB)** 的 `$0` 免费试用 offer，在应用界面里看不到，只存在于 Google Play Billing 的返回数据里。这个工具通过 Frida 挂载 Google One，直接从 Play Billing 拉取 offer，并把 Play 结账弹窗打开在你的模拟器或已 Root 手机上，核对 `$0` 后手动确认即可。

## 可用档位

- **12 个月免费**（`g1.2tb.ai.subs_variant` / `12months-eft`）— 5 TB，到期后 `$19.99/月`
- **6 个月免费**（`g1.2tb.ai.subs_variant` / `6months-eft`，另有 `6months-eft-2` / `6months-eft-ss-2026`）
- **3 个月免费**（`g1.play.2tb.ai` / `eft-3mo`）— 如果 12 个月版本被 Play 提示「已有订阅」，可以改用这个

开通后立刻去 Google Play 取消自动续订，试用时长保留且到期不会扣费。

## 准备条件

- **请用小号测试**，不要用主力 Google 账号。
- **账号之前没开过 Google One**（只要开过，即使当前没有订阅，12 个月 offer 也常会提示「已有订阅」）。
- **Google Play 已绑定付款方式**（拉起收银台必须有卡，`$0` 试用不扣费）。
- **开启 Root 的 MuMu 模拟器**或**已 Root 安卓手机**，且已安装 **Google Play 商店**与 **Google One**。
  - MuMu 设置路径：**设备设置 -> 开发者选项 -> 开启 Root**，然后重启模拟器。脚本直接兼容 `adb root`（`uid=0`），不需要单独装 `su`。
- **Python 3.10+** 与 **`frida==16.7.19`**（Frida 17+ 移除了全局 `Java`，必须锁定 `16.7.19`）：

```powershell
pip install -r requirements.txt
```

`adb` 会自动从 `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`、MuMu 目录或 `PATH` 中查找；`frida-server`（Windows MuMu 用 `x86_64`，真机用 `arm64`）会自动下载并推送。

## 快速开始（Windows）

双击 `start.bat`，选择界面语言（`1. English`、`2. Español`、`3. 简体中文`）：

1. **Pro 12 个月免费试用** — 直接使用当前 Play 商店账号，打开结账窗后停住，确认 `$0` 后手动点订阅。
2. **Pro 6 个月免费试用** — 同上，拉起 `6months-eft`。
3. **批量模式** — 粘贴 `邮箱----密码----` 列表，最后单独一行输入 `END`。

## 命令行用法

```powershell
# 检查 adb、root、frida-server 和计费模块
python pro_trial.py --check

# 只读列出当前 Play 账号能查到的所有 offer（不拉起结账）
python pro_trial.py --list --serial 127.0.0.1:16384

# 对已在 MuMu 登录好的账号直接拉起结账窗（手动确认）
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"

# 改用 6 个月或 3 个月
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:pass"
```

| 参数 | 说明 |
|---|---|
| `--check` | 检查环境（`adb`、root、`frida-server`、计费模块） |
| `--list` | 只查 offer，不拉起支付弹窗 |
| `--plan` | `pro` / `auto`（最长）、`12m`、`6m` 或 `3m` |
| `--account` | 单账号（`email:password[:totp]`） |
| `--no-add` | 跳过加号（账号已在设备上） |
| `--no-switch` | 不自动切换 Play 账号，只核对当前账号 |
| `--no-confirm` | 拉起结账窗后停住，不自动点击订阅 |
| `--serial` | 指定 ADB 设备（如 `127.0.0.1:16384`） |

## Offer 对照

| `--plan` | Product ID | Offer ID | 试用时长 | 到期价格 |
|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 个月 | $19.99/月 |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft`（`6months-eft-2`、`6months-eft-ss-2026`） | 6 个月 | $19.99/月 |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 个月 | $19.99/月 |

## 文件结构

- `start.bat` — Windows 双击启动（内置 EN / ES / ZH 语言选择）
- `pro_trial.py` — 交互菜单与命令行入口
- `bridge.py` — ADB、Frida 与 Play `BillingClient` 核心（支持 `adb root` 及中/英/西语 Play 界面）
- `requirements.txt` — 锁定 `frida==16.7.19`

## 说明

仅供个人测试与研究使用。点击订阅前请务必确认弹窗金额为 `$0` / 免费试用，开通后前往 **Play 商店 -> 付款和订阅 -> 订阅** 取消自动续订。
