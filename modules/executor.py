# modules/executor.py
import subprocess

def run_python_code(code: str) -> str:
    """Verilen Python kodunu güvenli şekilde çalıştırır."""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout if result.stdout else "Kod başarıyla çalıştı (Çıktı yok)."
        else:
            return f"Kod Hatası:\n{result.stderr}"
    except Exception as e:
        return f"Çalıştırma Hatası: {e}"