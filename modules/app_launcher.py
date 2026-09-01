# modules/app_launcher.py
import os

# Sık kullanılan Windows uygulamaları ve sistem komutları
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
    "spotify": "spotify.exe"
}

def launch_app(user_input: str) -> str:
    """Kullanıcının isteğine göre Windows uygulamasını başlatır."""
    text = user_input.lower()
    
    # Tanımlı uygulamalarda arama yap
    target_app = None
    app_label = ""
    
    for name, exe in APPS.items():
        if name in text:
            target_app = exe
            app_label = name
            break
            
    if not target_app:
        # Eğer listede yoksa, "aç" kelimesinden önceki veya sonraki kelimeyi çalıştırmayı dene
        words = text.replace("aç", "").replace("başlat", "").replace("çalıştır", "").strip().split()
        if words:
            target_app = words[0] + ".exe"
            app_label = words[0]
        else:
            return "[Uygulama Hatası]: Hangi uygulamanın açılacağı anlaşılamadı."

    try:
        # Windows 'start' komutu ile uygulamayı arka planda başlat
        os.system(f"start {target_app}")
        return f"[Sistem]: '{app_label.upper()}' uygulaması başarıyla başlatıldı."
    except Exception as e:
        return f"[Uygulama Hatası]: Uygulama başlatılamadı: {e}"