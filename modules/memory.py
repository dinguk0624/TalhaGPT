import json
import os
import tempfile
from typing import Any


class ConversationMemory:
    """Persistent conversation memory for TalhaGPT."""

    def __init__(self, max_history: int = 20, file_path: str = "./data/conversation_memory.json"):
        self.max_history = max_history
        self.file_path = os.path.abspath(file_path)
        self.history: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not os.path.isfile(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Memory file must contain a JSON list.")
            self.history = [m for m in data if isinstance(m, dict) and isinstance(m.get("role"), str)]
            self._trim_history()
        except Exception as error:
            print(f"[Memory] Failed to load memory: {error}")
            self.history = []

    def _save(self) -> None:
        directory = os.path.dirname(self.file_path)
        temporary_path = None
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            fd, temporary_path = tempfile.mkstemp(
                prefix="conversation_memory_",
                suffix=".tmp",
                dir=directory if directory else None,
                text=True,
            )
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=2)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_path, self.file_path)
            temporary_path = None
        except Exception as error:
            if temporary_path and os.path.exists(temporary_path):
                os.remove(temporary_path)
            print(f"[Memory] Failed to save memory: {error}")

    def add_message(self, role: str, content: str = "", **kwargs: Any) -> None:
        # Tool execution results are transient context and can be very large.
        # Keep them out of durable conversation history.
        if role == "tool":
            return

        message: dict[str, Any] = {"role": role, "content": content}
        for key, value in kwargs.items():
            if value is not None:
                message[key] = value
        self.history.append(message)
        self._trim_history()
        self._save()

    def _trim_history(self) -> None:
        while len(self.history) > self.max_history:
            if self.history and self.history[0].get("role") == "system" and len(self.history) > 1:
                self.history.pop(1)
            else:
                self.history.pop(0)

    def get_messages(self) -> list[dict[str, Any]]:
        return [dict(message) for message in self.history]

    def clear(self) -> None:
        self.history.clear()
        self._save()

    def last_message(self) -> dict[str, Any] | None:
        return dict(self.history[-1]) if self.history else None

    def count(self) -> int:
        return len(self.history)
