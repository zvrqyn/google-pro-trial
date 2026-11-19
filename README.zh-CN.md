# Google AI Pro Trial

[English](README.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md)

用于在 **MuMu 模拟器**（开启 Root）或已 Root 的安卓设备上，通过 Frida 注入 Google One 调用 Google Play `BillingClient`，查询并拉起 **Google AI Pro (5 TB)** `$0` 免费试用的极简英文交互式启动器与命令行工具。

> **免责声明：** 自动化或 Hook Google Play Billing 可能违反 Google 服务条款并导致账号受限。请仅在备用账号测试，确认结账窗口显示 `$0` 免费试用后再点订阅，并在试用到期前前往 Google Play 取消自动续订。

---

## 环境要求

| 组件 | 说明 |
|---|---|
| **系统** | Windows 10 / 11（或 macOS / Linux） |
| **Python** | Python 3.10+ |
| **Frida** | **`frida==16.7.19`**（执行 `pip install -r requirements.txt`；Frida 17+ 移除了全局 `Java` 对象，必须使用 `16.7.19`） |
| **ADB** | Android `platform-tools`（自动检测 `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`、MuMu 自带 `shell\adb.exe` 或 `PATH`） |
| **设备 / 模拟器** | 开启 Root 的 **MuMu 模拟器**（支持直接 `adb root` / `uid=0`，无需额外 `su` 文件）或已 Root 安卓手机 |
| **设备应用** | 已登录并绑定付款方式的 **Google Play 商店** + 已安装的 **Google One**（`com.google.android.apps.subscriptions.red`） |

---

## 准备工作

1. 安装指定版本的 Frida：
   ```powershell
   pip install -r requirements.txt
   ```
2. 打开 **MuMu 模拟器**，进入 **设备设置 → 开发者选项 → 开启 Root 权限**，保存并重启模拟器。
3. 在 MuMu 内登录 **Google Play 商店**（绑定好付款方式）并安装 **Google One**。

---

## 使用方法

### 方式 A：多语言交互式菜单（Windows）
双击 `start.bat` 选择语言（`1. English`、`2. Español`、`3. 简体中文`），或直接运行 `python pro_trial.py --lang zh`。环境自检完成后可选择：
1. **拉起 Pro 12 个月免费试用** — 对当前 Play 账号拉起 `12months-eft`（`g1.2tb.ai.subs_variant`）并停在结账页供手动确认。
2. **拉起 Pro 6 个月免费试用** — 对当前 Play 账号拉起 `6months-eft`（`g1.2tb.ai.subs_variant`）并停在结账页供手动确认。
3. **批量账号模式** — 粘贴 `邮箱----密码----` 列表并输入 `END` 批量执行。

### 方式 B：命令行直连

1. **环境自检**（`adb`、`root`、`frida-server`、计费模块）：
   ```powershell
   python pro_trial.py --check
   ```

2. **仅查询当前账号可用的 Pro 试用 offer**（只读）：
   ```powershell
   python pro_trial.py --list --serial 127.0.0.1:16384
   ```

3. **拉起结账弹窗并停留在屏幕供手动确认（`--no-confirm`）**：
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --serial 127.0.0.1:16384 --account "your_alt@gmail.com:password"
   ```

4. **强制使用 3 个月版本（`--plan 3m`）**（若 12 个月版本提示「已有订阅」时使用）：
   ```powershell
   python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "your_alt@gmail.com:password"
   ```

### 命令行参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--check` | 检查 `adb`、root、`frida-server` 与计费模块 | — |
| `--list` | 仅查询可用 offer，不拉起结账 | — |
| `--plan` | `pro` / `auto`（最长）、`12m`、`6m` 或 `3m` | `pro` |
| `--account` | 单账号格式 `email:password[:totp]` | — |
| `--no-add` | 跳过添加账号（设备已登录时使用） | 关闭 |
| `--no-switch` | 只校验当前 Play 账号，不自动切换 | 关闭 |
| `--no-confirm` | 拉起 Google Play 结账窗后不自动点击订阅，方便人工核对 | 关闭 |
| `--serial` | 指定 ADB 设备序列号（如 `127.0.0.1:16384`） | 第一个设备 |

---

## 支持的产品 ID

| 参数 (`--plan`) | Product ID | 容量 | 原价 | 试用 Offer |
|---|---|---|---|---|
| `12m` / `pro` | `g1.2tb.ai.subs_variant` | 5 TB | $19.99/月 | 12 个月 / 6 个月（`12months-eft`、`6months-eft*`） |
| `3m` / `pro` | `g1.play.2tb.ai` | 5 TB | $19.99/月 | 3 个月（`eft-3mo`） |

---

## 文件说明

- `pro_trial.py` — 极简英文交互式启动器与命令行主入口
- `bridge.py` — Frida + ADB + UI 核心引擎（兼容 `adb root` 与中/英/西语 Play 界面）
- `start.bat` — Windows 双击启动脚本
- `requirements.txt` — 锁定 `frida==16.7.19`
