# modules/memory.py

import json
import os
import tempfile
from typing import Any


class ConversationMemory:
    """
    Persistent conversation memory for TalhaGPT.

    Stores conversation history in a JSON file and
    automatically restores it when TalhaGPT starts again.

    Tool-calling messages and additional message metadata
    can also be stored.
    """

    def __init__(
        self,
        max_history: int = 20,
        file_path: str = "./data/conversation_memory.json",
    ):
        self.max_history = max_history
        self.file_path = os.path.abspath(file_path)

        self.history: list[dict[str, Any]] = []

        self._load()

    # ========================================================
    # LOAD MEMORY
    # ========================================================

    def _load(self) -> None:
        """
        Load previously saved conversation history.

        If the memory file does not exist, the history starts
        empty.

        If the file is invalid or cannot be read, the history
        is reset to an empty list.
        """

        if not os.path.isfile(self.file_path):
            return

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError(
                    "Memory file must contain a JSON list."
                )

            valid_messages = []

            for message in data:
                if isinstance(message, dict):
                    role = message.get("role")

                    if isinstance(role, str):
                        valid_messages.append(message)

            self.history = valid_messages

            self._trim_history()

        except Exception as error:
            print(
                f"[Memory] Failed to load memory: {error}"
            )

            self.history = []

    # ========================================================
    # SAVE MEMORY
    # ========================================================

    def _save(self) -> None:
        """
        Persist the current conversation history to disk.

        Uses a temporary file and atomic replacement to reduce
        the risk of corrupting the memory file if the program
        stops while saving.
        """

        directory = os.path.dirname(self.file_path)

        try:
            if directory:
                os.makedirs(
                    directory,
                    exist_ok=True,
                )

            fd, temporary_path = tempfile.mkstemp(
                prefix="conversation_memory_",
                suffix=".tmp",
                dir=directory if directory else None,
                text=True,
            )

            try:
                with os.fdopen(
                    fd,
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(
                        self.history,
                        file,
                        ensure_ascii=False,
                        indent=2,
                    )

                    file.flush()
                    os.fsync(file.fileno())

                os.replace(
                    temporary_path,
                    self.file_path,
                )

            except Exception:
                if os.path.exists(temporary_path):
                    os.remove(temporary_path)

                raise

        except Exception as error:
            print(
                f"[Memory] Failed to save memory: {error}"
            )

    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        role: str,
        content: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Add a message to the conversation history.

        Additional metadata such as tool_calls can be stored
        through keyword arguments.
        """

        message: dict[str, Any] = {
            "role": role,
            "content": content,
        }

        for key, value in kwargs.items():
            if value is not None:
                message[key] = value

        self.history.append(message)

        self._trim_history()
        self._save()

    # ========================================================
    # TRIM HISTORY
    # ========================================================

    def _trim_history(self) -> None:
        """
        Keep conversation history within max_history.

        The first system message is preserved whenever possible.
        """

        while len(self.history) > self.max_history:

            if (
                self.history
                and self.history[0].get("role") == "system"
            ):
                if len(self.history) > 1:
                    self.history.pop(1)
                else:
                    break

            else:
                self.history.pop(0)

    # ========================================================
    # GET MESSAGES
    # ========================================================

    def get_messages(self) -> list[dict[str, Any]]:
        """
        Return a copy of the conversation history.

        The returned format can be passed to the model.
        """

        return self.history.copy()

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear(self) -> None:
        """
        Clear all conversation history and persist the change.
        """

        self.history.clear()
        self._save()

    # ========================================================
    # LAST MESSAGE
    # ========================================================

    def last_message(self) -> dict[str, Any] | None:
        """
        Return the most recent message.

        Returns None if the conversation history is empty.
        """

        if not self.history:
            return None

        return self.history[-1]

    # ========================================================
    # MESSAGE COUNT
    # ========================================================

    def count(self) -> int:
        """
        Return the number of stored messages.
        """

        return len(self.history)