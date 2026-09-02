import os
import tempfile
import pyautogui

def capture_screen() -> str:
    try:
        # Use tempfile module for secure temp file handling
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            save_path = tmp.name
        
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        
        result = f"Ekran görüntüsü başarıyla alındı ve '{save_path}' dosyasına kaydedildi."
        
        # Clean up temp file after use
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
        except Exception:
            pass
        
        return result
    except Exception as e:
        return f"Ekran görüntüsü alınırken hata oluştu: {e}"
