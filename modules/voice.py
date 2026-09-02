# modules/voice.py
import os
import tempfile
from gtts import gTTS
import pygame
from config import TTS_LANGUAGE, ENABLE_VOICE

def speak(text: str):
    """Metni Türkçe sese çevirip çalar."""
    # Ses kapalıysa veya metin boşsa hiç ses çıkarma
    if not ENABLE_VOICE or not text.strip():
        return
    
    try:
        # Use tempfile module for secure temp file handling
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            filename = tmp.name
        
        tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
        tts.save(filename)

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
    except Exception as e:
        print(f"[Ses Hatası]: {e}")
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception:
                pass
