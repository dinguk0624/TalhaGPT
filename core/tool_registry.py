from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    """Represents a registered TalhaGPT tool."""
    name: str
    description: str
    parameters: dict
    function: Callable[..., Any]


class ToolRegistry:
    """Central registry for managing all TalhaGPT tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str, parameters: dict, function: Callable[..., Any]):
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        if not callable(function):
            raise TypeError(f"Tool '{name}' function must be callable.")
        if not isinstance(parameters, dict):
            raise TypeError("Tool parameters must be a dictionary.")
        self._tools[name] = Tool(name, description, parameters, function)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        return name in self._tools

    def _validate_arguments(self, tool: Tool, arguments: dict) -> str | None:
        if not isinstance(arguments, dict):
            return "Tool arguments must be a JSON object."
        schema = tool.parameters or {}
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        unknown = set(arguments) - set(properties)
        if unknown:
            return f"Unknown argument(s): {', '.join(sorted(unknown))}"
        missing = [name for name in required if name not in arguments]
        if missing:
            return f"Missing required argument(s): {', '.join(missing)}"
        for name, value in arguments.items():
            expected = properties.get(name, {}).get("type")
            if expected == "string" and not isinstance(value, str):
                return f"Argument '{name}' must be a string."
            if expected == "integer" and (isinstance(value, bool) or not isinstance(value, int)):
                return f"Argument '{name}' must be an integer."
            if expected == "number" and (isinstance(value, bool) or not isinstance(value, (int, float))):
                return f"Argument '{name}' must be a number."
            if expected == "boolean" and not isinstance(value, bool):
                return f"Argument '{name}' must be a boolean."
            if expected == "array" and not isinstance(value, list):
                return f"Argument '{name}' must be an array."
            if expected == "object" and not isinstance(value, dict):
                return f"Argument '{name}' must be an object."
        return None

    def execute(self, name: str, arguments: dict) -> str:
        tool = self.get(name)
        if tool is None:
            return f"Error: No tool named '{name}' was found."
        error = self._validate_arguments(tool, arguments)
        if error:
            return f"Tool argument validation error ({name}): {error}"
        try:
            result = tool.function(**arguments)
            return "Tool executed successfully but returned no result." if result is None else str(result)
        except Exception as e:
            return f"Tool execution error ({name}): {e}"

    def get_schemas(self) -> list[dict]:
        return [
            {"type": "function", "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }}
            for tool in self._tools.values()
        ]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())