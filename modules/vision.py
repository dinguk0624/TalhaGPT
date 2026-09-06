import os
from datetime import datetime

import pyautogui


def capture_screen() -> str:
    """Capture a screenshot and save it permanently under screenshots/."""
    try:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        save_path = os.path.join("screenshots", filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)

        abs_path = os.path.abspath(save_path)
        return (
            f"[Ekran Görüntüsü]: Başarıyla alındı ve kaydedildi.\n"
            f"Dosya yolu: {abs_path}\n"
            f"Not: Görüntü şu an sadece dosya olarak saklanıyor. "
            f"Modelin görüntüyü doğrudan analiz etmesi için ileride vision model desteği eklenebilir."
        )
    except Exception as e:
        return f"[Ekran Görüntüsü Hatası]: {e}"
