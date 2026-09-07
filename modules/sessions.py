# modules/sessions.py
"""Multiple named conversation sessions on disk."""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime

from modules.memory import ConversationMemory

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SESSIONS_DIR = os.path.join(PROJECT_ROOT, "data", "sessions")
INDEX_PATH = os.path.join(SESSIONS_DIR, "index.json")
LEGACY_MEMORY = os.path.join(PROJECT_ROOT, "data", "conversation_memory.json")

_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,40}$")


def _now_id() -> str:
    return "s" + datetime.now().strftime("%Y%m%d_%H%M%S")


class SessionStore:
    """Create, list, and switch conversation sessions."""

    def __init__(self, sessions_dir: str = SESSIONS_DIR):
        self.sessions_dir = os.path.abspath(sessions_dir)
        self.index_path = os.path.join(self.sessions_dir, "index.json")
        os.makedirs(self.sessions_dir, exist_ok=True)
        self._index: dict = self._load_index()
        self._migrate_legacy()
        if not self._index.get("sessions"):
            self.create("default")
        if not self._index.get("current"):
            self._index["current"] = self._index["sessions"][0]["id"]
            self._save_index()
        self.memory = self._open(self._index["current"])

    def _load_index(self) -> dict:
        if not os.path.isfile(self.index_path):
            return {"current": "", "sessions": []}
        try:
            with open(self.index_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict) and isinstance(data.get("sessions"), list):
                return data
        except (OSError, json.JSONDecodeError):
            pass
        return {"current": "", "sessions": []}

    def _save_index(self) -> None:
        os.makedirs(self.sessions_dir, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as file:
            json.dump(self._index, file, ensure_ascii=False, indent=2)

    def _session_path(self, session_id: str) -> str:
        return os.path.join(self.sessions_dir, f"{session_id}.json")

    def _migrate_legacy(self) -> None:
        if os.path.abspath(self.sessions_dir) != os.path.abspath(SESSIONS_DIR):
            return
        if not os.path.isfile(LEGACY_MEMORY):
            return
        if any(s.get("id") == "default" for s in self._index.get("sessions", [])):
            return
        dest = self._session_path("default")
        if not os.path.isfile(dest):
            try:
                os.replace(LEGACY_MEMORY, dest)
            except OSError:
                return
        self._index.setdefault("sessions", []).insert(
            0,
            {
                "id": "default",
                "title": "default",
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            },
        )
        self._index["current"] = "default"
        self._save_index()

    def _open(self, session_id: str) -> ConversationMemory:
        return ConversationMemory(
            max_history=12,
            file_path=self._session_path(session_id),
        )

    def current_id(self) -> str:
        return str(self._index.get("current") or "")

    def current_title(self) -> str:
        cid = self.current_id()
        for item in self._index.get("sessions", []):
            if item.get("id") == cid:
                return str(item.get("title") or cid)
        return cid

    def list_sessions(self) -> list[dict]:
        return [dict(item) for item in self._index.get("sessions", [])]

    def create(self, title: str | None = None) -> str:
        session_id = _now_id()
        while any(s.get("id") == session_id for s in self._index.get("sessions", [])):
            time.sleep(0.2)
            session_id = _now_id()
        label = (title or session_id).strip() or session_id
        if _ID_RE.fullmatch(label.replace(" ", "_")) and not any(
            s.get("id") == label.replace(" ", "_") for s in self._index.get("sessions", [])
        ):
            session_id = label.replace(" ", "_")
        entry = {
            "id": session_id,
            "title": label,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        self._index.setdefault("sessions", []).append(entry)
        self._index["current"] = session_id
        self._save_index()
        self.memory = self._open(session_id)
        return session_id

    def switch(self, query: str) -> str | None:
        q = (query or "").strip()
        if not q:
            return None
        q_low = q.casefold()
        match = None
        for item in self._index.get("sessions", []):
            sid = str(item.get("id") or "")
            title = str(item.get("title") or "")
            if sid == q or title.casefold() == q_low or sid.startswith(q):
                match = sid
                break
        if match is None:
            return None
        self._index["current"] = match
        self._save_index()
        self.memory = self._open(match)
        return match

    def touch(self) -> None:
        cid = self.current_id()
        now = datetime.now().isoformat(timespec="seconds")
        for item in self._index.get("sessions", []):
            if item.get("id") == cid:
                item["updated_at"] = now
                break
        self._save_index()
