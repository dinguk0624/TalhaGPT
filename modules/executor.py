# modules/executor.py
"""Code execution is intentionally disabled."""


def run_python_code(code: str) -> str:
    """Do not execute model- or user-supplied Python."""
    return (
        "[Güvenlik]: Rastgele Python kodu çalıştırma devre dışı bırakıldı. "
        "Bu özellik güvenlik nedeniyle kullanılamaz."
    )
