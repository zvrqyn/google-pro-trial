#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google AI Pro (5 TB) trial tool — interactive menu and CLI entry point."""

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bridge  # noqa: E402

IS_WIN = os.name == "nt"


def _init_console() -> bool:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if IS_WIN:
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            return False
    return bool(getattr(sys.stdout, "isatty", lambda: False)())


_TTY = _init_console()


class Style:
    G = "\033[32m" if _TTY else ""
    R = "\033[31m" if _TTY else ""
    Y = "\033[33m" if _TTY else ""
    C = "\033[36m" if _TTY else ""
    D = "\033[2m" if _TTY else ""
    B = "\033[1m" if _TTY else ""
    X = "\033[0m" if _TTY else ""


I18N = {
    "en": {
        "title": "Google AI Pro Trial (5 TB)",
        "subtitle": "MuMu Player (Root) · Frida BillingClient",
        "step_env": "[1/2] Environment Check",
        "step_act": "[2/2] Action",
        "py_old": "{ver} (Python 3.10+ required)",
        "frida_17": "{ver} found (requires frida==16.7.19 — run: pip install -r requirements.txt)",
        "frida_missing": "Not installed. Run: pip install -r requirements.txt",
        "adb_missing": "Not found. Install Android platform-tools or MuMu Player.",
        "dev_missing": "No device found. Open MuMu Player (with ADB enabled) and try again.",
        "multi_dev": "Multiple ADB targets detected:",
        "select_dev": "Select target [1]: ",
        "root_missing": "Root disabled. In MuMu: Device Settings -> Developer Options -> Enable Root -> Restart.",
        "active_acc": "Active Play Store account",
        "g1_err": "Could not launch Google One. Install Google One from Play Store inside MuMu.",
        "offers_found": "Found {n} free ($0) offer(s).",
        "checkout_ok": "Checkout dialog opened in MuMu.",
        "checkout_tip": "Verify it shows a $0 free trial before subscribing, and cancel auto-renewal afterward.",
        "checkout_fail": "No eligible $0 offer launched. Try the 6-month option (option 2) or another account.",
        "menu_1": "1. Launch Pro 12-month trial (active Play account, manual confirm)",
        "menu_2": "2. Launch Pro 6-month trial (active Play account, manual confirm)",
        "menu_3": "3. Batch accounts (paste email----password---- list)",
        "menu_0": "0. Exit",
        "choose": "Select [1]: ",
        "invalid": "Invalid option.",
        "batch_hint": "Paste accounts (one per line), then type END on a new line:",
        "batch_fmt": "Format: email----password----recovery----2fa----card----MM/YY----CVC----holder----zip",
        "batch_empty": "No accounts provided.",
        "summary": "Summary",
        "col_acc": "Account",
        "col_st": "Status",
        "col_off": "Offer",
        "saved_to": "Reports saved to",
    },
    "es": {
        "title": "Google AI Pro Trial (5 TB)",
        "subtitle": "MuMu Player (Root) · Frida BillingClient",
        "step_env": "[1/2] Comprobación de entorno",
        "step_act": "[2/2] Menú principal",
        "py_old": "{ver} (se requiere Python 3.10+)",
        "frida_17": "Detectado {ver} (requiere frida==16.7.19 — ejecuta: pip install -r requirements.txt)",
        "frida_missing": "No instalado. Ejecuta: pip install -r requirements.txt",
        "adb_missing": "No encontrado. Instala Android platform-tools o MuMu Player.",
        "dev_missing": "No se detectó ningún dispositivo. Abre MuMu Player (con ADB activo) y reintenta.",
        "multi_dev": "Se detectaron varios dispositivos ADB:",
        "select_dev": "Elige dispositivo [1]: ",
        "root_missing": "Sin root. En MuMu: Configuración del dispositivo -> Opciones de desarrollador -> Habilitar root -> Reiniciar.",
        "active_acc": "Cuenta activa en Play Store",
        "g1_err": "No se pudo abrir Google One. Instálalo desde Play Store dentro de MuMu.",
        "offers_found": "Se encontraron {n} oferta(s) gratis ($0).",
        "checkout_ok": "Ventana de pago abierta en MuMu.",
        "checkout_tip": "Verifica en pantalla que diga prueba gratuita ($0 hoy) antes de suscribirte y cancela la renovación después.",
        "checkout_fail": "No se abrió ninguna oferta $0. Prueba la opción de 6 meses (opción 2) o cambia de cuenta.",
        "menu_1": "1. Abrir prueba Pro 12 meses (cuenta activa, confirmación manual)",
        "menu_2": "2. Abrir prueba Pro 6 meses (cuenta activa, confirmación manual)",
        "menu_3": "3. Modo por lotes (pegar lista correo----contraseña----)",
        "menu_0": "0. Salir",
        "choose": "Elige [1]: ",
        "invalid": "Opción no válida.",
        "batch_hint": "Pega las cuentas (una por línea) y escribe END en una línea nueva:",
        "batch_fmt": "Formato: correo----contraseña----recup----2fa----tarjeta----MM/AA----CVC----titular----cp",
        "batch_empty": "No se ingresaron cuentas.",
        "summary": "Resumen",
        "col_acc": "Cuenta",
        "col_st": "Estado",
        "col_off": "Oferta",
        "saved_to": "Reportes guardados en",
    },
    "zh": {
        "title": "Google AI Pro Trial (5 TB)",
        "subtitle": "MuMu 模拟器 (Root) · Frida BillingClient",
        "step_env": "[1/2] 环境检查",
        "step_act": "[2/2] 操作菜单",
        "py_old": "{ver}（需要 Python 3.10+）",
        "frida_17": "当前为 {ver}（需要 frida==16.7.19，请运行：pip install -r requirements.txt）",
        "frida_missing": "未安装。请运行：pip install -r requirements.txt",
        "adb_missing": "未找到 ADB。请安装 Android platform-tools 或 MuMu 模拟器。",
        "dev_missing": "未检测到设备。请先启动 MuMu 模拟器（开启 ADB）后重试。",
        "multi_dev": "检测到多个 ADB 设备：",
        "select_dev": "请选择设备 [1]: ",
        "root_missing": "未开启 Root。请在 MuMu：设备设置 -> 开发者选项 -> 开启 Root -> 重启模拟器。",
        "active_acc": "当前 Play 商店账号",
        "g1_err": "无法启动 Google One。请在 MuMu 的 Play 商店中先安装 Google One。",
        "offers_found": "共找到 {n} 个 $0 免费试用 offer。",
        "checkout_ok": "已在 MuMu 中打开结账窗口。",
        "checkout_tip": "请核对屏幕显示 $0 免费试用后再点订阅，开通后记得取消自动续订。",
        "checkout_fail": "未拉起可用的 $0 试用。请尝试 6 个月版本（选项 2）或更换账号。",
        "menu_1": "1. 拉起 Pro 12 个月免费试用（当前 Play 账号，手动确认）",
        "menu_2": "2. 拉起 Pro 6 个月免费试用（当前 Play 账号，手动确认）",
        "menu_3": "3. 批量账号模式（粘贴 邮箱----密码---- 列表）",
        "menu_0": "0. 退出",
        "choose": "请选择 [1]: ",
        "invalid": "无效选项。",
        "batch_hint": "请粘贴账号（每行一个），完成后单独一行输入 END 回车：",
        "batch_fmt": "格式：邮箱----密码----辅助邮箱----2FA----卡号----月/年----CVC----姓名----邮编",
        "batch_empty": "未输入任何账号。",
        "summary": "汇总",
        "col_acc": "账号",
        "col_st": "状态",
        "col_off": "时长",
        "saved_to": "报告目录",
    },
}

