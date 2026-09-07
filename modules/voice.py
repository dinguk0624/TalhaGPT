# modules/voice.py
import os
import tempfile

from config import TTS_LANGUAGE, ENABLE_VOICE


def speak(text: str):
    """Metni Türkçe sese çevirip çalar."""
    if not ENABLE_VOICE or not text or not str(text).strip():
        return

    filename = None
    try:
        from gtts import gTTS
        import pygame
    except Exception as e:
        print(f"[Ses Hatası]: Ses kütüphaneleri yüklenemedi ({e})")
        return

    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            filename = tmp.name

        tts = gTTS(text=str(text), lang=TTS_LANGUAGE, slow=False)
        tts.save(filename)

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if hasattr(pygame.mixer.music, "unload"):
            pygame.mixer.music.unload()
    except Exception as e:
        print(f"[Ses Hatası]: {e}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception:
                pass
