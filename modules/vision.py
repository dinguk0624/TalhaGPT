import os
import pyautogui

def capture_screen() -> str:
    try:
        save_path = "temp_screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return f"Ekran görüntüsü başarıyla alındı ve '{save_path}' dosyasına kaydedildi."
    except Exception as e:
        return f"Ekran görüntüsü alınırken hata oluştu: {e}"