LANG = "en"


def t(key: str, **kwargs) -> str:
    text = I18N.get(LANG, I18N["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def sty(text: str, code: str) -> str:
    return f"{code}{text}{Style.X}"


def section(title: str) -> None:
    print(f"\n{sty(title, Style.B + Style.C)}")
    print(sty("─" * 56, Style.D))


def tag_ok(label: str, detail: str = "") -> None:
    right = f"  {sty(detail, Style.D)}" if detail else ""
    print(f"  {sty('OK', Style.G)}   {label:<12}{right}")


def tag_err(label: str, detail: str = "") -> None:
    right = f"  {detail}" if detail else ""
    print(f"  {sty('ERR', Style.R)}  {label:<12}{right}")


def tag_warn(label: str, detail: str = "") -> None:
    right = f"  {detail}" if detail else ""
    print(f"  {sty('!', Style.Y)}    {label:<12}{right}")


def _adb(*args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    cmd = [bridge.ADB] + (["-s", bridge.SERIAL] if bridge.SERIAL else []) + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def _devices() -> list[str]:
    out = subprocess.run([bridge.ADB, "devices"], capture_output=True, text=True).stdout
    return [ln.split("\t")[0] for ln in out.splitlines()[1:] if "\tdevice" in ln]


def _pick_adb() -> bool:
    try:
        bridge.ADB = bridge.find_adb()
        tag_ok("ADB", bridge.ADB)
        subprocess.run([bridge.ADB, "start-server"], capture_output=True)
        return True
    except SystemExit:
        tag_err("ADB", t("adb_missing"))
        return False


def _pick_target() -> bool:
    devs = _devices()
    if not devs:
        for port in (16384, 16416, 7555, 5555):
            subprocess.run([bridge.ADB, "connect", f"127.0.0.1:{port}"], capture_output=True, timeout=5)
        devs = _devices()

    if not devs:
        tag_err("Device", t("dev_missing"))
        return False

    if len(devs) == 1:
        bridge.SERIAL = devs[0]
        tag_ok("Device", bridge.SERIAL)
        return True

    print(f"\n  {t('multi_dev')}")
    for idx, d in enumerate(devs, 1):
        print(f"    {idx}. {d}")
    raw = input(f"  {t('select_dev')}").strip()
    pick = int(raw) - 1 if raw.isdigit() and 1 <= int(raw) <= len(devs) else 0
    bridge.SERIAL = devs[pick]
    tag_ok("Device", bridge.SERIAL)
    return True


def _check_env() -> bool:
    section(t("step_env"))

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info < (3, 10):
        tag_err("Python", t("py_old", ver=py_ver))
        return False
    tag_ok("Python", py_ver)

    try:
        import frida
        ver = frida.__version__
        major = int(ver.split(".")[0])
        if major >= 17:
            tag_err("Frida", t("frida_17", ver=ver))
            return False
        tag_ok("Frida", ver)
    except Exception:
        tag_err("Frida", t("frida_missing"))
        return False

    if not _pick_adb() or not _pick_target():
        return False

    try:
        bridge.ensure_root()
    except SystemExit:
        _adb("root", timeout=10)
        try:
            bridge.ensure_root()
        except SystemExit:
            tag_err("Root", t("root_missing"))
            return False
    tag_ok("Root", "uid=0")

    bridge.ensure_network()
    try:
        bridge.ensure_frida_server()
        bridge.ensure_module_apk()
    except SystemExit as e:
        tag_err("Setup", str(e))
        return False

    return True


def _run_active(plan: str, list_only: bool = False) -> None:
    acc = bridge.current_play_account()
    print(f"\n  {t('active_acc')}: {sty(acc or 'unknown', Style.B)}")
    pid = bridge.launch_app()
    if not pid:
        tag_err("Google One", t("g1_err"))
        return

    res = bridge.run_trial(pid, wait=25, plan=plan, list_only=list_only)
    if list_only:
        free = [o for o in res.get("offers", []) if str(o.get("micros")) == "0"]
        print(f"\n  {t('offers_found', n=len(free))}")
        for o in free:
            print(f"    - {o.get('product')} | {o.get('id')} | {o.get('period')} ($0)")
        return

    if res.get("launched") and res["launched"].get("code") == 0:
        print(f"\n  {sty(t('checkout_ok'), Style.G)}")
        print(f"  {t('checkout_tip')}")
    else:
        tag_warn("Checkout", t("checkout_fail"))


def _read_batch() -> list[list[str]]:
    print(f"\n  {t('batch_hint')}")
    print(sty(f"  {t('batch_fmt')}", Style.D))
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)

    rows = []
    for raw in lines:
        ln = raw.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = [p.strip() for p in ln.split("----")]
        while len(parts) < 9:
            parts.append("")
        if parts[0]:
            rows.append(parts[:9])
    return rows


def _period_label(rec: dict) -> str:
    txt = (rec.get("sheet") or {}).get("text", "") or ""
    m = re.search(r"(\d+)\s*(months?|mes(?:es)?|个月)", txt, re.I)
    if m:
        return f"{m.group(1)}m"
    rank = {"P1Y": "12m", "P12M": "12m", "P6M": "6m", "P3M": "3m", "P1M": "1m"}
    best = 0
    out = "-"
    for o in rec.get("offers", []):
        if str(o.get("micros")) == "0":
            p = str(o.get("period", ""))
            val = {"P1Y": 12, "P12M": 12, "P6M": 6, "P3M": 3, "P1M": 1}.get(p, 0)
            if val > best:
                best = val
                out = rank[p]
    return out


def _run_batch() -> None:
    rows = _read_batch()
    if not rows:
        tag_warn("Batch", t("batch_empty"))
        return

    bridge.REPORT_DIR.mkdir(exist_ok=True)
    results = []
    total = len(rows)
    for i, row in enumerate(rows, 1):
        email, pw, _rec, sec = row[0], row[1], row[2], row[3]
        card = bridge.parse_card(row)
        print(f"\n  [{i}/{total}] {sty(email, Style.B)}")
        try:
            rec = bridge.process(email, pw, sec, add=True, card=card, plan="pro", no_switch=False)
        except Exception as e:
            rec = {"email": email, "status": "exception", "error": str(e)[:160]}
        results.append(rec)
        (bridge.REPORT_DIR / f"{email.split('@')[0]}.json").write_text(
            bridge.json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    section(t("summary"))
    print(f"  {t('col_acc'):<34} {t('col_st'):<16} {t('col_off')}")
    print("  " + "-" * 60)
    for rec in results:
        st = rec.get("status", "unknown")
        period = _period_label(rec)
        print(f"  {rec.get('email', '?'):<34} {st:<16} {period}")
    print(f"\n  {t('saved_to')}: {bridge.REPORT_DIR.resolve()}")


def interactive_menu() -> int:
    print()
    print(sty(f"  {t('title')}", Style.B))
    print(sty(f"  {t('subtitle')}", Style.D))

    if not _check_env():
        return 1

    while True:
        section(t("step_act"))
        print(f"  {t('menu_1')}")
        print(f"  {t('menu_2')}")
        print(f"  {t('menu_3')}")
        print(f"  {t('menu_0')}")
        try:
            choice = input(f"\n  {t('choose')}").strip() or "1"
        except EOFError:
            return 0

        if choice == "0":
            return 0
        if choice == "1":
            _run_active("12m", list_only=False)
        elif choice == "2":
            _run_active("6m", list_only=False)
        elif choice == "3":
            _run_batch()
        else:
            tag_warn("Menu", t("invalid"))


def _ask_language() -> str:
    print()
    print(sty("  Google AI Pro Trial (5 TB)", Style.B))
    print(sty("  " + "─" * 44, Style.D))
    print("  Select language / Idioma / 选择语言:")
    print()
    print("    1. English")
    print("    2. Español")
    print("    3. 简体中文")
    raw = input("\n  Choose [1-3, default 1]: ").strip()
    return {"1": "en", "2": "es", "3": "zh"}.get(raw, "en")


def main() -> int:
    global LANG
    args = sys.argv[1:]
    ask_lang = False

    if "--ask-lang" in args:
        ask_lang = True
        args = [a for a in args if a != "--ask-lang"]

    # Extract --lang en|es|zh for interactive mode
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args) and args[idx + 1].lower() in I18N:
            LANG = args[idx + 1].lower()
            args = args[:idx] + args[idx + 2:]
        else:
            args = args[:idx] + args[idx + 1:]

    if args and args[0] != "--wizard":
        sys.argv = [sys.argv[0]] + args
        return bridge.main()

    if ask_lang:
        LANG = _ask_language()
    return interactive_menu()


if __name__ == "__main__":
    sys.exit(main())
