# modules/file_reader.py
"""Safe local file and directory reading for TalhaGPT."""

from __future__ import annotations

import os
from pathlib import Path

# Hard cap so the model context is not flooded
MAX_CHARS = 12000

# Only these text-like extensions are read by default
TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".log",
    ".html",
    ".css",
    ".xml",
    ".rst",
    ".env",
    ".sh",
    ".bat",
    ".ps1",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".java",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".sql",
}


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_safe_path(file_path: str) -> tuple[Path | None, str | None]:
    """Resolve path and block traversal outside the project root."""
    if not file_path or not str(file_path).strip():
        return None, "[Okuma Hatası]: Dosya yolu boş olamaz."

    clean = str(file_path).strip().strip("'\"")
    root = _project_root()

    candidate = Path(clean)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        return None, "[Okuma Hatası]: Proje dizini dışındaki dosyalara erişim engellendi."

    return candidate, None


def read_local_file(file_path: str) -> str:
    """Read a text file under the project directory and return its contents."""
    path, err = _resolve_safe_path(file_path)
    if err:
        return err

    if not path.is_file():
        return f"[Okuma Hatası]: Dosya bulunamadı → {path}"

    suffix = path.suffix.lower()
    if suffix and suffix not in TEXT_EXTENSIONS:
        return (
            f"[Okuma Hatası]: '{suffix}' uzantısı desteklenmiyor. "
            f"Desteklenenler: {', '.join(sorted(TEXT_EXTENSIONS))}"
        )

    try:
        raw = path.read_bytes()
    except OSError as e:
        return f"[Okuma Hatası]: Dosya okunamadı: {e}"

    for encoding in ("utf-8", "utf-8-sig", "cp1254", "latin-1"):
        try:
            content = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            content = None
    else:
        return "[Okuma Hatası]: Dosya metin olarak çözülemedi (binary olabilir)."

    content = content.replace("\r\n", "\n")
    note = ""
    if len(content) > MAX_CHARS:
        content = content[:MAX_CHARS]
        note = f"\n\n[Not: Dosya uzun olduğu için ilk {MAX_CHARS} karakter okundu.]"

    return f"[Dosya: {path.name}]\n{content}{note}"


def list_directory(dir_path: str = ".") -> str:
    """List files and folders under a project-relative path."""
    path, err = _resolve_safe_path(dir_path or ".")
    if err:
        return err

    if not path.exists():
        return f"[Liste Hatası]: Klasör bulunamadı → {path}"
    if not path.is_dir():
        return f"[Liste Hatası]: Bu bir klasör değil → {path}"

    try:
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError as e:
        return f"[Liste Hatası]: Klasör listelenemedi: {e}"

    if not entries:
        return f"[Klasör boş]: {path}"

    lines = [f"[Klasör: {path}]"]
    for entry in entries[:100]:
        kind = "DIR " if entry.is_dir() else "FILE"
        size = ""
        if entry.is_file():
            try:
                size = f" ({entry.stat().st_size} bytes)"
            except OSError:
                size = ""
        lines.append(f"  {kind}  {entry.name}{size}")

    if len(entries) > 100:
        lines.append(f"  ... ve {len(entries) - 100} öğe daha")

    return "\n".join(lines)
