# modules/permissions.py
"""Persistent per-tool permission policies: allow, ask, or deny."""

from __future__ import annotations

import json
import os
from typing import Literal

Policy = Literal["allow", "ask", "deny"]

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_PATH = os.path.join(PROJECT_ROOT, "data", "tool_permissions.json")

SENSITIVE_TOOLS = frozenset(
    {
        "launch_app",
        "capture_screen",
        "generate_image",
        "analyze_image",
    }
)
VALID_POLICIES = frozenset({"allow", "ask", "deny"})


class PermissionManager:
    """Load/save tool policies and decide whether a tool may run."""

    def __init__(self, file_path: str = DEFAULT_PATH):
        self.file_path = os.path.abspath(file_path)
        self._policies: dict[str, Policy] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.isfile(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return
            for name, policy in data.items():
                if isinstance(name, str) and policy in VALID_POLICIES:
                    self._policies[name] = policy
        except (OSError, json.JSONDecodeError):
            self._policies = {}

    def _save(self) -> None:
        directory = os.path.dirname(self.file_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self._policies, file, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def default_policy(self, tool_name: str) -> Policy:
        return "ask" if tool_name in SENSITIVE_TOOLS else "allow"

    def policy_for(self, tool_name: str) -> Policy:
        stored = self._policies.get(tool_name)
        if stored in VALID_POLICIES:
            return stored
        return self.default_policy(tool_name)

    def set_policy(self, tool_name: str, policy: str) -> str:
        name = (tool_name or "").strip()
        value = (policy or "").strip().lower()
        if not name:
            return "[İzin]: Tool adı boş olamaz."
        if value not in VALID_POLICIES:
            return "[İzin]: Politika allow, ask veya deny olmalı."
        self._policies[name] = value  # type: ignore[assignment]
        self._save()
        return f"[İzin]: '{name}' → {value}"

    def list_policies(self, tool_names: list[str] | None = None) -> dict[str, Policy]:
        names = tool_names or sorted(set(SENSITIVE_TOOLS) | set(self._policies))
        return {name: self.policy_for(name) for name in names}
