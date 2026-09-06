import os
from datetime import datetime


def capture_screen() -> str:
    """Capture a screenshot and save it permanently under screenshots/.

    pyautogui is imported lazily so the module can be imported on headless
    CI runners (no DISPLAY) without raising KeyError.
    """
    try:
        import pyautogui  # lazy: requires a display only when actually called
    except Exception as e:
        return f"[Ekran Görüntüsü Hatası]: pyautogui yüklenemedi ({e})"

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
