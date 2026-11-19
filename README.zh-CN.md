# google-pro-trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

通过 Frida 注入 Google One 调用安卓端 Google Play `BillingClient`，在开启 Root 的 **MuMu 模拟器**或已 Root 安卓手机上查询并拉起 **Google AI Pro (5 TB)** `$0` 免费试用结账窗口。

> 仅在备用账号使用。确认订阅前请核对结账页显示 `$0` 免费试用，并在到期前于 Google Play 取消自动续订。

## 环境要求

- Windows 10/11（或 macOS / Linux）
- Python 3.10+
- **`frida==16.7.19`**（执行 `pip install -r requirements.txt`；Frida 17+ 移除了全局 `Java`，必须使用 `16.7.19`）
- `adb`（`platform-tools`，自动检测 `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`、MuMu 自带 `shell\adb.exe` 或 `PATH`）
- 开启 Root 的 **MuMu 模拟器**（`设备设置 -> 开发者选项 -> 开启 Root -> 重启`）或已 Root 安卓手机
- 设备已登录并绑卡的 **Google Play 商店** + 已安装的 **Google One**（`com.google.android.apps.subscriptions.red`）

## 安装依赖

```powershell
pip install -r requirements.txt
```

启动已开启 Root 的 MuMu 模拟器，登录 Google Play 商店并添加付款方式，安装 Google One。

## 使用方法

### Windows 启动器（`start.bat`）
双击 `start.bat`，选择语言（`1. English`、`2. Español`、`3. 简体中文`），再选操作：
1. **Pro 12 个月免费试用**（`12months-eft`）— 使用当前 Play 账号，停在结账弹窗手动确认。
2. **Pro 6 个月免费试用**（`6months-eft`）— 使用当前 Play 账号，停在结账弹窗手动确认。
3. **批量模式** — 粘贴 `邮箱----密码----` 列表，最后输入 `END`。

### 命令行（CLI）

检查 `adb`、root、`frida-server` 与计费模块：
```powershell
python pro_trial.py --check
```

只读查询当前账号可用的全部 offer：
```powershell
python pro_trial.py --list --serial 127.0.0.1:16384
```

对已登录账号直接拉起结账窗但不自动确认：
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
```

指定 6 个月或 3 个月版本：
```powershell
python pro_trial.py --no-add --no-switch --no-confirm --plan 6m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "email@gmail.com:password"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--check` | 检查 `adb`、root、`frida-server` 与计费模块 | — |
| `--list` | 只查询可用 offer，不拉起结账 | — |
| `--plan` | `pro` / `auto`（最长）、`12m`、`6m` 或 `3m` | `pro` |
| `--account` | 单账号（`email:password[:totp]`） | — |
| `--no-add` | 跳过添加账号（设备已登录时使用） | 关闭 |
| `--no-switch` | 只校验当前 Play 账号，不自动切换 | 关闭 |
| `--no-confirm` | 拉起结账窗后停留在屏幕，供手动确认 | 关闭 |
| `--serial` | 指定 ADB 设备（如 `127.0.0.1:16384`） | 第一个设备 |

## 产品 ID 与试用 Offer

| `--plan` | Product ID | Offer ID | 试用时长 | 容量 | 原价 |
|---|---|---|---|---|---|
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 个月 | 5 TB | $19.99/月 |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft`（`6months-eft-2`、`6months-eft-ss-2026`） | 6 个月 | 5 TB | $19.99/月 |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 个月 | 5 TB | $19.99/月 |

## 文件说明

- `start.bat` — Windows 启动脚本（带语言选择）
- `pro_trial.py` — 交互菜单与命令行入口
- `bridge.py` — ADB、Frida 与 Play `BillingClient` 核心逻辑（兼容 `adb root` 及中/英/西语 Play 界面）
- `requirements.txt` — `frida==16.7.19`
