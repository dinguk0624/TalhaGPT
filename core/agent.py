import json
import logging

import ollama

from config import OLLAMA_HOST, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class Agent:
    """Main TalhaGPT model/tool execution loop."""

    def __init__(self, model_name: str, tool_registry, max_steps: int = 6, memory=None):
        self.model_name = model_name
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.memory = memory
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.tool_output_max_chars = 12000

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
                logger.warning("Invalid tool arguments: %s", exc)
        return {}

    def _limit_tool_output(self, value) -> str:
        text = str(value)
        if len(text) <= self.tool_output_max_chars:
            return text
        return text[:self.tool_output_max_chars] + "\n[Tool output truncated.]"

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
        stored = [m for m in self._load_memory_messages() if isinstance(m, dict) and m.get("role") != "tool"]
        current = [dict(m) for m in messages if isinstance(m, dict)]
        return stored + [m for m in current if m not in stored]

    def _ensure_system_prompt(self, messages: list[dict]) -> list[dict]:
        result = [dict(m) for m in messages if isinstance(m, dict)]
        system_index = next((i for i, m in enumerate(result) if m.get("role") == "system"), None)
        if system_index is None:
            result.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        elif not result[system_index].get("content"):
            result[system_index]["content"] = SYSTEM_PROMPT
        return result

    def run(self, messages: list[dict]) -> str:
        messages = self._ensure_system_prompt(self._prepare_messages(messages))

        if self.memory is not None:
            existing = self._load_memory_messages()
            for message in messages:
                if message.get("role") != "system" and message not in existing:
                    self._save_message(
                        message.get("role", "user"),
                        message.get("content", ""),
                        **{k: v for k, v in message.items() if k not in {"role", "content"}},
                    )

        for step in range(self.max_steps):
            logger.info("Agent step %s/%s", step + 1, self.max_steps)
            try:
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    tools=self.tool_registry.get_schemas(),
                )
            except Exception as exc:
                logger.exception("Model execution failed")
                return f"Model execution error: {exc}"

            response_message = response.message
            tool_calls = response_message.tool_calls or []
            content = (response_message.content or "").strip()

            if not tool_calls:
                if not content:
                    if step + 1 < self.max_steps:
                        messages.append({"role": "user", "content": "Provide a clear final answer to the user's request."})
                        continue
                    return "Model returned an empty response."
                messages.append({"role": "assistant", "content": content})
                self._save_message("assistant", content)
                return content

            messages.append(response_message)

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                arguments = self._parse_arguments(tool_call.function.arguments)
                if not self.tool_registry.has(tool_name):
                    result = f"Error: Tool '{tool_name}' was not found."
                else:
                    try:
                        result = self.tool_registry.execute(tool_name, arguments)
                    except Exception as exc:
                        logger.exception("Tool execution failed: %s", tool_name)
                        result = f"Error executing tool '{tool_name}': {exc}"

                messages.append({"role": "tool", "content": self._limit_tool_output(result)})

        return f"The agent reached its maximum limit of {self.max_steps} steps."