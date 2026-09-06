# core/tools.py

from modules.system import get_system_status
from modules.web import fetch_web_page, web_search
from modules.app_launcher import launch_app
from modules.api_tools import get_weather
from modules.journal import save_note
from modules.image_gen import generate_image
from modules.vision import capture_screen
from modules.file_reader import read_local_file, list_directory

from modules.rag import (
    add_document_to_memory,
    search_memory,
)

from .tool_registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    """Create and configure the central TalhaGPT tool registry."""

    registry = ToolRegistry()

    registry.register(
        name="get_weather",
        description="Get the current weather for a specified city.",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name.",
                }
            },
            "required": ["city"],
        },
        function=get_weather,
    )

    registry.register(
        name="get_system_status",
        description="Get the current computer system resource status.",
        parameters={
            "type": "object",
            "properties": {},
        },
        function=get_system_status,
    )

    registry.register(
        name="save_note",
        description=(
            "Save information provided by the user to persistent local memory. "
            "Use when the user asks to remember, save, or store information."
        ),
        parameters={
            "type": "object",
            "properties": {
                "note": {
                    "type": "string",
                    "description": "The information that should be saved to memory.",
                }
            },
            "required": ["note"],
        },
        function=save_note,
    )

    registry.register(
        name="launch_app",
        description="Launch an allowed application on the computer. Currently Windows-only.",
        parameters={
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application.",
                }
            },
            "required": ["app_name"],
        },
        function=launch_app,
    )

    registry.register(
        name="add_document_to_memory",
        description="Add a text document to TalhaGPT's persistent RAG memory.",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the text document to add to memory.",
                }
            },
            "required": ["file_path"],
        },
        function=add_document_to_memory,
    )

    registry.register(
        name="search_memory",
        description="Search TalhaGPT's RAG memory for information relevant to the user's query.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The information to search for in memory.",
                },
                "n_results": {
                    "type": "integer",
                    "description": "The maximum number of relevant memory chunks to return (default 4).",
                    "default": 4,
                },
            },
            "required": ["query"],
        },
        function=search_memory,
    )

    registry.register(
        name="read_file",
        description=(
            "Read the contents of a local text file under the project directory. "
            "Use when the user asks to open, read, show, or inspect a file "
            "(e.g. README, .py, .txt, .md, .json)."
        ),
        parameters={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative or absolute path of the file to read.",
                }
            },
            "required": ["file_path"],
        },
        function=read_local_file,
    )

    registry.register(
        name="list_directory",
        description=(
            "List files and folders in a directory under the project. "
            "Use when the user asks what is in a folder or wants to browse files."
        ),
        parameters={
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "Directory path relative to the project root (default: '.').",
                    "default": ".",
                }
            },
        },
        function=list_directory,
    )

    registry.register(
        name="generate_image",
        description="Generate an image using artificial intelligence based on the user's prompt.",
        parameters={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt describing the image to generate.",
                }
            },
            "required": ["prompt"],
        },
        function=generate_image,
    )

    registry.register(
        name="web_search",
        description="Search the internet for current information.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query.",
                }
            },
            "required": ["query"],
        },
        function=web_search,
    )

    registry.register(
        name="fetch_web_page",
        description="Read the contents of a web page.",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page.",
                }
            },
            "required": ["url"],
        },
        function=fetch_web_page,
    )

    registry.register(
        name="capture_screen",
        description="Capture a screenshot of the computer screen and save it under screenshots/.",
        parameters={
            "type": "object",
            "properties": {},
        },
        function=capture_screen,
    )

    return registry
