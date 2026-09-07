# modules/system.py
import os

import psutil


def _disk_root() -> str:
    if os.name == "nt":
        drive = os.path.splitdrive(os.path.abspath("."))[0]
        return drive + os.sep if drive else "C:\\"
    return "/"


def get_system_status():
    """Sistem kaynaklarının anlık durumunu döndürür."""
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage(_disk_root()).percent

    return (
        f"CPU Kullanımı: %{cpu_usage} | "
        f"RAM Kullanımı: %{ram_usage} | "
        f"Disk Kullanımı: %{disk_usage}"
    )