import json
import logging
import re
from typing import Callable

import ollama

from config import OLLAMA_HOST, REQUIRE_TOOL_CONFIRM, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

OLLAMA_OPTIONS = {
    "num_ctx": 4096,
    "num_predict": 256,
    "temperature": 0.7,
    "top_p": 0.9,
    "repeat_penalty": 1.3,
}

KEEP_ALIVE = "30m"
MAX_HISTORY_MSG_CHARS = 2000

RESTRICTED_TOOLS = frozenset({"launch_app", "capture_screen"})

_TOOL_HINTS = re.compile(
    r"("
    r"hava|weather|sıcak|soguk|"
    r"cpu|ram|sistem|system|kaynak|"
    r"ara|search|google|internette|web|url|http|"
    r"aç|ac|launch|başlat|baslat|uygulama|app|"
    r"ekran|screenshot|ekran görüntüsü|capture|"
    r"resim|image|görsel|gorsel|çiz|ciz|generate|"
    r"oku|read|dosya|file|readme|kod|code|"
    r"klasör|klasor|folder|dizin|listele|list|"
    r"not|hatırla|hatirla|remember|kaydet|save|bellek|memory|"
    r"belge|document|rag|index"
    r")",
    re.IGNORECASE,
)


def message_likely_needs_tools(text: str) -> bool:
    if not text or not text.strip():
        return False
    stripped = text.strip()
    if len(stripped) > 120:
        return True
    return bool(_TOOL_HINTS.search(stripped))


