import os
from datetime import datetime

from config import OLLAMA_HOST, VISION_MODEL
from modules.file_reader import _resolve_safe_path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def capture_screen(analyze: bool = False, question: str = "") -> str:
    """Capture a screenshot and optionally describe it with the vision model.

    pyautogui is imported lazily so the module can be imported on headless
    CI runners (no DISPLAY) without raising KeyError.
    """
    if isinstance(analyze, str):
        analyze = analyze.strip().lower() in {"true", "1", "yes"}
    else:
        analyze = bool(analyze)
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
        result = (
            f"[Ekran Görüntüsü]: Başarıyla alındı ve kaydedildi.\n"
            f"Dosya yolu: {abs_path}"
        )
        if analyze:
            description = analyze_image(
                abs_path,
                question or "Describe what is visible on this screenshot.",
            )
            result += f"\n\n[Görüntü Analizi]:\n{description}"
        return result
    except Exception as e:
        return f"[Ekran Görüntüsü Hatası]: {e}"


def analyze_image(file_path: str, question: str = "Describe this image.") -> str:
    """Send a project-local image to the configured Ollama vision model."""
    path, err = _resolve_safe_path(file_path)
    if err:
        return f"[Görüntü Hatası]: {err}"
    if not path.is_file():
        return f"[Görüntü Hatası]: Dosya bulunamadı → {path}"
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return (
            f"[Görüntü Hatası]: '{path.suffix}' desteklenmiyor. "
            f"Kullanılabilir: {', '.join(sorted(IMAGE_EXTENSIONS))}"
        )

    model = (VISION_MODEL or "").strip()
    if not model:
        return (
            "[Görüntü Hatası]: VISION_MODEL ayarlı değil. "
            "Örnek: ollama pull llava  ve  VISION_MODEL=llava"
        )

    prompt = (question or "").strip() or "Describe this image."
    try:
        import ollama

        client = ollama.Client(host=OLLAMA_HOST)
        response = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [str(path)],
                }
            ],
        )
        content = getattr(getattr(response, "message", None), "content", None)
        if not content and isinstance(response, dict):
            content = (response.get("message") or {}).get("content")
        if not content:
            return "[Görüntü Hatası]: Vision model boş cevap döndü."
        return str(content).strip()
    except Exception as e:
        return f"[Görüntü Hatası]: Analiz başarısız ({type(e).__name__}: {e})"
