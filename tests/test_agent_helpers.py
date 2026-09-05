from core.agent import Agent


def test_parse_arguments_accepts_json_object():
    assert Agent._parse_arguments('{"city": "Ankara"}') == {"city": "Ankara"}


def test_parse_arguments_rejects_invalid_json():
    assert Agent._parse_arguments('{invalid') == {}


def test_limit_tool_output():
    class Registry:
        pass

    agent = Agent("test", Registry(), max_steps=1)
    original = "x" * 100
    limited = agent._limit_tool_output(original)
    assert limited.startswith("x" * 100) is False
    assert limited.endswith("[Tool output truncated.]")