def _collapse_repeated_lines(text: str) -> str:
    """Drop consecutive duplicate lines (model repetition loops)."""
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        if out and line == out[-1] and line.strip():
            continue
        out.append(line)
    collapsed = "\n".join(out).strip()

    # Same full paragraph pasted many times without newlines
    if collapsed.count("\n") == 0 and len(collapsed) > 80:
        half = len(collapsed) // 2
        for size in range(min(half, 200), 20, -1):
            unit = collapsed[:size]
            if unit and collapsed == unit * (len(collapsed) // size):
                return unit.strip()
    return collapsed


class Agent:
    """Main TalhaGPT model/tool execution loop."""

    def __init__(
        self,
        model_name: str,
        tool_registry,
        max_steps: int = 4,
        memory=None,
        on_confirm: Callable[[str, dict], bool] | None = None,
        require_confirm: bool | None = None,
    ):
        self.model_name = model_name
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.memory = memory
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.tool_output_max_chars = 6000
        self.on_confirm = on_confirm
        self.require_confirm = (
            REQUIRE_TOOL_CONFIRM if require_confirm is None else require_confirm
        )

    @staticmethod
    def _parse_arguments(arguments) -> dict:
        if arguments is None:
            return {}
        if isinstance(arguments, dict):
            return arguments
        if isinstance(arguments, str):
            try:
                parsed = json.loads(arguments)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError as exc:
                logger.warning("Invalid tool arguments: %s", exp)
        return {}

    def _limit_tool_output(self, value) -> str:
        text = str(value)
        if len(text) <= self.tool_output_max_chars:
            return text
        return text[: self.tool_output_max_chars] + "\n[Tool output truncated.]"

    @staticmethod
    def _trim_message_content(message: dict) -> dict:
        msg = dict(message)
        content = msg.get("content")
        if isinstance(content, str) and len(content) > MAX_HISTORY_MSG_CHARS:
            msg["content"] = content[:MAX_HISTORY_MSG_CHARS] + "\n[...truncated]"
        return msg

    def _save_message(self, role: str, content: str = "", **kwargs) -> None:
        if self.memory is None:
            return
        try:
            self.memory.add_message(role, content, **kwargs)
        except Exception:
            logger.exception("Failed to save message to memory")

    def _load_memory_messages(self) -> list[dict]:
        if self.memory is None:
            return []
        try:
            messages = self.memory.get_messages()
            return messages if isinstance(messages, list) else []
        except Exception:
            logger.exception("Failed to load messages from memory")
            return []

    def _prepare_messages(self, messages: list[dict]) -> list[dict]:
        stored = [
            self._trim_message_content(m)
            for m in self._load_memory_messages()
            if isinstance(m, dict) and m.get("role") != "tool"
        ]
        current = [dict(m) for m in messages if isinstance(m, dict)]
        return stored + [m for m in current if m not in stored]

    def _ensure_system_prompt(self, messages: list[dict]) -> list[dict]:
        result = [dict(m) for m in messages if isinstance(m, dict)]
        system_index = next(
            (i for i, m in enumerate(result) if m.get("role") == "system"), None
        )
        if system_index is None:
            result.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        elif not result[system_index].get("content"):
            result[system_index]["content"] = SYSTEM_PROMPT
        return result

    def _stream_chat(
        self,
        messages: list,
        on_token: Callable[[str], None] | None = None,
        use_tools: bool = True,
    ):
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "stream": True,
            "options": OLLAMA_OPTIONS,
            "keep_alive": KEEP_ALIVE,
        }
        if use_tools:
            kwargs["tools"] = self.tool_registry.get_schemas()

        stream = self.client.chat(**kwargs)

        accumulated = ""
        tool_calls = []
        raw_message = None

        for chunk in stream:
            raw_message = chunk.message
            piece = raw_message.content or ""
            if piece:
                # Support both delta chunks and cumulative full-text chunks
                if accumulated and piece.startswith(accumulated):
                    delta = piece[len(accumulated) :]
                    accumulated = piece
                elif accumulated and accumulated.startswith(piece):
                    # occasional out-of-order / empty progress — ignore
                    delta = ""
                else:
                    delta = piece
                    accumulated += piece

                if delta and on_token is not None:
                    on_token(delta)

            if use_tools and raw_message.tool_calls:
                tool_calls = list(raw_message.tool_calls)

        return accumulated, tool_calls, raw_message

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name in RESTRICTED_TOOLS and self.require_confirm:
            allowed = True
            if self.on_confirm is not None:
                try:
                    allowed = bool(self.on_confirm(tool_name, arguments))
                except Exception:
                    logger.exception("on_confirm failed")
                    allowed = False
            if not allowed:
                return f"Tool '{tool_name}' was denied by the user."

        if not self.tool_registry.has(tool_name):
            return f"Error: Tool '{tool_name}' was not found."
        try:
            return self.tool_registry.execute(tool_name, arguments)
        except Exception as exp:
            logger.exception("Tool execution failed: %s", tool_name)
            return f"Error executing tool '{tool_name}': {exp}"

    def run(
        self,
        messages: list[dict],
        on_token: Callable[[str], None] | None = None,
    ) -> str:
        messages = self._ensure_system_prompt(self._prepare_messages(messages))

        last_user = ""
        for m in reversed(messages):
            if isinstance(m, dict) and m.get("role") == "user":
                last_user = str(m.get("content") or "")
                break
        use_tools = message_likely_needs_tools(last_user)
        if not use_tools:
            logger.info("Fast path: no tools for this turn")

        if self.memory is not None:
            existing = self._load_memory_messages()
            for message in messages:
                if message.get("role") != "system" and message not in existing:
                    self._save_message(
                        message.get("role", "user"),
                        message.get("content", ""),
                        **{
                            k: v
                            for k, v in message.items()
                            if k not in {"role", "content"}
                        },
                    )

        for step in range(self.max_steps):
            logger.info(
                "Agent step %s/%s (tools=%s)", step + 1, self.max_steps, use_tools
            )
            try:
                content, tool_calls, raw_message = self._stream_chat(
                    messages, on_token=on_token, use_tools=use_tools
                )
            except Exception as exp:
                logger.exception("Model execution failed")
                return f"Model execution error: {exp}"

            if not tool_calls:
                content = _collapse_repeated_lines((content or "").strip())
                if not content:
                    if step + 1 < self.max_steps:
                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    "Provide a clear final answer to the user's request."
                                ),
                            }
                        )
                        continue
                    return "Model returned an empty response."

                messages.append({"role": "assistant", "content": content})
                self._save_message("assistant", content)
                return content

            use_tools = True

            if raw_message is not None:
                messages.append(raw_message)
            else:
                messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": tool_calls,
                    }
                )

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                arguments = self._parse_arguments(tool_call.function.arguments)
                result = self._execute_tool(tool_name, arguments)
                messages.append(
                    {"role": "tool", "content": self._limit_tool_output(result)}
                )

        return f"The agent reached its maximum limit of {self.max_steps} steps."
