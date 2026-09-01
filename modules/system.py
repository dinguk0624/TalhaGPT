# modules/system.py
import psutil

def get_system_status():
    """Sistem kaynaklarının anlık durumunu döndürür."""
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return f"CPU Kullanımı: %{cpu_usage} | RAM Kullanımı: %{ram_usage} | Disk Kullanımı: %{disk_usage}"