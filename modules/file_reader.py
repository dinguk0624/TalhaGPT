# modules/file_reader.py
import os

def read_local_file(file_path: str) -> str:
    """Belirtilen dosya yolundaki metni okur."""
    # Tırnak işaretleri varsa temizle
    clean_path = file_path.strip("'\"")
    
    if not os.path.exists(clean_path):
        return f"[Hata]: '{clean_path}' adında bir dosya bulunamadı."
    
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Dosya çok uzunsa Ollama'yı kilitlenmesin diye sınırla (ilk 10.000 karakter)
            if len(content) > 10000:
                return content[:10000] + "\n\n[Not: Dosya çok uzun olduğu için ilk 10.000 karakter okundu.]"
            return content
    except Exception as e:
        return f"[Hata]: Dosya okunurken bir sorun oluştu: {e}"