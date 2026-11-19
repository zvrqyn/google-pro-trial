# google-pro-trial

[English](README.md) · [Español](README.es.md) · **简体中文**

这是一个在 Android 上查看 Google AI Pro（5 TB）试用选项的终端菜单。我在 Windows 上用 MuMu 模拟器做了测试。我的 Google Play 账号显示了三种试用时长，我选了 12 个月，收据上的实付金额是 **US$0.00**。

## 我的账号显示了哪些试用选项

| 试用时长 | 实测情况 |
| --- | --- |
| 12 个月 | 已在 Google Play 确认订阅，收据金额为 US$0.00。 |
| 6 个月 | 同一账号的可用优惠中列出了这一项。 |
| 3 个月 | 同一账号也显示了这一项。 |

Windows 菜单里列出的是 12 个月和 6 个月。表里还有 3 个月，是因为查询这个账号时也看到了这项优惠。

## 收据金额和续订价格

US$0.00 是开通试用当天的实付金额。续订日期和价格在 Google Play 的**付款和订阅 → 订阅**中单独列出，可以在那里查看自己账号的续订信息。

## 项目文件

菜单提供简体中文、英语和西班牙语，面向 MuMu 模拟器和已获取 root 权限的 Android 手机。

| 文件 | 用途 |
| --- | --- |
| `start.bat` | Windows 启动入口。 |
| `pro_trial.py` | 语言选择、终端菜单和命令行选项。 |
| `bridge.py` | 负责电脑与 Android 设备之间的通信。 |
| `requirements.txt` | 记录项目使用的 Python 依赖。 |

本项目基于 **gylive** 的工作。MIT 许可证和版权声明见 `LICENSE`。
