import pytest

from core.tool_registry import ToolRegistry


def test_register_and_execute():
    registry = ToolRegistry()
    registry.register(
        "greet",
        "Greets a user",
        {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
        lambda name: f"Hello {name}",
    )

    assert registry.execute("greet", {"name": "ostam"}) == "Hello ostam"


def test_missing_required_argument():
    registry = ToolRegistry()
    registry.register(
        "greet", "Greets", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}, lambda name: name
    )
    result = registry.execute("greet", {})
    assert "Missing required argument" in result


def test_unknown_argument():
    registry = ToolRegistry()
    registry.register(
        "greet", "Greets", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}, lambda name: name
    )
    result = registry.execute("greet", {"name": "ostam", "extra": True})
    assert "Unknown argument" in result


def test_wrong_argument_type():
    registry = ToolRegistry()
    registry.register(
        "greet", "Greets", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}, lambda name: name
    )
    result = registry.execute("greet", {"name": 123})
    assert "must be a string" in result


def test_unknown_tool():
    registry = ToolRegistry()
    assert "No tool named" in registry.execute("missing", {})


def test_duplicate_tool_registration():
    registry = ToolRegistry()
    registry.register("x", "X", {"type": "object"}, lambda: "x")
    with pytest.raises(ValueError):
        registry.register("x", "X", {"type": "object"}, lambda: "x")
