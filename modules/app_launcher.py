# modules/app_launcher.py
import logging
import platform
import subprocess

logger = logging.getLogger(__name__)

# Only explicitly allowlisted Windows applications may be launched.
# This keeps the tool safe from arbitrary executable execution.
APPS = {
    "hesap makinesi": "calc.exe",
    "not defteri": "notepad.exe",
    "cmd": "cmd.exe",
    "komut satırı": "cmd.exe",
    "görev yöneticisi": "taskmgr.exe",
    "paint": "mspaint.exe",
    "chrome": "chrome.exe",
    "discord": "discord.exe",
    "steam": "steam.exe",
    "spotify": "spotify.exe",
}


def launch_app(user_input: str) -> str:
    """Launch an explicitly allowlisted application (currently Windows-only)."""
    if platform.system() != "Windows":
        return (
            "[Uygulama Hatası]: Uygulama başlatma şu an yalnızca Windows'ta destekleniyor. "
            f"Mevcut sistem: {platform.system()}."
        )

    if not isinstance(user_input, str) or not user_input.strip():
        return "[Uygulama Hatası]: Hangi uygulamanın açılacağı belirtilmedi."

    text = user_input.casefold()
    target_app = None
    app_label = None

    for name, exe in APPS.items():
        if name in text:
            target_app = exe
            app_label = name
            break

    # Never construct an executable name from arbitrary user/model input.
    if target_app is None:
        return "[Uygulama Hatası]: Bu uygulama güvenlik nedeniyle izin verilen listede değil."

    try:
        subprocess.Popen([target_app], shell=False)
        logger.info("Application launched: %s (%s)", app_label, target_app)
        return f"[Sistem]: '{app_label.upper()}' uygulaması başarıyla başlatıldı."
    except FileNotFoundError:
        logger.error("Application not found: %s", target_app)
        return f"[Uygulama Hatası]: '{target_app}' uygulaması bulunamadı."
    except OSError:
        logger.exception("Failed to launch application: %s", target_app)
        return "[Uygulama Hatası]: Uygulama başlatılamadı."
