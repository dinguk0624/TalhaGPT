from core.agent import Agent


def test_parse_arguments_accepts_json_object():
    assert Agent._parse_arguments('{"city": "Ankara"}') == {"city": "Ankara"}


def test_parse_arguments_rejects_invalid_json():
    assert Agent._parse_arguments('{invalid') == {}


def test_limit_tool_output():
    class Registry:
        pass

    agent = Agent("test", Registry(), max_steps=1)
    # Force a small limit so the truncation path is actually exercised
    agent.tool_output_max_chars = 50

    original = "x" * 100
    limited = agent._limit_tool_output(original)

    assert limited.startswith("x" * 50)
    assert limited.endswith("[Tool output truncated.]")
    assert len(limited) < len(original) + 30
