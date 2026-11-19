# google-pro-trial

[English](README.md) · [Español](README.es.md) · **简体中文**

适用于 Windows 与 Android 的工具，用于拉起 **Google AI Pro（5 TB）** 隐藏在 Google Play Billing 里的 `$0` 免费试用。已在 Windows 的 MuMu 模拟器上实测：通过 Frida 注入 Google One，读取实时 Play Billing 优惠，并打开 Google Play 结账弹窗，核对 **US$0.00** 后手动确认。

## 可用试用档位

| 参数 | Product ID | Offer ID | 试用时长 | 到期续费 |
| --- | --- | --- | --- | --- |
| `12m` | `g1.2tb.ai.subs_variant` | `12months-eft` | 12 个月 | $19.99/月 |
| `6m` | `g1.2tb.ai.subs_variant` | `6months-eft`（`6months-eft-2`、`6months-eft-ss-2026`） | 6 个月 | $19.99/月 |
| `3m` | `g1.play.2tb.ai` | `eft-3mo` | 3 个月 | $19.99/月 |

US$0.00 是开通当天的实付金额。开通后前往 **Play 商店 → 付款和订阅 → 订阅** 取消自动续订，即可保留试用期且到期不扣费。

## 环境要求

| 组件 | 说明 |
| --- | --- |
| **Python 3.10+ 与 Frida 16.7.19** | 运行 `pip install -r requirements.txt`（Frida 17+ 移除了全局 `Java`，必须使用 `16.7.19`）。 |
| **ADB** | 自动查找 `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`、MuMu 自带 `shell\adb.exe` 或 `PATH`。 |
| **MuMu 模拟器（Root）或已 Root 手机** | MuMu 路径：**设备设置 → 开发者选项 → 开启 Root** 并重启。直接支持 `adb root`（`uid=0`），无需单独 `su`。 |
| **Google Play + Google One** | 使用**备用小号**登录，已绑定付款方式，且该账号此前未订阅过 Google One。 |

`frida-server`（Windows MuMu 自动选 `x86_64`，手机自动选 `arm64`）与 Play 计费模块会自动下载并推送。

## 最简单用法（Windows）

1. 安装 Frida `16.7.19`：
   ```powershell
   pip install -r requirements.txt
   ```
2. 启动 **MuMu 模拟器**里的安卓实例（已开启 Root），登录 **Google Play 商店**、绑定付款方式并安装 **Google One**。
3. 双击 **`start.bat`**，选择语言（`1. English`、`2. Español`、`3. 简体中文`），然后选择：
   - `1` — **Pro 12 个月免费试用**（`12months-eft`），停在结账窗手动确认。
   - `2` — **Pro 6 个月免费试用**（`6months-eft`），停在结账窗手动确认。
   - `3` — **批量模式**（粘贴 `邮箱----密码----` 列表，最后一行输入 `END`）。

## 命令行（CLI）

```powershell
# 检查 adb、root、frida-server 和计费模块
python pro_trial.py --check

# 只读查看当前 Play 账号能查到的所有优惠（不拉起结账）
python pro_trial.py --list --serial 127.0.0.1:16384

# 对当前已登录账号直接拉起结账窗（手动确认，支持 12m / 6m / 3m）
python pro_trial.py --no-add --no-switch --no-confirm --plan 12m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
python pro_trial.py --no-add --no-switch --no-confirm --plan 3m --serial 127.0.0.1:16384 --account "alt@gmail.com:password"
```

批量文件格式（每行一个账号，后面的字段可留空）：
```text
邮箱----密码----辅助邮箱----2FA密钥----卡号----月/年----CVC----持卡人----邮编
```

## 常见问题

- **12 个月提示「已有订阅」：** Google Play 会检查账号与设备历史。可改试 `--plan 3m`，或在 MuMu 中移除已开通过的旧账号后换新小号。
- **提示「未检测到设备」：** 确认已启动 MuMu 里的安卓模拟器窗口，而不只是打开了 MuMu 管理器主界面。
- **查询优惠时一直卡住：** 运行 `python -c "import frida; print(frida.__version__)"`，若为 `17.x` 请重装 `frida==16.7.19`。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `start.bat` | Windows 启动器（支持 EN / ES / ZH 语言选择） |
| `pro_trial.py` | 交互式菜单与命令行入口 |
| `bridge.py` | ADB、Frida 与 Play `BillingClient` 核心（兼容 `adb root` 及中/英/西语 Play 界面） |
| `requirements.txt` | 锁定 `frida==16.7.19` |

## 许可与说明

仅供个人测试与研究，请勿使用主力账号。基于 **gylive** 的工作修改，采用 MIT 许可证，详见 `LICENSE`。
