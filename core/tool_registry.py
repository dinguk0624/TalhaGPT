from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    """
    Represents a registered TalhaGPT tool.
    """

    name: str
    description: str
    parameters: dict
    function: Callable[..., Any]


class ToolRegistry:
    """
    Central registry for managing all TalhaGPT tools.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict,
        function: Callable[..., Any],
    ):
        """
        Register a new tool.
        """

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = Tool(
            name=name,
            description=description,
            parameters=parameters,
            function=function,
        )

    def get(self, name: str) -> Tool | None:
        """
        Get a tool by its name.

        Returns None if the tool does not exist.
        """

        return self._tools.get(name)

    def has(self, name: str) -> bool:
        """
        Check whether a tool is registered.
        """

        return name in self._tools

    def execute(
        self,
        name: str,
        arguments: dict
    ) -> str:
        """
        Execute a registered tool and return
        the result as a string.
        """

        tool = self.get(name)

        if tool is None:

            return (
                f"Error: No tool named '{name}' was found."
            )

        try:

            result = tool.function(
                **arguments
            )

            if result is None:

                return (
                    "Tool executed successfully "
                    "but returned no result."
                )

            return str(result)

        except Exception as e:

            return (
                f"Tool execution error "
                f"({name}): {e}"
            )

    def get_schemas(self) -> list[dict]:
        """
        Generate tool schemas required for
        Ollama function calling.
        """

        schemas = []

        for tool in self._tools.values():

            schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )

        return schemas

    def list_tools(self) -> list[str]:
        """
        Return the names of all registered tools.
        """

        return list(self._tools.keys())