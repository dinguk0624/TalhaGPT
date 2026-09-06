# modules/logger.py
"""Logging setup with Windows-safe UTF-8 handling."""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime


def _configure_stdio() -> None:
    """Prefer UTF-8 on stdout/stderr so emoji and Turkish text do not crash."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


class _SafeStreamHandler(logging.StreamHandler):
    """StreamHandler that never raises on UnicodeEncodeError."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            stream = self.stream
            try:
                stream.write(msg + self.terminator)
            except UnicodeEncodeError:
                encoding = getattr(stream, "encoding", None) or "utf-8"
                safe = (msg + self.terminator).encode(encoding, errors="replace")
                if hasattr(stream, "buffer"):
                    stream.buffer.write(safe)
                else:
                    stream.write(safe.decode(encoding, errors="replace"))
            self.flush()
        except Exception:
            self.handleError(record)


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_configure_stdio()

logger = logging.getLogger("TalhaGPT")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()
logger.propagate = False

log_file = os.path.join(
    LOG_DIR, f"talha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

console_handler = _SafeStreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger(name: str = "TalhaGPT") -> logging.Logger:
    """Get a logger instance for the specified module."""
    child = logging.getLogger(name)
    child.setLevel(logging.DEBUG)
    # Child loggers propagate to root TalhaGPT handlers when name is nested
    if name != "TalhaGPT" and not name.startswith("TalhaGPT."):
        child = logging.getLogger(f"TalhaGPT.{name}")
        child.setLevel(logging.DEBUG)
    return child
